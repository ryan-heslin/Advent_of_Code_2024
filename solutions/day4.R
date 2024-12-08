make_masks <- function(n){
    stop <- n- 1
    # horizontal, vertical, four diagonals
    list(rbind(0, 0:stop), rbind(0:stop, 0), rbind(0:stop, 0:stop), rbind(0:stop, 0:(-stop)))

}

flatten <- function(x){ 
    dim(x)  <- NULL
    x
}

pad <- function(X, pad, fill = ""){
    n <- nrow(X)
    m <- ncol(X)
    top <- array(data = fill, dim = c(pad, m))
    X <- rbind(top, X, top)
    n <- n + pad * 2
    side <- array(data = fill, dim = c(n, pad))
    cbind(side, X, side)
}


count_matches <- function(arr, coord, masks, targets){
    check_string <- function(m, targets){
        #if (all((coord - 3) == c(6, 1))){ browser()}
        #if (length(targets) > 2) browser()
        val  <- arr[t(m + coord)] 
        #if( all(val == targets[[1]]) || all(val == targets[[2]])) print(coord - 3)
        
        for (tar in targets){
            if (all(val == tar)){
            return(TRUE)
            }
        }
        FALSE
    }
    part1 <- vapply(masks[[1]], check_string, targets = targets[[1]], FUN.VALUE = numeric(1))  |> 
        sum()
    part2 <- vapply(masks[[2]], check_string, targets = targets[[2]], FUN.VALUE = numeric(1))  |> 
        sum()
    c(part1, part2)
}

raw <- readLines("inputs/day4.txt")  |> 
    lapply(strsplit, split = "")  |> 
    unlist(recursive = FALSE)  |>  
    do.call(what = rbind)

n <- nrow(raw)
m <- ncol(raw)
targets <- list(c("X", "M", "A", "S"), c("S", "A", "M", "X"))
extra  <- length(targets[[1]]) - 1
masks = make_masks(extra + 1)
data <- pad(raw, extra)
pattern = "M.S
.A.
M.S"
pattern <- strsplit(pattern, "\n")[[1]]  |>  
    lapply(\(x) strsplit(x, "")[[1]])  |> 
    do.call(what = rbind)  
letters <- pattern[1,]
letters <- letters[letters != "."]
options <- expand.grid(letters, letters)  |> 
    apply(\(x) c(x[[1]], x[[2]], "A", letters[letters !=x[[2]]], letters[letters != x[[1]]]), MARGIN = 1)  |>
    asplit(MARGIN = 2) 
x_mas_mask <- which(pattern != ".", arr.ind = TRUE) -1
# Reading order
x_mas_mask <- x_mas_mask[order(x_mas_mask[,1]),]  |> 
    t()  |> 
    list()

coords  <- expand.grid((extra + 1):(n + extra), (extra+1):(m+extra), stringsAsFactors =FALSE)  |> 
    as.matrix()  |> 
    asplit(MARGIN = 1)  |> 
    lapply(flatten)

targets <- c(list(targets), list(options))
masks  <- c(list(masks), list(x_mas_mask))

parts <- vapply(coords, count_matches, arr = data, masks = masks , targets = targets, FUN.VALUE = numeric(2))   |> 
    rowSums()
print(parts)

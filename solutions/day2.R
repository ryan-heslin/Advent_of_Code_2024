input  <- readLines("inputs/day2.txt")
processed <- lapply(input, \(x) as.integer(strsplit(x, split = " ")[[1]]))

is_safe <- function(x){
    diffs <- diff(x)
    (all(diffs > 0) || all(diffs < 0)) && (max(abs(diffs)) < 4) 
}

validate <- \(x){ 
    part1 <- is_safe(x)
    part2 <- TRUE

    if(!part1){
        for(i in seq_along(x)){ 
            part2 <- is_safe(x[-i])
            if (part2){
                break
            }
        }
    }
    c(part1, part2)
}

parts <- vapply(processed, validate, FUN.VALUE = integer(2))    |> 
    rowSums()
print(parts)

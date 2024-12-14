parse_machines <- function(machines){
    parse_matrices <- function(x){
        nums <- as.integer(x)
        list(matrix(nums[1:4], nrow = 2, byrow = FALSE), nums[5:6])
    }
    regmatches(machines, gregexpr("[0-9]+", machines))  |> 
        lapply(parse_matrices )
}

gcd <- function(a, b){
    while (b != 0){
        t  <- b
        b <- a %% b
        a <- t
    }
    a
}

solve_equation <- function(pair, cost){
    null <- c(0, 0)
    mat <- pair[[1]]
    # No rank-deficient matrices
    inverse <- matrix(c(mat[[4]], -mat[[3]], -mat[[2]], mat[[1]]), byrow  = TRUE, nrow = 2)
    lhs <- inverse %*% pair[[2]]
    determinant <- det(mat)
    lhs <- as.integer(lhs)
    determinant <- determinant
    result <- lhs %/% determinant
    print(result)
    print(ceiling(result))
    if (!identical(result, ceiling(result))) return (0)
    #browser()
  #result <- tryCatch(solve(pair[[1]], pair[[2]])  , error = function(e) null)
if(any(result > 100) || any(result < 0)){ 
    result <- null
}
crossprod(result, cost)[[1]]
}



text <- readChar("inputs/day13.txt", file.info("inputs/day13.txt")$size)  |> 
    trimws()  |> 
    strsplit("\\n\\n")  |> 
    getElement(1)

data <- parse_machines(text)
part1 <- vapply(data, solve_equation, cost = c(3, 1) , FUN.VALUE = numeric(1))  |> 
    sum()
print(part1)

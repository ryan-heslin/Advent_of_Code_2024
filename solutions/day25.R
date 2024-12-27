parse <- function(string){
    result <- strsplit(string, "\n")  |> 
        getElement(1)  |> 
        lapply(\(x) strsplit(x, "")[[1]]) |> 
        do.call(what = rbind)
    result == "#"
}

solve <- function(locks, keys){
    result <- 0
    for( l in locks){ 
        for(k in keys){ 
            result <- result + (max(l + k) <  2)
        }
    }
    result
}


input <- "inputs/day25.txt"
raw <- readChar(input, file.info(input)$size)[[1]]

data <- gsub("\n+$", "", raw)  |> 
    strsplit("\n\n") |> 
    getElement(1)  |> 
    lapply(parse)

locks  <-  list()
keys  <- list()
width <- ncol(data[[1]])

for (grid in data){
    if (sum(grid[1,]) == width){ 
        locks  <- append(locks, list(grid))
    }else{
        keys  <- append(keys, list(grid))
    }
}

part1 <- solve(locks, keys)
print(part1)

using HungarianAlg: hungarian, display

msize = 4
matrix = rand(0:200, (msize, msize))
println(string(join([string(matrix[a, :]) for a in 1:msize], "\n")))
println()

result = hungarian(matrix)
println(display(result))
println()

println(result.match)
println(result.revenues)
println(result.row_weights)
println(result.col_weights)
println(result.revenue_sum)

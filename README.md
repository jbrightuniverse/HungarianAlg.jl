A Julia implementation of the Hungarian Algorithm for optimal matching in bipartite weighted graphs.

Based on the graph theory implementation in [these notes](http://www.cse.ust.hk/~golin/COMP572/Notes/Matching.pdf) combined with the matrix interpretation in [these notes](https://montoya.econ.ubc.ca/Econ514/hungarian.pdf). 

Also derives from [these](https://github.com/jbrightuniverse/FastHungarianAlgorithm) [prior](https://github.com/jbrightuniverse/hungarianalg) [repos](https://github.com/jbrightuniverse/hungarianalg2) implemented in C and Python.

For a detailed overview, see [this Jupyter notebook](https://github.com/jbrightuniverse/hungarianalg-julia/blob/main/docs/hungarian_algorithm_julia.ipynbb).

# Usage

Installation: `pkg add https://github.com/jbrightuniverse/hungarianalg-julia/`

Import: `using HungarianAlg: hungarian, display`

In Jupyter or within a Julia script, do `using Pkg` and `Pkg.add(PackageSpec(url="https://github.com/jbrightuniverse/hungarianalg-julia"))`

Function call: `result = hungarian(matrix)`

Pretty print: `println(display(result))`

Properties:
- Optimal Matching: `result.match`
- Revenues: `result.revenues`
- Row Weights: `result.row_weights`
- Col Weights: `result.col_weights`
- Total Revenue: `result.revenue_sum`

See `docs/example.jl` for a comprehensive example.

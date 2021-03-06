A Julia implementation of the Hungarian Algorithm for optimal matching in bipartite weighted graphs.

Based on the graph theory implementation at [http://www.cse.ust.hk/~golin/COMP572/Notes/Matching.pdf](http://www.cse.ust.hk/~golin/COMP572/Notes/Matching.pdf) combined with the matrix interpretation at [https://montoya.econ.ubc.ca/Econ514/hungarian.pdf](https://montoya.econ.ubc.ca/Econ514/hungarian.pdf). 

Also derives from [these](https://github.com/jbrightuniverse/FastHungarianAlgorithm) [prior](https://github.com/jbrightuniverse/hungarianalg) [repos](https://github.com/jbrightuniverse/hungarianalg2) implemented in C and Python.

For a detailed overview, see [this Jupyter notebook](https://github.com/jbrightuniverse/HungarianAlg.jl/blob/master/docs/hungarian_algorithm_julia.ipynb).

# Usage

Installation: `pkg add https://github.com/jbrightuniverse/HungarianAlg.jl/`

Import: `using HungarianAlg: hungarian, display`

In Jupyter or within a Julia script, do `using Pkg` and `Pkg.add(PackageSpec(url="https://github.com/jbrightuniverse/HungarianAlg.jl"))`

Function call: `result = hungarian(matrix)`

Pretty print: `println(display(result))`

Properties:
- Optimal Matching: `result.match`
- Revenues: `result.revenues`
- Row Weights: `result.row_weights`
- Col Weights: `result.col_weights`
- Total Revenue: `result.revenue_sum`

See `docs/example.jl` for a comprehensive example.

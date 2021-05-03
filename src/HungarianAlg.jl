module HungarianAlg

    mutable struct Result
        #= A simple result object. =#
        match
        revenues
        row_weights
        col_weights
        revenue_sum
    end

    function hungarian(matrx)
        #= Runs the Hungarian Algorithm on a given matrix and returns the optimal matching with potentials. =#
        
        # Step 1: Prep matrix, get size
        matchsize = size(matrx)[1]
        
        # Step 2+3: Generate trivial potentials and alternating tree
        rpotentials = []
        cpotentials = []
        matching = -1 * ones(Int64, 1, matchsize)
        x_parents =  -1 * ones(Int64, 1, matchsize)
        y_parents =  -1 * ones(Int64, 1, matchsize)
        for i = 1:matchsize
            # the row weight is the maximum revenue in a row
            push!(rpotentials, maximum(matrx[i,:]))
            push!(cpotentials, 0)
        end

        treed_x = BitSet([1])
        untreed_y = BitSet(1:matchsize)
        treed_y = BitSet()

        # Step 4: Loop while our matching is too small
        while -1 in matching
            # Step A: Find any neighbour in equality graph
            # where a row is in the tree and a col is not in the tree
            pair = nothing
            for x in treed_x, y in untreed_y
                if matrx[x, y] == rpotentials[x] + cpotentials[y]
                    pair = [x, y]
                    break
                end
            end
                
            if isnothing(pair)
                # Step B: If all firms are in the tree, update potentials to get a new one
                big = Inf
                # iterate over relevant pairs
                for dx in treed_x, dy in untreed_y
                    # find the difference and check if its smaller than any we found before
                    alpha = rpotentials[dx] + cpotentials[dy] - matrx[dx, dy]
                    if alpha < big
                      big = alpha
                      pair = [dx, dy]
                    end
                end

                # apply difference to potentials as needed
                for dx in treed_x 
                    rpotentials[dx] -= big
                end

                for dy in treed_y
                    cpotentials[dy] += big
                end
            end

            if !(pair[2] in matching)
                # Step D: Firm is not matched so add it to matching 
                matching[pair[1]] = pair[2]
                # Step E: Swap the alternating path in our alternating tree attached to the worker we matched
                source = pair[1]
                matched = 1
                while true
                    if matched == 1
                        if x_parents[source] == -1
                            break
                        end
                        above = x_parents[source]
                    else
                        above = y_parents[source]
                        matching[above] = source
                    end
                    matched = 1 - matched
                    source = above
                end

                # Step F: Destroy the tree, go to Step 4 to check completion, and possibly go to Step A
                if -1 in matching
                    x_parents =  -1 * ones(Int64, 1, matchsize)
                    y_parents =  -1 * ones(Int64, 1, matchsize)
                    free = findfirst(isequal(-1), matching)[2]
                    treed_x = BitSet([free])
                    untreed_y = BitSet(1:matchsize)
                    treed_y = BitSet()
                end            

            else
                # Step C: Firm is matched so add it to the tree and go back to Step A
                wasMatchedTo = findfirst(isequal(pair[2]), matching)[2]
                push!(treed_x, wasMatchedTo)
                push!(treed_y, pair[2])
                delete!(untreed_y, pair[2])
                y_parents[pair[2]] = pair[1]
                x_parents[wasMatchedTo] = pair[2]
            end

        end
        revenues = [matrx[i, matching[i]] for i = 1:matchsize]
        return Result([[i, matching[i]] for i = 1:matchsize], revenues, rpotentials, cpotentials, sum(revenues))
    end

    function display(self)
        #= A function for pretty-printing a Hungarian Algorithm Result =#
        matchsize = length(self.match)
        maxlen = max(length(string(maximum(self.revenues))), length(string(minimum(self.revenues))))
        baselist = [[" "^maxlen for i = 1:matchsize] for j = 1:matchsize]
        for i = 1:matchsize
            entry = self.match[i]
            newstring = string(self.revenues[i])
            if length(newstring) > maxlen
                appender = ""
            else
                appender = " "^(maxlen - length(newstring))
            end
            baselist[entry[1]][entry[2]] = appender * newstring
        end
        formatted_list = join([string(row) for row in baselist], "\n")
        return "Matching:\n" * formatted_list*"\n\nRow Potentials: " * string(self.row_weights) * "\nColumn Potentials: " * string(self.col_weights)
    end

end

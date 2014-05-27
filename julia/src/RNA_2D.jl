module RNA_2D


# README
#
# -structure type definition
# -structure validation (Vienna dot bracket)
# -conversion between representations (dot bracket, mountain, base pair set)
# -distance functions (mountain, base pair set, hausdorff)
# -RNAshapes (lvl 1,3,5) abstract shapes
# -Annotated level 5 abstract shape (bp or length)



export structure,           #2D structure type
       testDotBracket,      #tests Vienna dotbracket
       dotBracketToMountain,#dot bracket -> moutain
       dotBracketToBPSet,   #dot bracket -> bp set
       mountainDistance,    #dist(moutain1, mountain2)
       basePairSetDistance, #dist(bpset1, bpset2)
       hausdorffDistance,   #dist(bpset1, bpset2)
       levenshteinDistance  #dist(string1, string2), aka edit distance



immutable structure
  # 2D structure representation
  dotBracket::String              #Vienna dot bracket
  mountain::Vector{Int}           #mountain representation of the dot bracket
  base_pair_set::Vector{(Int,Int)}#base pair set (sorted) of the dot bracket
  energy::FloatingPoint           #energy of the structure
  id                              #id of the sequence the structure belongs to
  seq                             #sequence of the structure

  function structure{T <: String}(dotBracket::T;
                                  energy = -Inf,
                                  id = None,
                                  seq=None)
    @assert testDotBracket(dotBracket) == true
    dotBracket = convert(String, dotBracket)
    mountain = dotBracketToMountain(dotBracket)
    base_pair_set = dotBracketToBPSet(dotBracket)
    new(dotBracket, mountain, base_pair_set, energy, id, seq)
  end
end



function testDotBracket(dotBracket::String)
  #tests Vienna dot-bracket for illegal structure (or symbol)
  counter = 0
  for i in dotBracket
    if i=='('
      counter+=1
    elseif i==')'
      counter-=1
    elseif i!='.' #illegal symbol
      return false
    end
    if counter < 0 #unbalanced structure
      return false
    end
  end

  if counter!= 0
    return false #unbalanced structure
  end
  return true
end



function dotBracketToMountain(dotBracket::String)
  #Vienna dotbracket to mountain representation
  #e.g. "..(((.....))).." -> [0, 0, 1, 2, 3, 3, 3, 3, 3, 3, 2, 1, 0, 0, 0]
  counter = 0
  val = Int[]
  for i in dotBracket
    if(i=='(')
      counter += 1
    elseif(i==')')
      counter -= 1
    end
    push!(val, counter)
  end
  return val
end



function dotBracketToBPSet(dotBracket::String)
  #Vienna dotbracket to base pair set (sorted list by first base of the pair)
  # "((..))" -> [(1,6), (2,5)]
  bpset= (Int,Int)[]
  accumulator = Int[]
  count = 1 #1 indexed
  for i in dotBracket
    if i == '('
      push!(accumulator, count)
    elseif i ==')'
      push!(bpset, (pop!(accumulator), count))
    end
    count += 1
  end
  return sort(bpset)
end



function sequenceDotBracketToBPSeq{S<:String}(dotBracket::S, sequence::S)
  #Vienna dotbracket 
  #@assert 


end



function mountainDistance(m1::Vector{Int}, m2::Vector{Int})
  #lp1 mountain distance on two mountains representation of same length
  #e.g. [1,2,2,2,1], [1,2,3,2,1] = 1
  @assert length(m1) == length(m2)
  absdiff(x::(Int,Int))= abs(x[1]-x[2])
  return mapreduce(absdiff, +, zip(m1, m2))
end



function basePairSetDistance(bp1::Vector{(Int,Int)}, bp2::Vector{(Int,Int)})
  #naive base pair distance (cardinality of symmetric difference, |(A\B)U(B\A)|)
  return length(symdiff(bp1, bp2))
end



function hausdorffDistance(bp1::Vector{(Int,Int)}, bp2::Vector{(Int,Int)})
  function distanceBP(a::(Int, Int), b::(Int, Int))
    return max(abs(a[1]-b[1]), abs(a[2]-b[2]))
  end
  
  function distanceBPtoSet(a::(Int, Int), b::Vector{(Int,Int)})
    return minimum(map(x->distanceBP(a,x), b))
  end
  
  hausdorffLefttoRight = maximum(map(x->distanceBPtoSet(x,bp2), bp1))
  hausdorffRightToLeft = maximum(map(x->distanceBPtoSet(x,bp1), bp2))
  return max(hausdorffLefttoRight, hausdorffRightToLeft)
end



function levenshteinDistance{T<:String}(s::T, t::T)
  # levenshtein distance between two strings (also known as edit distance)
  #(in our case, two vienna dot bracket secondary structures)
  m = length(s)
  n = length(t)
  d = zeros(m+1,n+1)
  for i = 1:m+1
    d[i, 1] = i-1
  end

  for j=1:n+1
    d[1,j] = j-1
  end

  for j=2:n+1
    for i =2:m+1
      if s[i-1] == t[j-1]
        d[i,j] = d[i-1, j-1]
      else
        choices = [d[i-1, j]+1, d[i, j-1]+1, d[i-1, j-1]+1]
        d[i,j] = minimum(choices)
      end
    end
  end
  return d[m,n]
end


#multiple dispatch for structure type
mountainDistance(s1::structure, s2::structure) = mountainDistance(s1.mountain, s2.mountain)
basePairSetDistance(s1::structure, s2::structure) = basePairSetDistance(s1.base_pair_set, s2.base_pair_set)
hausdorffDistance(s1::structure, s2::structure) = hausdorffDistance(s1.base_pair_set, s2.base_pair_set)
levenshteinDistance(s1::structure, s2::structure) = levenshteinDistance(s1.dotBracket, s2.dotBracket)




function getStems(structure::String)
  #helper for abstract shape analysis
  #returns the stems
  @assert RNA_2D.testDotBracket(structure) == true
  list_opener = Int[]
  stems = (Vector{Int}, Vector{Int}, Dict{Int, Int})[]
  list_stem_end = Int[]

  i = 1
  # separate into stems
  while i <= length(structure)
    #add to opening list
    if structure[i] == '('
      push!(list_opener, i)

    #find the closing in the opening list
    elseif structure[i] == ')'
      stem = (Int[], Int[], Dict{Int, Int}())

      while i <= length(structure)
        if structure[i] == ')'
          opener = pop!(list_opener)
          push!(stem[1], opener)
          push!(stem[2], i)
          stem[3][opener] = i

          if (!isempty(list_opener)) && (list_opener[end] in list_stem_end)
            push!(list_stem_end, list_opener[end])
            break
          end

        elseif structure[i] =='('
          if (!isempty(list_opener))
            push!(list_stem_end, list_opener[end])
          end
          i -= 1
          break
        end

        i += 1
      end

      push!(stems, stem)
    end
    i += 1
  end
  return stems
end


function RNAshapes(structure::String)
  #computes RNA abstract shapes level 1, 3 and 5 for the given structure string

  #get the stems
  stems = getStems(structure)

  # build the level1 for each stems
  range_occupied = {}
  dict_lvl1 = Dict()
  for stem in stems
    range_open  = collect([ (minimum(stem[1])) : (maximum(stem[1])) ])
    range_close = collect([ (minimum(stem[2])) : (maximum(stem[2])) ])
    range_occupied = vcat(range_occupied, range_open, range_close)

    temp_lvl1_open = ""
    temp_lvl1_close = ""
    last_opener = None
    last_closer = None

    for opener in sort(stem[1])
      if last_opener == None
        temp_lvl1_open = string(temp_lvl1_open, "[")
        temp_lvl1_close = string("]", temp_lvl1_close)
      else
        if abs(opener - last_opener) != 1
          temp_lvl1_open = string(temp_lvl1_open, "_")
        end
        if abs(stem[3][opener] - last_closer) != 1
          temp_lvl1_close = string("_", temp_lvl1_close)
        end
        if (endswith(temp_lvl1_open , "_")) || (beginswith(temp_lvl1_close, "_"))
          temp_lvl1_open = string(temp_lvl1_open, "[")
          temp_lvl1_close = string("]", temp_lvl1_close)
        end
      end
      last_opener = opener
      last_closer = stem[3][opener]
    end

    dict_lvl1[ minimum(stem[1]) ] = {"elem" => temp_lvl1_open,  "lvl5" => "["}
    dict_lvl1[ minimum(stem[2]) ] = {"elem" => temp_lvl1_close, "lvl5" => "]"}
    println(dict_lvl1)
  end

  #assemble level1
  level1 = ""
  level5 = ""

  for i= 1:length(structure)
    if i in keys(dict_lvl1)
      level1 = string(level1, dict_lvl1[i]["elem"])
      level5 = string(level5, dict_lvl1[i]["lvl5"])
    end

    if structure[i] == '.' && (! endswith(level1, "_")) && (!(i in range_occupied))
      level1 = string(level1, "_")
    end
  end
  println("level 5 = $level5")
  level1 = replace(level1, "[_]", "[]")
  level1 = replace(level1, " ", "")
  level3 = replace(level1, "_", "")

  #particular case
  if(level5 == "")
    level5 = "_"
    level3 = "_"
  end
  return (level5, level3, level1)
end


function shapeLvl5Annotated{T<:String}(structure::T)
  #annotate the lvl 5 abstract shape
  #2 annotations
  #(first opening, last closing, number of base pairs)
  #(first opening, last closing, (range opening, range closing))
  @assert testDotBracket(structure) == true

  stems = getStems(structure)
  println(stems)
  pairs1 = (Int, Int,Int)[]         #3rd field number of base pairs
  pairs2 = (Int, Int, (Int, Int))[] #3rd field is (range_open, range_close)
  for stem in stems
    push!(pairs1, (minimum(stem[1]), maximum(stem[2]), length(stem[3])))
    push!(pairs2, (minimum(stem[1]), maximum(stem[2]),(maximum(stem[1])- minimum(stem[1]), maximum(stem[2])-minimum(stem[2]))))
  end

  lvl5 = (Int, String)[]
  for stem in pairs1
    push!(lvl5, (stem[1], "["))
    push!(lvl5, (stem[2], "]"))
  end
  sort!(lvl5)
  (sort(pairs1), sort(pairs2), join(map(x->x[2], lvl5)))
end




end
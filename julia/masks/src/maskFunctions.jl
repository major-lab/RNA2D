#mask functions
# - destroy percentage of a mask


function isRNA{S<:String}(seq::S)
  #verifies that the sequence is RNA
  #accepts T
  seq = uppercase(seq)
  for nt in seq
    if !(nt in ['A','T','C','G','U'])
      return false
    end
  end
  return true
end


function isBalancedMask{S<:String}(mask::S)
  #verifies that the given mask is balanced
  #format is :
  #           'x' -> unknown
  #           '.' -> unpaired
  #    '(' or ')' -> paired
  count = 0
  for info in mask
    if info == '('
      count += 1
    elseif info == ')'
      count -= 1
    elseif info != 'x'
      return false
    end

    if count < 0
      return false
    end
  end

  if count != 0
    return false
  else
    return true
  end
end


function destroyNonCanonicalFromMask{S <: String}(balancedMask::S, RNAsequence::S)
  #removes non canonical base pairs from the mask
  @assert isRNA(RNAsequence) == true
  @assert isBalancedMask(mask) == true
  @assert length(balancedMas) == length(RNAsequence)

  function isCanonical(a,b)
    #checks if the base pair is canonical or not
    if a == 'T' || a == 't'
      a = 'U'
    elseif b == 'T' || b == 't'
      b = 'U'
    end
    pair = [uppercase(a), uppercase(b)]
    sort!(pair)
    pair = (pair[1], pair[2])
    pair in [('A', 'U'), ('C','G')]
  end

  paired = (Int,Int)[]
  unpaired = Int[]
  openingPair = Int[]
  for (i, info) in enumerate(balancedMask)
    if info == '('
      push!(openingPair, i)
    elseif info == ')'
      opening = pop!(openingPair)
      if isCanonical(RNAsequence[opening], RNAsequence[i])
        push!(paired, (opening, i))
      end
    elseif info == '.'
      push!(unpaired, i)
    end
  end

  resultMask = Char[]
  for i = 1:length(balancedMask)
    push!(resultMask, 'x')
  end
  for i in unpaired
    resultMask[i] = '.'
  end
  for (i,j) in paired
    resultMask[i] = '('
    resultMask[j] = ')'
  end
  CharString(resultMask)
end



function percentageBalancedMask{S<:String}(balancedMask::S, percentage::FloatingPoint)
  #separates the information in the mask by paired or unpaired types
  #destroys a portion of it randomly (depending on given percentage)
  #the percentage is the floor of percentage * length(paired)
  #                               percentage * length(unpaired)
  #this technique was used in the RNA folding benchmark
  @assert  0 <= percentage <= 1
  @assert isBalancedMask(balancedMask) == true
  paired = (Int, Int)[]
  unpaired = Int[]
  openingPair = Int[]

  for (i, info) in enumerate(balancedMask)
    if info == '.'
      push!(unpaired, i)
    elseif info == '('
      push!(openingPair, i)
    elseif info == ')'
      push!(paired, (pop!(openingPair, i)))
    end
  end

  shuffle!(paired)
  shuffle!(unpaired)

  toKeepPaired = floor(percentage * length(paired))
  toKeepUnpaired = floor(percentage * length(unpaired))

  if toKeepPaired == 0
    paired = []
  else
    paired = paired[1:toKeepPaired]
  end
  if toKeepUnpaired == 0
    unpaired = []
  else
    unpaired = unpaired[1:toKeepUnpaired]
  end

  resultMask = Char[]
  for i = 1:length(balancedMask)
    push!(resultMask, 'x')
  end
  for i in unpaired
    resultMask[i] = '.'
  end
  for (i,j) in paired
    resultMask[i] = '('
    resultMask[j] = ')'
  end
  CharString(resultMask)
end



function conciliateUnbalancedMask{S<:String}(unbalancedMask1::S, unbalancedMask2::S)
  #conciliate
  @assert length(masks1) == length(masks2)
  for sym in collect(unbalancedMask1)
    @assert sym in keys(symbols)
  end

  for sym in collect(unbalancedMask2)
    @assert sym in keys(symbols)
  end

  const symbols = { #should make this an enum really
    ')' => 1,
    '(' => 2,
    '.' => 3,
    'x' => 4,
    '|' => 5,
    '-' => 6,
    '[' => 7,
    ']' => 8,
    '+' => 9,
    '_' => 10,
    '<' => 11,
    '>' => 12,
    '!' => 13,
    'p' => 14,
    'q' => 15
  }

  const conciliationMatrix = Array[
  # warning : Julia is row-major (and 1-based, but that's been fixed)
  #)  (  .  x  |  -  [  ]  +  _  <  >  !  p  q 
  #1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
  [ 1, 0, 0, 1, 1,12, 0, 8, 8, 8, 0,12,12, 0, 1], # ) 1   reverse paired
  [ 0, 2, 0, 2, 2,11, 7, 0, 7, 7,11, 0,11, 2, 0], # ( 2   forward paired
  [ 0, 0, 3, 3, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 3], # . 3   unpaired
  [ 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15], # x 4   don't care
  [ 1, 2, 0, 5, 5,13, 7, 8, 9, 9,11,12,13,14,15], # | 5   paired
  [12,11, 3, 6,13, 6, 0, 0, 0, 3,11,12,13, 0, 0], # - 6   not (canonically paired)
  [ 0, 7, 0, 7, 7, 0, 7, 0, 7, 7, 0, 0, 0, 7, 0], # [ 7   forward (canonically paired)
  [ 8, 0, 0, 8, 8, 0, 0, 8, 8, 8, 0, 0, 0, 0, 8], # ] 8   reverse (canonically paired)
  [ 8, 7, 0, 9, 9, 0, 7, 8, 9, 9, 0, 0, 0, 0, 0], # + 9   (canonically paired)
  [ 8, 7, 3,10, 9, 3, 7, 8, 9,10, 0, 0, 0, 0, 0], # _ 10  not (paired non canonically)
  [ 0,11, 0,11,11,11, 0, 0, 0, 0,11, 0,11,11, 0], # < 11  forward (paired non canonically)
  [12, 0, 0,12,12,12, 0, 0, 0, 0, 0,12,12, 0,12], # > 12  reverse (paired non canonically)
  [12,11, 0,13,13,13, 0, 0, 0, 0,11,12,13, 0, 0], # ! 13  (paired non canonically)
  [ 0, 2, 3,14, 2,11, 7, 0, 7, 0,11, 0, 0,14, 0], # p 14  not (reverse paired)
  [ 1, 0, 3,15, 1,12, 0, 8, 8, 0, 0,12, 0, 0,15]  # q 15  not (forward paired)
  ]

  unbalancedMask1 = map(x->symbols[x], collect(unbalancedMask1))
  unbalancedMask2 = map(x->symbols[x], collect(unbalancedMask2))
  result = [-1 for i = 1:length(unbalancedMask1)]
  for i = 1:length(unbalancedMask1) #conciliate the masks
    result[i] = conciliationMatrix[unbalancedMask2[i], conciliatedMask1[i]]
  end

  #print a nice error message if there is information that is not possible to conciliate
  errorPositions = (Int, Char, Char)[]
  for (i, sym) in enumerate(result)
    if sym == -1
      push!(errorPositions, (i, unbalancedMask1[i], unbalancedMask2[i]))
    end
  end

  if length(errorPositions) == 0
    return result

  else
    errorMessage = String[]
    for err in errorPositions
      push!(errorMessage, "($(err[1]) and $(err[2]) at position $(err[3]) are incompatible\n")
    end
    error(join(errorMessage))
  end
end



function shapeLvl5Annotated{T<:String}(dotBracket::T)
  #annotate the lvl 5 abstract shape
  #2 annotations
  #(first opening, last closing, number of base pairs)
  #(first opening, last closing, (range opening, range closing))
  @assert isValidDotBracket(dotBracket) == true

  stems = getStems(dotBracket)
  #println(stems)
  pairs1 = (Int, Int,Int)[]         #3rd field number of base pairs
  pairs2 = (Int, Int, (Int, Int))[] #3rd field is (range_open, range_close)
  for stem in stems
    push!(pairs1, (minimum(stem[1]), maximum(stem[2]), length(stem[3])))
    push!(pairs2, (minimum(stem[1]), maximum(stem[2]),(maximum(stem[1])- minimum(stem[1]), maximum(stem[2])-minimum(stem[2]))))
  end

  lvl5 = (Int, String)[]
  for stem in pairs1
    push!(lvl5, (stem[1], "["))
    push!(lvl5, (stem[2], "]$(stem[3])"))
  end
  sort!(lvl5)
  (sort(pairs1), sort(pairs2), join(map(x->x[2], lvl5)))
end


type shape
  #representation of lvl5 shape
  leftMost::Int
  rightMost::Int
  basePairs::Dict{Int, Int}
  #no children implies shape is a leaf
  children::Vector{shape} # length(children) != 1
  parent::Union(shape, UnionType)
  pairCount::Int

  function shape(leftMost,
                rightMost,
                basePairs,
                children=shape[],
                parent = None)
    new(leftMost, rightMost, basePairs, children, parent, 0)
  end
end





function shapeTreeToString(root::shape)
  #show preorder traversal of the shape (will output lvl5 shape, with annotation)
  shapeVector = (Int, String)[]
  function preOrder(s::shape)
    push!(shapeVector, (s.leftMost, "["))
    push!(shapeVector, (s.rightMost, "]$(length(s.basePairs))"))
    for child in s.children
      preOrder(child)
    end
  end
  for s in root.children
    preOrder(s)
  end
  join(map(x->x[2], sort(shapeVector)))
end

function show(io::IO, root::shape)
  write(io, shapeTreeToString(root))
end


function dotBracketToShapeTree{S<:String}(dotBracket::S)
  #Vienna dot bracket to lvl5 shape tree
  @assert isValidDotBracket(dotBracket) == true
  stems = sort(getStems(dotBracket), by = x->minimum(x[1]))
  leftRight = (Int, Int, Dict{Int, Int})[]
  for stem in stems
    push!(leftRight, (minimum(stem[1]), maximum(stem[2]), stem[3]))
  end

  root = shape(0, length(dotBracket)+1, Dict{Int, Int}())
  position = root
  closing = Int[]
  i = 1
  while length(leftRight) != 0
    #opening case
    if leftRight[1][1] == i
      stem = shift!(leftRight)
      push!(closing, stem[2])
      child = shape(stem[1], stem[2], stem[3], shape[], position)
      push!(position.children, child)
      position = child #go down

    #closing case
    elseif i in closing
      position = position.parent #go up
    end
    i+=1
  end
  root
end


function getBPCount(inputShape::shape)
  #returns the number of bp nested in the shape
  count = Int[]
  function preOrder(s::shape)
    #preorder traversal
    push!(count,length(s.basePairs))
    for child in s.children
      preOrder(child)
    end
  end
  preOrder(inputShape)
  sum(count)
end


function removeUnpaired{S<:String}(dotBracket::S)
  #removes the unpaired character '.' from the dotbracket
  @assert isValidDotBracket(dotBracket)
  result = Char[]
  for c in dotBracket
    if c =='(' || c==')'
      push!(result, c)
    end
  end
  CharString(result)
end


function dotBracketToTree{S<:String}(dotBracket::S)
  #
  @assert isValidDotBracket(dotBracket)
  result = Tree()
  
end
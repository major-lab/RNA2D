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




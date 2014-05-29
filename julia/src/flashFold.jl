

using ArgParse

#BEGIN CONSTANTS

# Minimum unpaired nucleotides in a terminal loop.
# (can set MIND=1 if you want but energies in MCFold 
# original database for NCMs of type (.) are all +Inf
const MIND = 2

# min space required to start a multi-branch,
# changed to 3 to allow for terminal long loops
const MIN_MB = 3

# max number of nucleotides in a terminal loop 
# described by an NCM (including closing bp)
const MAX_NCM_TERMINAL_LOOP = 6

# max NCM identifier (or NCMID)
const NCMs = 21

# Minimum NCMID of 2 strands. Smaller values are terminal
# loop NCMs (or one strand NCMs)
const FIRST_TWO_STRANDS_NCM = 4

# hairpin loops consisting of only one terminal 1_1_X NCM
# are normally dissallowed ( 0 )
const ALLOW_STEMS_OF_ONE = false

# allow long unpaired nucleotides loop to cap stems
const ALLOW_LONG_TERMINAL_LOOP = false

#mask symbols
const maskSymbols = {
  ')' => 1,   # reverse paired
  '(' => 2,   # forward paired
  '.' => 3,   # unpaired
  'x' => 4,   # don't care
  '|' => 5,   # paired
  '-' => 6,   # not canonically paired
  '[' => 7,   # forward canonically paired
  ']' => 8,   # reverse canonically paired
  '+' => 9,   # canonically paired
  '_' => 10,  # not (paired non canonically)
  '<' => 11,  # forward paired non canonically
  '>' => 12,  # reverse paired non canonically
  '!' => 13,  # paired non canonically
  'p' => 14,  # not reverse paired
  'q' => 15   # not forward paired
}

#END CONSTANTS



#BEGIN UTILITIES

function seqtoInt{S<:String}(rnaSequence::S)
  # convert a RNA as character string to integer string 
  # where A->1, C->2, G->3, U->4, T->4
  # throw error if another character found in stream
  result = Int[]
  for c in collect(rnaSequence)
    if c in ['A', 'a']
      push!(result, 1)
    elseif c in ['C', 'c']
      push!(result, 2)
    elseif c in ['G', 'g']
      push!(result, 3)
    elseif c in ['T', 'U', 't', 'u']
      push!(result, 4)
    else
      error("wrong character \"$c\" in seq")
    end
  end
  result
end

function seq2idx(seqAsInt::Vector{Int}, i::Int, j::Int, k::Int, l::Int)
  # Generate an index value usable to access the NCMs energy values from the table energies.
  # seqAsInt is the sequence of nucleotides coded as integers (A=1, C=2, G=3, U=4)
  # i..k is the interval for the 5' strand of the NCM
  # j..l is the interval for the 3' strand of the NCM
  # if there is only one strand in the NCM, then set j and l to -1
  # The value computed is subtracted by 20 because the energies table does not contain values for the first 20 entries (dinucleotides)
  # The value is further subtracted by 1 because the formula computes indexes usable in R where tables and vectors start with value 1.
#   val = 0
#   posInWord = 1
#   if l > 0
#     while l >= j

end




#END UTILITIES



#BEGIN MASK FACILITIES


function string2balanced_idb{S<:String}(balanced_mask::S)
  #user supplied balanced mask is converted to an integer dot bracket
  #representation and checked for integrity at the same time.
  #masks are composed of chars from ().x where ( must match ),
  #x is -1 and . is self index (ie: idb[i]=i)
  result = Int[]
  count = 0
  for sym in collect(balanced_mask)
    if !(sym in ['(', ')', '.', 'x'])
      error("ERROR: mask symbol $sym not valid")
    elseif sym == '('
      count += 1
      push!(result, maskSymbols[sym])
    elseif sym == ')'
      count -= 1
      push!(result , maskSymbols[sym])
    else
      push!(result, maskSymbols[sym])
    end

    if count < 0
      error("ERROR: unbalanced mask")
    end
  end
  if count != 0
    error("ERROR: unbalanced mask")
  end
  result
end


function string2UMASK_idb{S<:String}(unbalanced_mask::S)
  #no error checking in this one
  result = Int[]
  for sym in collect(unbalanced_mask)
    if !(sym in keys(maskSymbols))
      error("ERROR: invalid symbol $sym")
    end
    push!(result, maskSymbols[sym])
  end
  result
end


#END MASK FACILITIES



#BEGIN forward: INSIDE ALGORITHM


#END forward : INSIDE ALGORITHM
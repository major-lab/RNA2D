
class rna2Dstructure(object):
    """2D structure representation of RNA"""
    def __init__(self, dotBracket, energy=float("inf"),\
                 identification="", seq="" ):
      assert isRNA(seq)
      assert isValidDotBracket(dotBracket)
      self.dotBracket = dotBracket
      self.energy = energy
      self.identification = identification
      self.seq = seq



def isRNA(seq):
    """verifies the identity of the nucleotides in the sequence"""
    upperSeq = seq.upper()
    for nt in upperSeq:
        if not(nt in ['A','T','C','G','U']):
            return False
    return True

def isValidDotBracket(dotBracket):
    """tests Vienna dot-bracket for illegal structure (or symbol)"""
    counter = 0
    for i in dotBracket:
        if i=='(':
            counter+=1
        elif i==')':
            counter-=1
        elif i!='.': #illegal symbol
            return False
        if counter < 0: #unbalanced structure
            return False
    if counter!= 0:
        return False #unbalanced structure
    return True


def dotBracketToMountain(dotBracket):
    """Vienna dotbracket to mountain representation
    e.g. "..(((.....))).." -> [0, 0, 1, 2, 3, 3, 3, 3, 3, 3, 2, 1, 0, 0, 0]"""
    assert isValidDotBracket(dotBracket) == True
    counter = 0
    val = list()
    for i in dotBracket:
        if(i=='('):
            counter += 1
        elif(i==')'):
            counter -= 1
        val.append(counter)
    return val


def dotBracketToBPSet(dotBracket):
    """Vienna dotbracket to base pair set (sorted list by first base of the pair)
    "((..))" -> [(1,6), (2,5)]"""
    bpset= list()
    accumulator = list()
    count = 1 #1 indexed
    for i in dotBracket:
        if (i == '('):
            accumulator.append(count)
        elif(i == ')'):
            bpset.append((accumulator.pop(), count))
        count += 1
    bpset.sort()
    return bpset



def mountainDistance(mountain1, mountain2):
    """lp1 mountain distance on two mountains representation of same length
    e.g. [1,2,2,2,1], [1,2,3,2,1] = 1"""
    assert len(m1) == len(m2)
    def absdiff(x):
        """absolute difference, applied over a zipped array"""
        return abs(x[0] - x[1])
    return sum(map(lambda x:absdiff(x), zip(m1, m2)))



def basePairSetDistance(bp1, bp2):
  """naive base pair distance (cardinality of symmetric difference, |(A\B)U(B\A)|)"""
  return len((set(bp1).symmetric_difference(set(bp2))))




def toBPSeq(rnaSequence, dotBracket):
    """outputs RNA sequence and structure to bpseq format
    index base paired (0->unpaired)
    1 C 0
    2 C 9
    3 U 8
    4 G 0
    5 A 0
    6 A 0
    7 C 0
    8 A 3
    9 G 2"""
    assert isRNA(rnaSequence) == True
    assert isValidDotBracket(dotBracket) == True
    assert len(rnaSequence) == len(dotBracket)
    basePairs = dotBracketToBPSet(dotBracket)
    result = list() #(Int, Char, Int)
    result.append("header")
    for (i, bp) in enumerate(rnaSequence):
        result.append( (i+1, bp, 0))
    for (bp1, bp2) in basePairs:
        result[bp1] = (result[bp1][0], result[bp1][1], bp2)
        result[bp2] = (result[bp2][0], result[bp2][1], bp1)
    return "\n".join(map(lambda x: str(x[0])+" "+str(x[1])+ " "+ str(x[2]), result[1:]))



def getStems(dotBracket):
    """gets the stems from the dotBracket
    ([opening], [closing], dict of pairs"""
    assert isValidDotBracket(dotBracket) == True
    list_opener = []
    stems = []
    list_stem_end = []
    i = 0
    # separate into stems
    while(i <= len(dotBracket)-1):
        #add to opening list
        if(dotBracket[i] == '('):
            list_opener.append(i)
        #find the closing in the opening list
        elif(dotBracket[i] == ')'):
            stem = ([], [], dict())
            while(i <= len(dotBracket)-1):
                if(dotBracket[i] == ')'):
                    print(list_opener)
                    opener = list_opener.pop()
                    stem[0].append(opener)
                    stem[1].append(i)
                    stem[2][opener] = i
                    if((not len(list_opener)==0) and (list_opener[-1] in list_stem_end)):
                        list_stem_end.append(list_opener[-1])
                        break
                elif(dotBracket[i] =='('):
                    if (not len(list_opener)==0):
                        list_stem_end.append(list_opener[-1])
                    i -= 1
                    break
                i += 1
            stems.append(stem)
        i += 1
    return stems



#def RNAshapes(dotBracket)
  ##computes RNA abstract shapes level 1, 3 and 5 for the given dotBracket string

  ##get the stems
  #stems = getStems(dotBracket)

  ## build the level1 for each stems
  #range_occupied = {}
  #dict_lvl1 = Dict()
  #for stem in stems
    #range_open  = collect([ (minimum(stem[0])) : (maximum(stem[0])) ])
    #range_close = collect([ (minimum(stem[1])) : (maximum(stem[1])) ])
    #range_occupied = vcat(range_occupied, range_open, range_close)

    #temp_lvl1_open = ""
    #temp_lvl1_close = ""
    #last_opener = None
    #last_closer = None

    #for opener in sort(stem[0])
      #if last_opener == None
        #temp_lvl1_open = string(temp_lvl1_open, "[")
        #temp_lvl1_close = string("]", temp_lvl1_close)
      #else
        #if abs(opener - last_opener) != 1
          #temp_lvl1_open = string(temp_lvl1_open, "_")
        
        #if abs(stem[2][opener] - last_closer) != 1
          #temp_lvl1_close = string("_", temp_lvl1_close)
        
        #if (swith(temp_lvl1_open , "_")) || (beginswith(temp_lvl1_close, "_"))
          #temp_lvl1_open = string(temp_lvl1_open, "[")
          #temp_lvl1_close = string("]", temp_lvl1_close)
        
      
      #last_opener = opener
      #last_closer = stem[2][opener]
    

    #dict_lvl1[ minimum(stem[0]) ] = {"elem" => temp_lvl1_open,  "lvl5" => "["}
    #dict_lvl1[ minimum(stem[1]) ] = {"elem" => temp_lvl1_close, "lvl5" => "]"}
    #println(dict_lvl1)
  

  ##assemble level1
  #level1 = ""
  #level5 = ""

  #for i= 1:len(dotBracket)
    #if i in keys(dict_lvl1)
      #level1 = string(level1, dict_lvl1[i]["elem"])
      #level5 = string(level5, dict_lvl1[i]["lvl5"])
    

    #if dotBracket[i] == '.' && (! swith(level1, "_")) && (!(i in range_occupied))
      #level1 = string(level1, "_")
    
  
  #println("level 5 = $level5")
  #level1 = replace(level1, "[_]", "[]")
  #level1 = replace(level1, " ", "")
  #level3 = replace(level1, "_", "")

  ##particular case
  #if(level5 == "")
    #level5 = "_"
    #level3 = "_"
  
  #return (level5, level3, level1)




from RNA_2D import *
from zhangShasha import *


def buildStem(n):
    """builds a straight stem of length n"""
    assert n>0
    root = Node(None)
    position = root
    for i in range(0, n-1):
        child = Node(position)
        position = child
    return root


def dotBracketToTree(dot_bracket):
    """creates a abstract shape base pair tree from the Vienna dot bracket"""
    assert isValidDotBracket(dot_bracket)
    stems = getStems(dot_bracket)
    index = len(dot_bracket)
    root = Node(None)
    stack = [root]

    abstract_shape_5 = []
    for stem in stems:
        abstract_shape_5.append(('o', stem[0][-1], len(stem[0])))
        abstract_shape_5.append(('c', stem[1][-1]))
    abstract_shape_5.sort()

    for s in abstract_shape_5:
        if s[0] == 'o':
            stack[-1].append(buidStem(s[2]))
            

    return root


#function dotBracketToShapeTree{S<:String}(dotBracket::S)
  ##Vienna dot bracket to lvl5 shape tree
  #@assert isValidDotBracket(dotBracket) == true
  #stems = sort(getStems(dotBracket), by = x->minimum(x[1]))
  #leftRight = (Int, Int, Dict{Int, Int})[]
  #for stem in stems
    #push!(leftRight, (minimum(stem[1]), maximum(stem[2]), stem[3]))
  #end

  #root = shape(0, length(dotBracket)+1, Dict{Int, Int}())
  #position = root
  #closing = Int[]
  #i = 1
  #while length(leftRight) != 0
    ##opening case
    #if leftRight[1][1] == i
      #stem = shift!(leftRight)
      #push!(closing, stem[2])
      #child = shape(stem[1], stem[2], stem[3], shape[], position)
      #push!(position.children, child)
      #position = child #go down

    ##closing case
    #elseif i in closing
      #position = position.parent #go up
    #end
    #i+=1
  #end
  #root
#end
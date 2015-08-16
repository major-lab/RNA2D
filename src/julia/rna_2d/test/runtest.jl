#unit tests for the RNA_2D module

using Base.Test

function test_rna2Dstructure()
  a = rna2Dstructure("(.)(((((....)))))", id="1")
  b = rna2Dstructure("(.)(.)(...........)", id="2", energy=-42.0)
  c = rna2Dstructure("(.)")
  return true
end


function randomDotBracket()
  #helper method
  #generate random valid dot bracket
  #choice of three moves
  # 1- (
  # 2- )
  # 3- .
  opening = ['(', '.', '.']
  closing = [')', '(', '.','.']
  function addSymbol(choices, values, stack)
    sym = choices[rand(1:length(choices))]
    if sym == '('
      push!(values, sym)
      return stack + 1
    elseif sym == ')' && stack != 0
      push!(values, sym)
      return stack -1
    elseif sym == '.'
      push!(values, sym)
    else return -1
    end
    return stack
  end

  partialAddSymbol = s->addSymbol(s, val, stack)

  stack = 0
  val = Char[]
  stack = partialAddSymbol(opening)

  while true && length(val) < 40
    if val[end] == '('
      stack = partialAddSymbol(opening)
    else #symbol is either ')' or '.'
      stack = partialAddSymbol(closing)
      if stack == -1
        return CharString(val)
      end
    end
  end

  #just to avoid the problem of ()
  push!(val, '.')
  while stack > 0
    push!(val, ')')
    stack -= 1
  end
  return CharString(val)
end



function randomDotBracketPlus()
  #generate non empty dotbrackets (ie. not "." or ".."...)
  x = randomDotBracket()
  while true
    for i in x
      if i !='.'
        return x
      end
    end
    x = randomDotBracket()
  end
end

function test_isValidDotBracket1()
  @test isValidDotBracket("((((.)))") == false #missing brackets on the right
  @test isValidDotBracket("(((.))))") == false #missing brackets on the left
end


function test_isValidDotBracket2(n::Int)
  @assert n > 0
  for i = 1:n
    @test isValidDotBracket(randomDotBracket())==true
  end
  return true
end


function test_RNAshapes(n::Int)
  #use only on computers where RNAshapes is installed
  @assert n > 0
  for i = 1:n
    dotB = randomDotBracket()
    t5 = chomp(readall(`RNAshapes -D $dotB -t5`))
    t3 = chomp(readall(`RNAshapes -D $dotB -t3`))
    t1 = chomp(readall(`RNAshapes -D $dotB -t1`))
    result = RNAshapes(dotB)
    @test t5 == result[1]
    @test t3 == result[2]
    @test t1 == result[3]
  end
  println("RNAshapes                       [OK]")
end



function test_hausdorffDistance(n::Int)
  @assert n>0
  #simple debug example
  S1 = "........((((...))))."
  S2 = ".......((((...)))).."

  B1 = dotBracketToBPSet(S1)
  B2 = dotBracketToBPSet(S2)

  @test hausdorffDistance(B1,B2) == 1

  for i = 1:n
    a = dotBracketToBPSet(randomDotBracketPlus())
    b = dotBracketToBPSet(randomDotBracketPlus())
    hausdorffDistance(a,b)
  end
end

function test_dotBracketToShapeTree(n::Int)
  #
  @assert n>0
  for i = 1:n
    struct = randomDotBracketPlus()
    @test shapeLvl5Annotated(struct)[3] == shapeTreeToString(dotBracketToShapeTree(struct))
  end
end

function test_all()
  println("")
  test_rna2Dstructure()
  println("structure constructor           [OK]")
  test_isValidDotBracket1()
  test_isValidDotBracket2(10000)
  println("dot bracket verification        [OK]")
  test_hausdorffDistance(100)
  println("hausdorff distance              [OK]")
  test_dotBracketToShapeTree(100)
  println("shape tree                      [OK]")
  println("")
  return true
end


test_all()

#unit tests for the RNA_2D module


using Base.Test

require("../src/RNA_2D.jl")


function test_structure()
  a = RNA_2D.structure("(.)(((((....)))))", id=1)
  b = RNA_2D.structure("(.)(.)(...........)", id="2", energy=-42.0)
  c = RNA_2D.structure("(.)")
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

function test_testDotBracket1()
  @test RNA_2D.testDotBracket("((((.)))") == false #missing brackets on the right
  @test RNA_2D.testDotBracket("(((.))))") == false #missing brackets on the left
end


function test_testDotBracket2(n::Int)
  @assert n > 0
  for i = 1:n
    @test RNA_2D.testDotBracket(randomDotBracket())==true
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
    result = RNA_2D.RNAshapes(dotB)
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

  B1 = RNA_2D.dotBracketToBPSet(S1)
  B2 = RNA_2D.dotBracketToBPSet(S2)

  @test RNA_2D.hausdorffDistance(B1,B2) == 1

  for i = 1:n
    a = RNA_2D.dotBracketToBPSet(randomDotBracketPlus())
    b = RNA_2D.dotBracketToBPSet(randomDotBracketPlus())
    RNA_2D.hausdorffDistance(a,b)
  end
end


function test_all()
  println("")
  test_structure()
  println("structure constructor           [OK]")
  test_testDotBracket1()
  test_testDotBracket2(10000)
  println("dot bracket verification        [OK]")
  test_hausdorffDistance(100)
  println("hausdorff distance tested       [OK]")
  println("")
  return true
end


test_all()



require("../utility/fastaReader.jl")
require("../../src/RNA_2D.jl")


data = fastaRead("data.txt")

allData = (String, String)[]
for (name, structs) in data
  for struct in structs
    push!(allData, (string(name), struct))
  end
end

lvl5s = map(x->(x[1], x[2], RNA_2D.shapeLvl5Annotated(x[2])[3]), allData)


annotatedLvl5ToStruct = Dict{String, Vector{(String, String)}}()

for (name, struct, shapeLvl5) in lvl5s
  annotatedLvl5ToStruct[shapeLvl5] = push!(get(annotatedLvl5ToStruct, shapeLvl5, (String, String)[]), (name, struct))
end


rm("examples.txt")
f = open("examples.txt","w")
close(f)
for (shape, structs) in annotatedLvl5ToStruct
  f = open("examples.txt", "a")
  println(f, shape)
  println(f, structs)
  println(f, "")
  close(f)
end



def fastaRead(fileName):
    """reads a fasta file and returns Vector{(String, Vector{String})}"""
    f = open(fileName, "r")
    lines = f.readlines()
    print(len(lines))
    f.close()

    result = []
    name = ""
    data = []
    for line in lines:
        if line.startswith(";"):
            continue
        elif line.startswith(">"):
            result.append((name, data))
            name = str(line.split(">")[1]).rstrip()
            data =  []
        elif line != "\n":
            data.append(line.rstrip())
    print(len(data))
    result.append((name, data))
    return result[1:]

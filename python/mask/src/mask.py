#balanced mask conversion functions


#pdb2db format (input)
    # X  no information
    # .  unpaired
    # () base pair

#rmdetect format (input)
    # .  no information
    # x  unpaired
    # () base pair


#RNAFold format (same as rmdetect)
    # .  no information
    # x  unpaired
    # () base pair


#RNAWolf format (same as rmdetect)
    # .  no information
    # x  unpaired
    # () base pair

#flashfold format
    # x  no information
    # .  unpaired
    # () base pair


#RNAStructure
#Folding constraints are saved in plain text with a CON extension.
#These can be hand edited. For multiple entries of a specific type
#of constraint, entries are each listed on a separate line.
#Note that all specifiers, followed by "-1" or "-1 -1", are expected by
#RNAstructure. For all specifiers that take two arguments, it is
#assumed that the first argument is the lower base pair number.

##Example
    #DS:
    #15
    #25
    #76
    #-1
    #SS:
    #17
    #18
    #20
    #35
    #-1
    #Mod:
    #2
    #15
    #-1
    #Pairs:
    #16 26
    #-1 -1
    #FMN:
    #-1
    #Forbids:
    #15 27
    #-1 -1

    #XA: Nucleotides that will be double-stranded
    #XB: Nucleotides that will be single-stranded (unpaired)
    #XC: Nucleotides accessible to chemical modification
    #XD1, XD2: Forced base pairs
    #XE: Nucleotides accessible to FMN cleavage
    #XF1, XF2: Prohibited base pairs


import copy


INPUT_STYLES = ["std", "rmdetect"]
OUTPUT_STYLES = ["flashfold", "rnastructure", "rnawolf", "rnafold"]


def isValidMask(mask):
    """checks validity of balanced mask"""
    opening = []
    good = True
    for i in mask:
        if(i == "("):
            opening.append(i)
        elif(i==")"):
            #unbalanced ")"
            if len(opening) == 0:
                good = False
                break
            else:
                opening.pop()
        #invalid character
        elif(not (i in ['X', 'x','.'])):
            good = False
            break
    #unbalanced "("
    if len(opening) != 0:
        good = False
    return good


def toCommonRepr(mask, inputStyle):
    """transform all masks to RNAFold representation"""
    mask = copy.copy(mask)
    #use RNAfold as internal representation
    if inputStyle == "rmdetect":
        return mask

    elif inputStyle == "std":
        mask = mask.replace("X", "k")
        mask = mask.replace(".", "x")
        mask = mask.replace("k", ".")
    return mask


def convertMask(inputMask, output_format):
    """ convert input mask to the specified format
    the input mask must be already converted to internal representation"""
    assert output_format in OUTPUT_STYLES
    outputMask = copy.copy(inputMask)

    #internal representation
    # .  no information
    # x  unpaired
    # () base pair

    if output_format == "flashfold":
        #flashfold format
        # x  no information
        # .  unpaired
        # () base pair
        outputMask = outputMask.replace("x", "d")
        outputMask = outputMask.replace(".", "x")
        outputMask = outputMask.replace("d", ".")

    elif output_format == "rnastructure":
        #convert to numbers and to their ungodly notation
        opening = []
        pairs = []
        unpaired = []
        for (i,e) in enumerate(outputMask):
            if e == '(':
                opening.append(i+1)
            elif e == ')':
                pairs.append((opening.pop(), i+1))
            elif e == "x":
                unpaired.append(i+1)
        pairs.sort()

        #XA: Nucleotides that will be double-stranded
        DS = "DS:\n-1\n"
        #XB: Nucleotides that will be single-stranded (unpaired)
        SS = "SS:\n"
        for i in unpaired:
            SS += str(i)
            SS += "\n"
            SS += "-1\n"
        #XC: Nucleotides accessible to chemical modification
        MOD = "Mod:\n-1\n"
        #XD1, XD2: Forced base pairs
        PAIRS = "Pairs:\n"
        for i in pairs:
            PAIRS += str(i[0])
            PAIRS += " "
            PAIRS += str(i[1])
            PAIRS += "\n"
            PAIRS += "-1 -1\n"
        #XE: Nucleotides accessible to FMN cleavage
        FMN = "FMN:\n-1\n"
        #XF1, XF2: Prohibited base pairs
        FORBIDS = "Forbids:\n-1 -1\n"
        outputMask = DS + SS + MOD + PAIRS + FMN + FORBIDS
    return outputMask


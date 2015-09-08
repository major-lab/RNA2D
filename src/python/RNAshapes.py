"""RNAshapes related functions"""


def get_stems(structure):
    """extract stems from the structure"""
    stems = []
    list_opener = []
    print structure

    i = 0
    list_stem_start = []

    # separate into stems
    while i < len(structure):

        if structure[i] == "(":
            list_opener.append(i)
            if not list_stem_start:
                list_stem_start.append(i)
        elif structure[i] == ")":
            current_stem = [[], [], []]
            while i < len(structure):
                if structure[i] == ")":
                    closer = list_opener.pop(-1)
                    current_stem[0].append(closer)
                    current_stem[1].append(i)
                    current_stem[2].append((closer, i))
                    if closer in list_stem_start:
                        break
                elif structure[i] == "(":
                    list_stem_start.append(i)
                    i -= 1
                    break
                i += 1
            stems.append(current_stem)
        i += 1
    return stems


def dot_bracket_to_abstract_shape(structure):
    """Converts a Vienna dot-bracket structure into
       its corresponding abstract shape as defined in RNAshapes.
       Written by Stephen Leong Koan, IRIC, 2013"""
    # the 3 levels we use are the following
    # 1: Most accurate - all loops and all unpaired
    # 3: Nesting pattern for all loop types but no unpaired regions
    # 5: Most abstract - helix nesting pattern and no unpaired regions

    stems = get_stems(structure)

    # build the level 1 for each stems
    range_occupied = []
    dict_lvl1 = dict()
    for stem in stems:
        range_open = range(min(stem[0]), max(stem[0])+1)
        range_close = range(min(stem[1]), max(stem[1])+1)
        range_occupied.extend(range_open + range_close)

        temp_lvl1_open = " "
        for i in range_open:
            if structure[i] == "(" and temp_lvl1_open[-1] != "[":
                temp_lvl1_open += "["
            elif structure[i] == "." and temp_lvl1_open[-1] != "_":
                temp_lvl1_open += "_"

        temp_lvl1_close = " "
        for i in range_close:
            if structure[i] == ")" and temp_lvl1_close[-1] != "]":
                temp_lvl1_close += "]"
            elif structure[i] == "." and temp_lvl1_close[-1] != "_":
                temp_lvl1_close += "_"

        while temp_lvl1_open.count("[") < temp_lvl1_close.count("]"):
            temp_lvl1_open = "[" + temp_lvl1_open

        while temp_lvl1_open.count("[") > temp_lvl1_close.count("]"):
            temp_lvl1_close += "]"

        dict_lvl1[str(min(stem[0]))] = temp_lvl1_open
        dict_lvl1[str(min(stem[1]))] = temp_lvl1_close

    # assemble level 1
    level_1 = ""
    for i, element in enumerate(structure):
        level_1 += dict_lvl1.get(str(i), "").strip()
        if element == "." and level_1[-1] != "_" and not i in range_occupied:
            level_1 += "_"

    print level_1
    level_1 = level_1.replace("[_]", "[]")

    # from level 1, build level 3 (remove unpaired symbols)
    level_3 = level_1.replace("_", "")
    level_3 = level_3.replace(" ", "")

    # from level 3, build level 5 by removing stems with bulges
    level_5 = level_3
    while level_5.count("[[]]") > 0:
        level_5 = level_5.replace("[[]]", "[]")

    return (level_5, level_3, level_1)



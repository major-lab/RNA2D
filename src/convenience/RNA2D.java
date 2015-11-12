package convenience;


import core.representations.AbstractShapes;
import core.representations.GranularTree;
import core.verification.Verifier;

import java.util.ArrayList;

/**
 * Holds some of the more simple and useful method calls which can be called when used as library.
 */
public final class RNA2D {


    //region Input checking
    public static boolean isValidDotBracket(String dotBracket)
    {
        return Verifier.isValidRNA2DStructure(dotBracket);
    }



    public static boolean isValidRNASequence(String rnaSequence)
    {
        ArrayList<Character> allowedSymbols = new ArrayList<>();
        allowedSymbols.add('A');
        allowedSymbols.add('U');
        allowedSymbols.add('G');
        allowedSymbols.add('C');
        return Verifier.isValidCanonicalRNASequence(rnaSequence, allowedSymbols);
    }
    //endregion



    //region Representation conversion


    public static String dotBracketToAbstractShape(String dotBracket, int shapeLevel)
    {
        return AbstractShapes.dotBracketToAbstractShape(dotBracket, shapeLevel);
    }


    public static String dotBracketToGranularTree(String dotBracket, int granularity)
    {
        return GranularTree.dotBracketToGranularTree(dotBracket, granularity);
    }

    //endregion



}

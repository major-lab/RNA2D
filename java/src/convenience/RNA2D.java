package convenience;


import verification.Verifier;

/**
 * Holds some of the more simple and useful method calls.
 */
public final class RNA2D {

    public static boolean isValidDotBracket(String dotBracket)
    {
        return Verifier.isValidRNA2DStructure(dotBracket);
    }




}

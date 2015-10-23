package verification;


import java.util.ArrayList;

/**
 * Holds verification functions for sequence, structure, file formats and such.
 */
public final class Verifier {


    //region INPUT CHECKERS
    /**
     * verifies that the arguments given to the constructor build a legal tree
     * @param dotBracket string representation, usually Vienna dot bracket
     * @return true if a valid tree is build from the arguments
     */
    public static boolean isValidRNA2DStructure(String dotBracket)
    {
        int counter = 0;
        for (char c : dotBracket.toCharArray())
        {
            if (c == '(')        // stack
            {
                counter += 1;
            }
            else if (c == ')')   // unstack
            {
                counter -= 1;
            }
            else if (c != '.')   // illegal character
            {
                return false;
            }
            if (counter < 0)     // left unbalanced
            {
                return false;
            }
        }
        return counter == 0;
    }


    /**
     * verifies if the RNA sequence given is composed of AUGC
     * @param sequence RNA sequence
     * @return true if it is a valid sequence of AUGC, false otherwise
     */
    public static boolean isValidCanonicalRNASequence(String sequence, ArrayList<Character> validSymbols)
    {
        boolean isValid = true;
        for (char c : sequence.toUpperCase().toCharArray())
        {
            if (!(c == 'A' || c =='U' || c == 'G' || c == 'C'))
            {
                isValid = false;
                break;
            }
        }
        return isValid;
    }
    //endregion
}

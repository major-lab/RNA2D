package core.verification;


import java.util.ArrayList;

/**
 * Holds core.verification functions for sequence, structure, file formats and such.
 */
public final class Verifier {



    /**
     * verifies that the arguments given to the constructor build a legit secondary
     * structure in Vienna dot-bracket format
     * @param dotBracket string representation, usually Vienna dot bracket
     * @return true if the string represents a legal structure in Vienna dot-bracket format
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
     * verifies if the RNA sequence given is composed of valid symbols only
     * @param sequence RNA sequence
     * @return true if it is a valid sequence of AUGC, false otherwise
     */
    public static boolean isValidCanonicalRNASequence(String sequence, ArrayList<Character> validSymbols)
    {
        boolean isValid = true;
        for (char c : sequence.toUpperCase().toCharArray())
        {
            if (!(validSymbols.contains(c)))
            {
                isValid = false;
                break;
            }
        }
        return isValid;
    }




}

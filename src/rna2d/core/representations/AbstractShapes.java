package rna2d.core.representations;

import rna2d.core.datastructures.Node;
import rna2d.core.datastructures.OrderedRootedTree;
import rna2d.core.verification.Verifier;

import java.util.ArrayDeque;
import java.util.ArrayList;


/**
 * Converts Vienna dot-bracket structures to Abstract Shapes representation.
 * Currently only level 1-3-5 are implemented (2 and 4 might get done if needed).
 *
 * for review, please refer to "Abstract shapes of RNA, Nucleic Acids Research, 2004"
 */
public final class AbstractShapes{


    /**
     * remove stem nodes repetitions and convert to a single node instead e.g. ((())) -> ()
     * @param node start of the stem
     * @param nestingSymbol symbol used to represent nesting (usually '(')
     * @return wether or not stem removal was applied
     */
    private static boolean removeStem(Node<Character> node, char nestingSymbol)
    {   // to be used in a BFS traversal only
        if ( (node.getLabel() == nestingSymbol) && (node.getChildren().size() == 1) )
        {
            node.setChildren(node.getChildren().get(0).getChildren());
            return true;
        }
        else
        {
            return false;
        }
    }




    public static void removeAllStems(Node<Character> tree, char nestingSymbol)
    {
        ArrayDeque<Node<Character>> Q = new ArrayDeque<>();
        Q.addLast(tree);
        Node<Character> currentNode;

        boolean modified;
        while(!Q.isEmpty())
        {
            // dequeue
            currentNode = Q.pollFirst();

            // apply stem removing operation and check status
            modified = removeStem(currentNode, nestingSymbol);
            if (modified)
            {
                // requeue immediately
                Q.addFirst(currentNode);
            }
            else if (currentNode.getLabel() == nestingSymbol)
            {
                for (int i = 0; i != currentNode.getChildren().size(); ++i)
                {
                    Q.addLast( currentNode.getChildren().get(i));
                }
            }
        }
    }


    public static ArrayList<Character> preProcessDotBracket(String dotBracket)
    {
        ArrayList<Character> step1 = new ArrayList<>();
        char[] chars = dotBracket.toCharArray();
        char lastChar = 'a';
        for (char currentChar : chars)
        {
            if ( ! ((currentChar =='.') && (lastChar == currentChar)))
            {
                // add it
                step1.add(currentChar);
            }
            lastChar = currentChar;
        }

        // (.) . ()
        ArrayList<Character> step2 = new ArrayList<>();
        step2.add(step1.get(0));

        for(int i = 1; i != step1.size()-1; ++i)
        {
            if (!( (step2.get(step2.size() - 1) == '(') && (step1.get(i) == '.') && (step1.get(i+1) == ')') ))
            {
                step2.add(step1.get(i));
            }
        }
        step2.add(step1.get(step1.size() - 1));

        return step2;
    }


    /**
     * The actual dotbracket -> abstract shape converter
     * @param dotBracket input secondary structure
     * @param level level of the shape wanted
     * @return the shape of specified level for the secondary structure given
     * @throws IllegalArgumentException, in case of badly formated secondary structure input
     */
    public static String dotBracketToAbstractShape(String dotBracket, int level) throws IllegalArgumentException
    {
        if (!Verifier.isValidRNA2DStructure(dotBracket))
        {
            throw new IllegalArgumentException("input RNA structure is problematic: " + dotBracket);
        }

        if (!(level == 1 || level == 3 || level==5))
        {
            throw new IllegalArgumentException("Conversion to abstract shape level " + level + " is not implemented (only 1, 3 and 5)");
        }



        // pre-process the dot-bracket and convert it to tree representation
        ArrayList<Character> processed = preProcessDotBracket(dotBracket);

        OrderedRootedTree<Character> tree = new OrderedRootedTree<>(processed, '(', ')', '.');
        ArrayList<Node<Character>> subTrees = tree.getRoot().getChildren();



        //-------------------------------------------level 1
        // must remove nodes with single children (stems without branching)
        for (Node<Character> subRoot : subTrees)
        {
            removeAllStems(subRoot, '(');
        }
        String level1 = tree.toString().replace("(", "[").replace(")", "]").replace(".", "_");
        if (level == 1)
        {
            return level1;
        }


        //-------------------------------------------level 3
        // remove the '_'
        ArrayList<Character> level3 = new ArrayList<>();
        for (Character c: level1.toCharArray())
        {
            if (c != '_')
            {
                level3.add(c);
            }
        }
        if (level == 3)
        {
            StringBuilder builder = new StringBuilder();
            for (Character c: level3)
            {
                builder.append(c);
            }
            return builder.toString();
        }

        //-------------------------------------------level 5
        // same as for level 1 except it is applied on the level 3 string
        OrderedRootedTree<Character> tree2 = new OrderedRootedTree<>(level3, '[', ']', '_');

        ArrayList<Node<Character>> trees2 = tree2.getRoot().getChildren();
        for (Node<Character> n : trees2)
        {
            removeAllStems(n, '[');
        }
        return tree2.toString();
    }
}

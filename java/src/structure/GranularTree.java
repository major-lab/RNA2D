package structure;

import util.Node;
import util.OrderedRootedTree;
import verification.Verifier;

import java.util.ArrayList;
import java.util.LinkedList;


/**
 * Granular Tree representation of RNA secondary structure
 * =======================================================
 *
 *
 * Unpaired information is ignored (lost) and only base pairs are taken into account.
 *
 *
 * Basically the same as Shape level 5 but with stem length information conserved.
 * The encoding is variable. If the granularity is 1, then it corresponds to simply ignoring
 * unpaired nucleotides information. As the granularity grows, more and more information is lost
 * (each base pair represents the ceiling
 *
 * Lossy tree compression ((((..)))).(.) -> (())() if granularity == 2
 */
public final class GranularTree {


    /**
     * Vienna dot-bracket RNA structure to Granular Tree representation (also in Vienna dot-bracket)
     */
    public static String dotBracketToGranularTree(String dotBracket, int granularity) throws IllegalArgumentException{

        // some defensive programming
        if (!Verifier.isValidRNA2DStructure(dotBracket))
        {
            throw new IllegalArgumentException("input RNA structure is problematic: " + dotBracket);
        }
        if (granularity < 1)
        {
            throw new IllegalArgumentException("granularity should be greater than or equal to 1 (actual value is " + granularity + ")");
        }


        // first convert the structure to a base pair tree (by removing the '.' symbol)
        OrderedRootedTree basePairTree = new OrderedRootedTree(dotBracket.replace(".", ""), '(', ')', '.');


        LinkedList<Node<Character>> searchSpace = new LinkedList<>();
        ArrayList<Node<Character>> stemStarters = new ArrayList<>();
        for (Node<Character> node : basePairTree.getRoot().getChildren())
        {
            searchSpace.add(node);
        }

        // find the nodes who begin a stem
        while (searchSpace.size() > 0) {
            Node<Character> currentNode = searchSpace.poll();
            if (startsStem(currentNode, basePairTree.getRoot())) {

                stemStarters.add(currentNode);
            }
            for (Node<Character> children : currentNode.getChildren()) {
                searchSpace.add(children);
            }
        }

        // replace old stems by new stems of specified size based on the previous one's size
        // (that's the granular transformation)
        for (Node<Character> node : stemStarters)
        {
            // size of the new stem
            int newLength = (int) Math.ceil((double) stemLength(node) / (double) granularity);
            ArrayList<Node<Character>> lastChildren = lastNodeOfStem(node).getChildren();

            Node<Character> position = node;
            for (int i = 1; i < newLength; ++i)
            {
                position = position.getChildren().get(0);
            }

            Node<Character> child;
            while(position.getChildren() != lastChildren)
            {
                // remove unwanted nodes from the stem
                child = position.getChildren().get(0);
                // remove parent pointer
                child.setParent(null);
                // remove child pointer and link grand-child
                position.setChildren(child.getChildren());
                child.setChildren(null);

            }
        }
        return basePairTree.toString();
    }


    //region Helpers
    /**
     * verifies if a node starts a stem. to do so it must either have a single children or none
     * and it must have a parent that is a junction or no parent at all
     * @param node position in the tree
     * @return if the node starts a stem or not
     */
    private static boolean startsStem(Node<Character> node, Node<Character> artificialRoot)
    {
        boolean property1 = (node.getChildren().size() == 1 || node.getChildren().size() ==0);
        boolean property2 = (node.getParent() == artificialRoot || node.getParent().getChildren().size() > 1);
        return (property1 && property2);
    }


    private static int stemLength(Node<Character> position)
    {
        int stemLength = 1;
        while(position.getChildren().size() == 1)
        {
            stemLength +=1;
            position = position.getChildren().get(0);
        }
        return stemLength;
    }


    private static Node<Character> lastNodeOfStem(Node<Character> node)
    {
        Node<Character> position = node;
        while (position.getChildren().size() == 1)
        {
            position = position.getChildren().get(0);
        }
        return position;
    }
    //endregion

}

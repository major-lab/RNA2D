package rna2d.core.representations;

import rna2d.core.datastructures.Node;
import rna2d.core.datastructures.OrderedRootedTree;
import rna2d.core.verification.Verifier;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.regex.Pattern;

public class Shapiro {
    OrderedRootedTree<Character> tree;

    Shapiro(String dotBracket)
    {
        assert Verifier.isValidRNA2DStructure(dotBracket);
        ArrayList<Character> characters = new ArrayList<>();
        for(Character c: dotBracket.toCharArray())
        {
            characters.add(c);
        }
        OrderedRootedTree<Character> fullTree = new OrderedRootedTree<>(characters, '(', ')', '.');
        fullTree.changeLabels('(', 'P');
        fullTree.changeLabels('.', 'U');

        // go through the tree, changing the labels on the nodes
        // by breadth-first traversal
        ShapiroLabel(fullTree.getRoot());
        tree = fullTree;
    }



    /**
     * Return the match to a Shapiro label for a P-node (don't ever feed it a U-node).
     * Can be either one of the 6 following values
     * H: hairpin
     * I: internal node
     * B: bulge
     * M: multi-loop
     * R: helix (stem)
     * N: artificial root
     * @param position position node to match to a case
     * @return the character representing the label, one of the HIBMRN characters
     */
    private static char match(Node<Character> position)
    {
        assert position.getLabel() != 'U';
        Character value = ' ';
        if (position.getParent() == null)
        {
            value =  'N';
        }

        // construct a string of the children labels (used for matching functions)
        StringBuilder builder = new StringBuilder();
        for(Node<Character> child : position.getChildren())
        {
            builder.append(child.getLabel());
        }
        String childLabels = builder.toString();

        if(HCase(childLabels))
        {
            value =  'H';
        }
        if(ICase(childLabels))
        {
            value =  'I';
        }
        if(BCase(childLabels))
        {
            value =  'B';
        }
        if(MCase(childLabels))
        {
            value =  'M';
        }
        if (RCase(childLabels))
        {
            value =  'R';
        }
        return value;
    }


    /**
     * helix (stem) is characterized by a single P-node children
     * @param nodeChildrenLabels
     * @return
     */
    static boolean RCase(String nodeChildrenLabels)
    {
        return Pattern.compile("P").matcher(nodeChildrenLabels).matches();
    }

    /**
     * internal loop, characterized by a single P-node, with at least one U-node
     * on the left and right of the P-node
     * @param nodeChildrenLabels
     * @return
     */
    static boolean ICase(String nodeChildrenLabels)
    {
        return Pattern.compile("U+PU+").matcher(nodeChildrenLabels).matches();
    }


    /**
     * bulge
     * @param nodeChildrenLabels
     * @return
     */
    static boolean BCase(String nodeChildrenLabels)
    {

        Pattern pattern1 = Pattern.compile("U+P");
        Pattern pattern2 = Pattern.compile("PU+");
        return (pattern1.matcher(nodeChildrenLabels).matches() ||
                pattern2.matcher(nodeChildrenLabels).matches());
    }

    /**
     * hairpin
     * @param nodeChildrenLabels
     * @return
     */
    static boolean HCase(String nodeChildrenLabels)
    {
        return Pattern.compile("U*").matcher(nodeChildrenLabels).matches();
    }

    /**
     * multi-loop
     * @param nodeChildrenLabels
     * @return
     */
    static boolean MCase(String nodeChildrenLabels)
    {
        return nodeChildrenLabels.replace("U", "").length()>1;
    }


    /**
     * Relabel each node into a Shapiro Encoding
     * @param treeRoot root of the tree to relabel
     */
    public static void ShapiroLabel(Node<Character> treeRoot)
    {
        ArrayDeque<Node<Character>> Q = new ArrayDeque<>();
        Q.addLast(treeRoot);
        Node<Character> currentNode;
        while(!Q.isEmpty())
        {
            // dequeue
            currentNode = Q.pollFirst();

            // figure out the type of the node and relabel the node
            if (currentNode.getLabel() == 'P')
            {
                currentNode.setLabel(match(currentNode));
            }

            // enqueue the children of the currently used node
            for(Node<Character> child : currentNode.getChildren())
            {
                Q.addLast(child);
            }
        }
    }

}

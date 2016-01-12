package rna2d.core.datastructures;


import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;


/**
 * Ordered labeled tree used to represent both RNA abstract shapes
 * and Vienna dot-bracket (planar ordered labeled tree)
 */

public class OrderedRootedTree<T extends Comparable<T>> {

    private Node<T> artificialRoot;


    /**
     * Constructor
     * Vienna dot bracket symbols =  ( ) .
     * Abstract shapes symbols = [ ] _
     *
     * @param representation representation of the tree
     * @param nestingSymbol  symbol that causes nesting
     * @param closingSymbol  symbol that corresponds to going up in the tree
     * @param addNodeSymbol  symbol to add a node to the current node
     */
    public OrderedRootedTree(List<T> representation, T nestingSymbol, T closingSymbol, T addNodeSymbol) {

        // assign the string representation and remember the symbols
        // create rooted tree (with artificial root)
        artificialRoot = new Node<>(null, nestingSymbol);
        Node<T> position = artificialRoot;
        int index = 0;
        for (T c : representation) {
            if (c == nestingSymbol)       // create new node and position goes down
            {
                position = new Node<>(position, nestingSymbol);
                position.setIndex(index);
                index += 1;
            } else if (c == closingSymbol)  // position goes up
            {
                position = position.getParent();
            } else if (c == addNodeSymbol) // add unpaired node, position stays same
            {
                new Node<>(position, addNodeSymbol);
                position.setIndex(index);
                index += 1;
            }
        }
    }

    public OrderedRootedTree(Node<T> artificialRoot)
    {
        this.artificialRoot = artificialRoot;
    }


    /**
     * recursively go through the tree by post-order and add the labels to the list of labels
     *
     * @param position current node in the tree being traversed
     * @param labelsList list of the labels already traversed (to which labels are added)
     */
    private void getPostOrderLabels(Node<T> position, ArrayList<T> labelsList) {

        for(Node<T> child : position.getChildren())
        {
            getPostOrderLabels(child, labelsList);
        }
        labelsList.add(position.getLabel());
    }


    public String toString() {
        ArrayList<T> symbolList = new ArrayList<>();
        for (Node<T> position : artificialRoot.getChildren()) {
            getPostOrderLabels(position, symbolList);
        }
        StringBuilder builder = new StringBuilder(symbolList.size());
        for (T c : symbolList) {
            builder.append(c);
        }
        return builder.toString();
    }


    public void changeLabels(T originalLabel, T replacementLabel)
    {
        ArrayDeque<Node<T>> Q = new ArrayDeque<>();
        Q.addLast(artificialRoot);
        Node<T> currentNode;

        boolean modified;
        while(!Q.isEmpty())
        {
            // dequeue
            currentNode = Q.pollFirst();

            // relabel if necessary
            if (currentNode.getLabel().compareTo(originalLabel) == 0)
            {
                currentNode.setLabel(replacementLabel);
            }

            // enqueue the children of the current node
            for (Node<T> child : currentNode.getChildren())
            {
                Q.addLast(child);
            }
        }
    }


    public Node<T> getRoot() {
        return artificialRoot;
    }
}


package rna2d.core.io;

import com.sun.xml.internal.ws.addressing.ProblemAction;

import java.io.*;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.regex.Pattern;


/**
 * Container of readers used for RNA input files format
 */
public final class Readers {

    /**
     * figure out where the dot bracket ends on a given line
     * usually formatted like (((..))) -1.2, with structure and energy
     * @param line the line to extract the position from
     * @return where the line should be cut to take only the dotbracket
     */
    private static int getSuboptLength(String line) {
        char[] chars = line.toCharArray();
        int i = 0;
        for (char c : chars) {
            if (c != '(' && c != ')' && c != '.') {
                return i;
            } else {
                i += 1;
            }
        }
        return line.length();
    }


    /**
     * read marna file format with suboptimal structures
     * we only take suboptimal structures as data, rest is ignored
     * @param fileName input file path
     * @return the many lists of suboptimal structures, no sequence, no energy
     */
    public static ArrayList<ArrayList<String>> readMarnaFile(String fileName){
        ArrayList<ArrayList<String>> data = new ArrayList<>();
        ArrayList<String> subopts = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(new FileReader(fileName))) {
            for (String line; (line = br.readLine()) != null; ) {
                // process the line

                // figure out where we are
                if (line.startsWith(">") && (subopts.size() != 0)) {
                    // new subopts are coming, add old ones to the data
                    data.add(subopts);
                    subopts = new ArrayList<>();
                } else if (line.startsWith("(") || line.startsWith(")") || line.startsWith(".")) {
                    // read the new suboptimal
                    // must keep only the structure (first part)
                    subopts.add(line.substring(0, getSuboptLength(line)));
                }
            }
            // line is not visible here.
            if (subopts.size() != 0) {
                data.add(subopts);
            }
        }
        catch (FileNotFoundException e) {
            System.out.println("Could not find specified file (" + fileName + ")");
        }catch (IOException e) {
            e.printStackTrace();
        }
        return data;
    }
}



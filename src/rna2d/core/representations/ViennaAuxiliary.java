package rna2d.core.representations;

public class ViennaAuxiliary {

    private final String string;

    public ViennaAuxiliary(String structure) {
        this.string = b2aux(structure);
    }


    public String toString() {
        return string;
    }


    public String getString() {
        return this.string;
    }

    private static String b2aux(String structure) {
        int[] match_paren;
        int i, o, p;
        char[] string;

        string = structure.toCharArray();

        // (char *) space(sizeof(char)*(strlen(structure)+1));
        match_paren = new int[structure.length() / 2 + 1]; // (short *) space(sizeof(short)*(strlen(structure)/2+1));


        i = o = 0;
        while (i < string.length) {
            switch (string[i]) {
                case '.':
                    break;

                case '(':
                    o += 1;
                    match_paren[o] = i;
                    break;

                case ')':
                    p = i;
                    //TODO: make this more beautiful
                    while ((p < string.length - 1) && (string[p + 1] == ')') && (match_paren[o - 1] == (match_paren[o] - 1))) {
                        p += 1;
                        o -= 1;
                    }
                    string[p] = ']';
                    i = p;
                    string[match_paren[o]] = '[';
                    o -= 1;
                    break;

                default:
                    throw new IllegalArgumentException("Junk in structure at aux_structure\n");
            }

            i += 1;
        }
        StringBuilder builder = new StringBuilder();
        for (char c : string) {
            builder.append(c);
        }
        return builder.toString();
    }


    public static void main(String[] args) {
        String struct = b2aux(".((..(((...)))..((..)))).");
        System.out.println(struct);
    }
}

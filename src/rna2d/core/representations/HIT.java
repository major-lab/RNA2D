package rna2d.core.representations;



/**
 * Homeomorphic Irreducible Tree.
 */
public class HIT {
    private final String string;


    public HIT(String structure)
    {
        this.string = b2HIT(structure);
    }


    public static String b2HIT(String structure)
    {

        int i, u, p, l;

        StringBuilder HITBuilder = new StringBuilder();

        char[] string = new ViennaAuxiliary(structure).toString().toCharArray();

        HITBuilder.append("(");

        i=p=u=0;

        while (i < string.length) {
            switch(string[i]) {
                case '.':
                    u+=1;
                    break;
                case '[':
                    if (u>0){
                        HITBuilder.append("(U");
                        HITBuilder.append(u);
                        HITBuilder.append(")");
                        u=0;
                    }
                    HITBuilder.append("(");
                    break;
                case ')':
                    if (u>0) {
                        HITBuilder.append("(U");
                        HITBuilder.append(u);
                        HITBuilder.append(")");
                        u=0;
                    }
                    p+=1;
                    break;
                case ']':
                    if (u>0) {
                        HITBuilder.append("(U");
                        HITBuilder.append(u);
                        HITBuilder.append(")");
                        u=0;
                    }
                    HITBuilder.append("(P");
                    HITBuilder.append(p + 1);
                    HITBuilder.append(")");
                    p=0;
                    break;
            }
            i+=1;
        }
        if (u>0) {
            HITBuilder.append("(U");
            HITBuilder.append(u);
            HITBuilder.append(")");
        }
        HITBuilder.append("R)");

        return HITBuilder.toString();
    }


    public static void main(String[] args)
    {
        String struct = ".((..(((...)))..((..)))).";
        System.out.println(b2HIT(struct));
    }
}

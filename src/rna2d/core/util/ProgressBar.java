package rna2d.core.util;

public class ProgressBar {
    private String processName;
    private int barLength;
    
    
    public ProgressBar(String processName_, int barLength) {
        processName = processName_;
        this.barLength = barLength;
    }


    public void update(double percentage) {
        // displays the current progress of the process
        assert (percentage >= 0.);
        assert (percentage <= 1.);

        int progressLength = (int) (barLength * percentage);
        System.err.print("[");
        for (int i = 0; i < barLength; ++i) {
            if (i <= progressLength)
                System.err.print("#");
            else
                System.err.print(" ");
        }
        System.err.print("] " + (int)(percentage * 100.) + "% " + processName + "\r");
        System.err.flush();
    }


    /**
     *  called after last iteration, displays 100% success
     */
    public void clean() {
        this.update(1.);
        System.err.println();
        System.err.flush();
    }
}
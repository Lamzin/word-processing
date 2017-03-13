public class ParaphraseTest {

    // some magic values
    static double dSLD = 0.8f;

    //
    public Sentence A;
    public Sentence B;
    public boolean isParaphrase;

    public String source;

    // features
    public double SLD;   // [S]entence [L]ength [D]ifference
    public double[] NGCN; // [N]-[G]rams [C]omparing – comparison of unigrams, bigrams, and trigrams

    public ParaphraseTest(String source) {
        this.source = source;
        this.parseSource();
    }

    public ParaphraseTest(Sentence A, Sentence B, boolean isParaphrase) {
        this.A = A;
        this.B = B;
        this.isParaphrase = isParaphrase;
    }

    private void parseSource() {
        String[] rows = this.source.split("\t");
        this.isParaphrase = rows[0].equals("1");

        this.A = new Sentence(rows[1], rows[3]);
        this.B = new Sentence(rows[2], rows[4]);
    }

    public String toString() {
        return String.format(
                "\n{\n\tA: %s\tB: %s\tisParaphrase: %d\n}\n",
                this.A.toString(),
                this.B.toString(),
                this.isParaphrase ? 1 : 0
        );
    }

    private void calculateFeatures() {
        this.calculateSLD();
        this.calculateNGCN();
    }

    // [S]entence [L]ength [D]ifference – comparison of lexeme quantity in sentences
    private void calculateSLD() {
        this.SLD = 1.0f / Math.pow(dSLD, Math.abs(this.A.words.length) - Math.abs(this.B.words.length));
    }

    // [N]-[G]rams [C]omparing – comparison of unigrams, bigrams, and trigrams
    private void calculateNGCN() {
        NGCN = new double[4];
        for (int i = 1; i < 4; i++) {
            NGrams NGramsA = new NGrams(i, this.A.words);
            NGrams NGramsB = new NGrams(i, this.B.words);
            this.NGCN[i] =
                    (double)(NGramsA.intersection(NGramsB).getNgramsCount()) /
                    (double)(NGramsA.getNgramsCount());
        }
    }

}

import java.util.Arrays;
import java.util.Map;
import java.util.HashMap;


public class NGrams {

    private int N;
    private String[] words;
    private Map<String, NGram> ngrams;

    public NGrams(int N, String[] words) {
        this.N = N;
        this.words = words;
        this.build();
    }

    public NGrams(int N, Map<String, NGram> ngrams) {
        this.N = N;
        this.ngrams = ngrams;
    }

    private void build() {
        this.ngrams = new HashMap<String, NGram>();
        for (int i = 0; i < words.length - this.N; i++) {
            NGram n = new NGram(Arrays.copyOfRange(this.words, i, i + this.N));
            this.ngrams.put(n.getHash(), n);
        }
    }

    public Map<String, NGram> getNgrams() {
        return new HashMap<String, NGram>(this.ngrams);
    }

    public int getNgramsCount() {
        return this.ngrams.size();
    }

    public NGrams intersection(NGrams B) {
        Map<String, NGram> result = new HashMap<String, NGram>(this.getNgrams());
        result.keySet().retainAll(B.getNgrams().keySet());
        return new NGrams(this.N, result);
    }

}

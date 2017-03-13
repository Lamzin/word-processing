import java.util.Arrays;

public class Sentence {

    public String id;
    public String text;
    public String source;
    public String[] words;

    public Sentence(String source) {
        this.source = source;
        this.parseSource();
        this.getWords();
    }

    public Sentence(String id, String text) {
        this.id = id;
        this.text = text;
        this.getWords();
    }

    private void parseSource() {
        String[] rows = this.source.split("\t");
        this.id = rows[0];
        this.text = rows[1];
    }

    private void getWords() {
        this.words = this.text.replaceAll("[!?,\":.]", "").split("\\s+");
    }

    public String toString() {
        return String.format(
                "\n{\n\tsource: %s,\n\tid: %s\n\ttext: %s\n\twords: %s\n}\n",
                this.source,
                this.id,
                this.text,
                Arrays.toString(this.words)
        );
    }

}

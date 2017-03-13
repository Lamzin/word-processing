import java.security.MessageDigest;


public class NGram {

    private String hash;
    private String[] words;

    public NGram(String[] words) {
        this.words = words;
        this.calculateHash();
    }

    private void calculateHash() {
        try {
            byte[] bytes = String.join(" ", this.words).getBytes("UTF-8");
            MessageDigest md = MessageDigest.getInstance("MD5");
            this.hash = new String(md.digest(bytes));
        } catch (Exception e) {
            System.out.println(e.toString());
        }
    }

    public boolean equals(NGram B) {
        return this.getHash().equals(B.getHash());
    }

    public String getHash() {
        return this.hash;
    }
}

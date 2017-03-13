import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;


public class MSRDataExtractor {

    static String msrDataPath = "src/extractor/msrpc/msr_paraphrase_data.txt";
    static String msrTestPath = "src/extractor/msrpc/msr_paraphrase_test.txt";
    static String msrTrainPath = "src/extractor/msrpc/msr_paraphrase_train.txt";

    public static void main(String[] args) {
//        getTest();
        getTrain();
    }

    private static void getData() {
        List<String> sources = readFromFile(msrDataPath);
        List<Sentence> sentences = getSentences(sources);
        System.out.println(sentences);
    }

    private static void getTest() {
        List<String> sources = readFromFile(msrTestPath);
        List<ParaphraseTest> tests = getParaphraseTests(sources);
        System.out.println(tests);
    }

    private static void getTrain() {
        List<String> sources = readFromFile(msrTrainPath);
        List<ParaphraseTest> tests = getParaphraseTests(sources);
        System.out.println(tests);
    }

    private static List<String> readFromFile(String filePath) {
        List<String> sources = new ArrayList<String>();
        try {
            BufferedReader br = new BufferedReader(new FileReader(filePath));
            for(String line = br.readLine(); line != null; line = br.readLine()) {
                sources.add(line);
            }
            br.close();
        } catch (Exception e) {
            System.out.print(e.toString());
        }
        return sources;
    }

    private static List<Sentence> getSentences(List<String> sources) {
        List<Sentence> sentences = new ArrayList<Sentence>();
        for (String source : sources) {
            sentences.add(new Sentence(source));
        }
        return sentences;
    }

    private static List<ParaphraseTest> getParaphraseTests(List<String> sources) {
        List<ParaphraseTest> tests = new ArrayList<ParaphraseTest>();
        for (String source : sources) {
            tests.add(new ParaphraseTest(source));
        }
        return tests;
    }

}
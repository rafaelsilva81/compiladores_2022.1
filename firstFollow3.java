
import java.util.*;
public class firstFollow3 {

    public static void main(String[] args) {
        TreeMap<String, String> grammar= new TreeMap<String, String>();
        
    }

    public int lowcase(String word) {
        int low = 0;

        for(int h = 0; h < word.length(); h++) {
            if (Character.isUpperCase(word.charAt(h))) {
                low = 0;
            } else {
                low = 1;
            }
        }

        return low;
    }
    
    public String firsts = " ";
    public String follows = " ";

    public void fist(char firstChar) {
        //int size = 9;
        TreeMap<String, String> grammar= new TreeMap<String, String>();
        grammar.put("S", "S ; S");
        grammar.put("S", "id := E");
        grammar.put("S", "print ( L )");
        grammar.put("E", "id");
        grammar.put("E", "num");
        grammar.put("E", "E + E");
        grammar.put("E", "( S , E ) ");
        grammar.put("L", "E");
        grammar.put("L", "L , E");

        String derivation_aux;
        char[] word = new char[25];
        int h = 0, i = 0;

        for (Map.Entry<String,String> entry : grammar.entrySet()) {
            if(entry.getKey().equals(Character.toString(firstChar))) {
                derivation_aux = entry.getValue();
                for (int j = 0; j < derivation_aux.length(); j++) {
                    if (derivation_aux.charAt(j) == ' ') {
                        word[h] = derivation_aux.charAt(j);
                        h++;
                    }
                }
            }
        }


    }

}
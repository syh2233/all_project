import java.util.*;

public class PriceToken {
    public double getPricesum(String shoppingReceipt) {
        String regex = "[^01245689.]+";
        shoppingReceipt = shoppingReceipt.replaceAll(regex, "#");
        StringTokenizer fenxi = new StringTokenizer(shoppingReceipt, "#");
        double sum = 0;
        while (fenxi.hasMoreElements()) {
            String item = fenxi.nextToken();
            double price = Double.parseDouble(item);
            sum = sum + price;
        }
        return sum;
    }
}
import java.util.*;

public class PriceToken {
    public double getPricesum(String shoppingReceipt) {
        String regex = "[^01245689.]"; // 正则表达式有误，应该是"[^0-9.]"来匹配非数字字符
        shoppingReceipt = shoppingReceipt.replaceAll(regex, "#"); // 将非数字字符替换为"#"
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
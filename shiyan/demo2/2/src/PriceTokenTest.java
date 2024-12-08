import java.util.*;

public class PriceTokenTest {
    public static void main(String[] args) {
        String shoppingReceipt = "水果:9元, 蔬菜: 10元, 饮料: 15元";
        PriceToken lookPriceMess = new PriceToken();
        System.out.println(shoppingReceipt);
        double sum = lookPriceMess.getPricesum(shoppingReceipt);
        System.out.println(sum);
    }
}
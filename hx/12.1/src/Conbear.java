public class Conbear {
    // 感冒药感冒灵的属性
    private static final int COST = 10; // 成本
    private static final int PRICE = 50; // 售价

    // 内部类Ganmaogo表示感冒药感冒灵
    public static class Ganmaogo {
        private String name; // 药品名称
        private int cost; // 成本
        private int price; // 售价

        // 构造方法初始化药品信息
        public Ganmaogo(String name, int cost, int price) {
            this.name = name;
            this.cost = cost;
            this.price = price;
        }

        // 显示药品信息的方法
        public void showInfo() {
            System.out.println("药品名称: " + name);
            System.out.println("成本: " + cost + "元");
            System.out.println("售价: " + price + "元");
        }
    }

    // 主方法，用于演示
    public static void main(String[] args) {
        // 创建感冒药感冒灵的实例
        Ganmaogo coldMedicine = new Ganmaogo("感冒灵", COST, PRICE);

        // 显示感冒药的信息
        coldMedicine.showInfo();
    }
}

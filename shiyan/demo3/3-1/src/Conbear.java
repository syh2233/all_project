public class Conbear {
    private int cost = 10;
    private int price = 50;

    public void show() {
        System.out.println("药物名称：感冒灵，成本：" + cost + "元，售价：" + price + "元");
    }

    public class Ganmaogo {
        public void show() {
            System.out.println("药物名称：Ganmaogo，成本：" + Conbear.this.cost + "元，售价：" + Conbear.this.price + "元");
        }
    }

    public static void main(String[] args) {
        Conbear conbear = new Conbear();
        conbear.show();

        Conbear.Ganmaogo ganmaogo = conbear.new Ganmaogo();
        ganmaogo.show();
    }
}
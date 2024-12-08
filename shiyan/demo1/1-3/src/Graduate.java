public abstract class Graduate implements StudentInterface, TeacherInterface {
    public static String name = "zhangsan";
    public static String sex = "男";
    public static int age = 25;
    public static int fee = 22000;
    public static int pay = 20000;

    public static void main(String args[]) {
        System.out.println("姓名为：" + name + ",性别为：" + sex + ",年龄为：" + age + "学费为：" + fee + "工资为：" + pay);
        if (pay - fee < 2000) {
            System.out.println("provide a loan");
        }
    }
}
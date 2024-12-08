public class ExceptionTest {
    public static void main(String[] args) {
        try {
            int result = 10 / 0;
        } catch (ArithmeticException e) {
            System.out.println("发生异常：" + e.getMessage());
        } finally {
            System.out.println("这是finally块中的语句。");
        }
    }
}
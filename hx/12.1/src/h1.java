public class h1 {
    public static void main(String[] args) {
        String str = "This is the wrong behavior";
        String a = "This is the wrong beavhise";
        long length = (char) str.length();
        System.out.println(length); // 第一题

        System.out.println(str.equals(a)); // 第二题

        int index = str.indexOf("is");
        int index2 = str.indexOf("is", 2);
        System.out.println(index); // 第三题
        System.out.println(index2); // 第四题
    }
}
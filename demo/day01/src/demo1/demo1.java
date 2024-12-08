package demo1;

public class demo1 {
    public static void main(String[] args) {
        System.out.println("hello world");
        System.out.println("-------------");
        printHelloWorld();
        System.out.println("-------------");
        System.out.println(sum(1,2));
    }

    public static void printHelloWorld() {
        System.out.println("hello world");
        System.out.println("hello world");
        System.out.println("hello\tworld");
    }

    public static int sum(int a, int b) {
        return a +b;
    }
}

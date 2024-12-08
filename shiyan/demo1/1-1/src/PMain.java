public class PMain {
    public static void main(String args[]){
        Employee zhangsan;
        Teacher lisi;

        zhangsan = new Employee();
        lisi = new Teacher();
        zhangsan.empno = "2001132";
        zhangsan.duty = "负责区域市场";
        lisi.teano = "2001133";
        lisi.zc = "高级教师";

        System.out.println("张三职工编号为" + zhangsan.empno);
        System.out.println("张三职责为" + zhangsan.duty);
        System.out.println("李丽职工编号为" + lisi.teano);
        System.out.println("李丽职称为" + lisi.zc);
    }
}
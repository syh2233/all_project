
// Pupil.java
public class Pupil extends Student {
    // Pupil的有参构造函数，调用父类的有参构造函数
    Pupil(String name, String sex, int age, String grade) {
        super(name, sex, age, grade, null); // 假设id可以为null或者在这里不需要
    }

    // 覆盖speak方法
    @Override
    public void speak() {
        System.out.println("该小学生的姓名：" + this.name);
        System.out.println("性别：" + this.sex);
        System.out.println("年龄：" + this.age);
        if (grade.equals("2015")) {
            System.out.println("今年是一年级");
        } else if (grade.equals("2016")) {
            System.out.println("今年是二年级");
        } else if (grade.equals("2017")) {
            System.out.println("今年是三年级");
        } else if (grade.equals("2018")) {
            System.out.println("今年是四年级");
        } else if (grade.equals("2019")) {
            System.out.println("今年是五年级");
        } else if (grade.equals("2020")) {
            System.out.println("今年是六年级");
        }
    }
}

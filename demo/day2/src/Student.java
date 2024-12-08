// Student.java
public class Student {
    String name;
    String sex;
    int age;
    String grade;
    String id;

    // 无参构造函数
    Student() {
    }

    // 有参构造函数
    Student(String name, String sex, int age, String grade, String id) {
        this.name = name;
        this.sex = sex;
        this.age = age;
        this.grade = grade;
        this.id = id;
    }

    // 抽象的speak方法，用于输出学生信息
    public void speak() {
        System.out.println("姓名" + this.name);
        System.out.println("学号" + this.id);
        System.out.println("性别" + this.sex);
    }
}


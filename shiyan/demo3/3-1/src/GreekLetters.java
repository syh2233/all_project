abstract class GreekLetters {
    abstract void show();
}

class Main {
    public static void main(String[] args) {
        showMess(new GreekLetters() {
            @Override
            void show() {
                System.out.println("Alpha Beta Gamma Delta Epsilon");
            }
        });
    }

    public static void showMess(GreekLetters gl) {
        gl.show();
    }
}
interface Photoable {
    void PhotoCatch();
}

class Phone {
    public void PhotoCatch(Photoable ph) {
        ph.PhotoCatch();
    }

    public static void main(String[] args) {
        Phone phone = new Phone();
        phone.PhotoCatch(new Photoable() {
            @Override
            public void PhotoCatch() {
                System.out.println("Taking a photo...");
            }
        });
    }
}
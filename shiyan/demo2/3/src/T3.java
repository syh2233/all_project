import java.util.Calendar;
import java.util.Date;

public class T3 {
    public static void main(String[] args) {
        Calendar calendar = Calendar.getInstance();
        int day = calendar.get(Calendar.DAY_OF_MONTH);
        int hour = calendar.get(Calendar.HOUR_OF_DAY);
        int minute = calendar.get(Calendar.MINUTE);
        int second = calendar.get(Calendar.SECOND);
        System.out.print("现在时间是：");
        System.out.printf("%d年%d月%d日 %d时%d分%d秒\n", calendar.get(Calendar.YEAR), calendar.get(Calendar.MONTH) + 1, day, hour, minute, second);

        int y = 2018, m = 9, d = 1;
        calendar.set(y, m - 1, d);
        long time1 = calendar.getTimeInMillis();

        y = 2019;
        m = 7;
        d = 1;
        calendar.set(y, m - 1, d);
        long time2 = calendar.getTimeInMillis();

        long subDay = (time2 - time1) / (1000 * 60 * 60 * 24);
        System.out.println("与" + new Date(time2));
        System.out.println("相隔" + subDay + "天");
    }
}
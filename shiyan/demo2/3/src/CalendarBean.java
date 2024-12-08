import java.util.Calendar;

public class CalendarBean {
    private int year;
    private int month;

    public void setYear(int year) {
        this.year = year;
    }

    public void setMonth(int month) {
        this.month = month;
    }

    public String[] getCalendar() {
        String[] calendar = new String[42]; // 6行7列，加上可能的空白
        Calendar rili = Calendar.getInstance();
        rili.set(year, month - 1, 1);
        int weekDay = rili.get(Calendar.DAY_OF_WEEK); // 星期几，以1（星期日）到7（星期六）表示
        int daysInMonth = getDaysInMonth(year, month); // 该月的天数

        // 填充日历数组
        for (int i = 0; i < 42; i++) {
            calendar[i] = "";
        }
        for (int i = weekDay - 1; i < 42; i++) {
            if (i < weekDay - 1 + daysInMonth) {
                calendar[i] = String.valueOf(i - weekDay + 2); // 从1开始计数
            }
        }

        return calendar;
    }

    private int getDaysInMonth(int year, int month) {
        // 判断是否为闰年
        boolean isLeapYear = (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
        if (month == 2) {
            return isLeapYear ? 29 : 28;
        } else if (month == 4 || month == 6 || month == 9 || month == 11) {
            return 30;
        } else {
            return 31;
        }
    }

    public static void main(String[] args) {
        CalendarBean calendarBean = new CalendarBean();
        calendarBean.setYear(2020);
        calendarBean.setMonth(12);
        String[] calendar = calendarBean.getCalendar();

        // 打印日历
        System.out.println("日 一 二 三 四 五 六");
        for (int i = 0; i < 42; i++) {
            if (i % 7 == 0 && i != 0) {
                System.out.println();
            }
            System.out.print(calendar[i] + " ");
        }
    }
}
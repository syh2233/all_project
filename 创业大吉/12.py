def exam1():
    n = int(input())
    F = [1 for i in range(n+1)]
    k = 3
    while k <= n:
        F[k] = F[n-1]+F[n-2]
        k += 1

    print(F[n])


def exam2():
    import math
    a = int(input())
    b = a*pow(math.pi, 2)
    print("%.7f" % b)


def exam3():
    n = int(input())
    s = n*(n+1) / 2
    print(s)


def exam4():
    a, b = map(int, input().split(" "))
    print(a+b)


def exam5():
    n = int(input())
    arr = input().split(" ")
    print(max(int(arr[i]) for i in range(n)))
    print(min(int(arr[i]) for i in range(n)))
    print(sum(int(arr[i]) for i in range(n)))


def exam6():
    arr = [chr(ord('A') + i) for i in range(26)]
    n, m = map(int, input().split())
    arr1 = [[0 for i in range(m)] for j in range(n)]
    for i in range(n):
        for j in range(m):
            if j >= i:
                arr1[i][j] = chr(ord('A')+j-i)
            else:
                arr1[i][j] = chr(ord('A')+i-j)

    for i in range(n):
        for j in range(m):
            print(arr1[i][j], end='')
        print()


def exam7():
    for i in range(32):
        print("{0:0>5}".format(format(i, 'b')))


def exam8():
    while 1:
        y = int(input())
        print("yes" if y%4==0 and y%100!=0 or y%400==0 else "no")


def exam9():
    n = int(input())
    sum = 1
    for i in range(1, n+1):
        sum = sum * int(i)

    print(sum)


def exam10():
    a = input()
    b = input()
    aa = list(a)
    aa.reverse()
    bb = list(b)
    bb.reverse()
    def jinzi(a1,b1):
        global r
        if int(a1) + int(b1) > 10:
            r = 1
        else:
            r = 0
    cc = [0 for i in range(len(a))]
    dd= []
    r = 0
    d = 0
    for i in range(len(a)):
        cc[i] = r
        try:
            jinzi(a1=aa[i], b1=bb[i])
            dd.append(bb[i])
        except:
            jinzi(a1=aa[i], b1=0)
            dd.append('0')
        if int(aa[i]) + int(dd[i])+ int(cc[i]) >= 10:
            cc[i] = (int(aa[i]) + int(dd[i]) + int(cc[i]))%10
            d = 1
        else:
            cc[i] = (int(aa[i]) + int(dd[i]) + int(cc[i])) % 10 + d
            d = 0
    cc.reverse()

    for j in cc:
        print(j, end='')


def exam11():
    n = int(input())
    pi = list(map(int, input().split()))
    sum1 = 0
    for j in range(2*n):
        try:
            pa = min(pi[i] for i in range(len(pi)))
        except:
            break
        pi.remove(pa)
        if j % 2 == 0:
            pb = pa
        else:
            pi.append(pa+pb)
            sum1 = sum1 + pa + pb
    print(sum1)


def exam12():
    n = int(input())
    arr = [[0 for i in range(n)] for i in range(n)]
    arr1 = []
    def play_quan():
        for i in range(n):
            for j in range(n):
                a = arr[i][j]
                if a == 1:
                    for l in range(n):
                        arr1.append(f'{i}_{l}')
                        arr1.append(f'{l}_{j}')
                    for k in range(n):
                        if k <= 10:
                            arr1.append(f'{i+k}_{k+j}')
                            if i-k > 0:
                                arr1.append(f'{i - k}_{k + j}')
                            elif k-j > 0:
                                arr1.append(f'{i + k}_{j - k}')
                            elif i-k > 0 and j-k > 0:
                                arr1.append(f'{i - k}_{j - k}')
                        else:
                            break
    for i in range(n):
        for j in range(n):
            play_quan()
            if f'{i}_{j}' not in arr1:
                arr[i][j] = 1
    for i in arr:
        print(i)


def exam13():
    n = int(input())
    arr = list(map(int, input().split(" ")))
    arr.sort()
    for i in arr:
        print(i, end=' ')


def exam14():
    v1, v2, t, s, l = map(int, input().split(" "))
    t2 = l/v2
    a = 0
    tim = t/(v1 -v2)#超越时的时间
    l2 = tim * v2#超越t时的路程
    tu = l2/v1#兔子跑t的时间
    while (l2 + tu*v1 + t) * a < l:
        a += 1
    t1 = (a-1)*s + l/v1
    if t2 == t1:
        print('D')
        print('%.0f'%t1)
    elif t2<t1:
        print('T')
        print('%.0f'%t2)
    elif t2>t1:
        print('R')
        print('%.0f'%t1)


def exam15():
    n = int(input())
    arr = []
    s = 1
    a = ''
    for k in range(n):
        for i in range(k+1, 0, -1):
            if i==k+1:
                s = (str(f"{k+1}"))
            elif i%2==0:
                s = (str(f"{i}+sin({s})"))
            elif i%2==1:
                s = (str(f"{i}-sin({s})"))
            a = str(f"sin({s})")
        arr.append(a)
    try:
        arr.remove('')
    except:
        arr = arr
    j = 0
    a1 = ''
    for i in range(n, 0, -1):
        s2 = str(f'{arr[j]} + {i}')
        try:
            s22 = a1
        except:
            s22 = ''
        if i == n:
            a1 = str(f"{s2}")
        else:
            a1 = str(f"({s22}){s2}")

        j += 1
    print(a1)


def exam16():
    n = int(input())
    arr = list(input())
    arr1 = [0 for i in range(n)]
    k=0
    for i in arr:
        for j in arr:
            if i==j:
                arr1[k] = i
                arr1[n-1-k] = j
            else:
                if n%2==0:
                    arr1[int(n/2)] = i
                else:
                    arr1[int((n-1) / 2)] = j
        k += 1
        arr.remove(i)
        try:
            arr.remove(i)
        except:
            k
    print(arr1)


def exam17():
    arr1 = list(input().split())
    arr2 = list(input().split())
    h = int(arr2[3]) - int(arr1[3])
    w = int(arr2[0]) - int(arr1[0])
    s = h * w
    print("%.2f"%s)


def exam18():
    n = int(input())
    arr = [[0 for i in range(n)] for i in range(n)]
    for i in arr:
        print(i)


def exam19():
    t = int(input())
    arr = []
    for i in range(t):
        n = input()
        ans = format(int(n, 16), 'o')
        arr.append(ans)
    for i in arr:
        print(i)


def exam20():
    a = input()
    b = input()
    c = 0
    if len(a) != len(b):
        print(1)
    else:
        for i, j in zip(a, b):
            if ord(i) + 32 == ord(j) or ord(i) - 32 == ord(j):
                c = 1
        if c == 1:
            print(3)
        elif a == b:
            print(2)
        else:
            print(4)


def exam21():
    t = int(input())
    h = int(t / 3600)
    m = int((t % 3600) / 60)
    s = int(t % 60)
    print(f"{h}:{m}:{s}")


def exam22():
    n = input()
    print(int(n, 16))


def exam23():
    n = int(input())
    print(format(n, 'X'))


def exam24():
    n = int(input())
    for i in range(10000, 1000000):
        num = str(i)
        if num == num[::-1]:
            if n == sum(int(j) for j in num):
                print(num)


def exam25():
    n = input()
    count = 0
    for i in n:
        if i == 'a' or i == 'e' or i == 'i' or i == 'o' or i == 'u':
            count += 1
    print(count)


def exam26():
    list1 = []
    for i in range(1000, 10000):
        mun = str(i)
        if mun == mun[::-1]:
            list1.append(i)
    print(list1)


def exam27():
    arr = []
    for i in range(100, 1000):
        sum = str(i)
        if pow(int(sum[0]), 3) + pow(int(sum[1]), 3) +pow(int(sum[2]), 3) == i:
            arr.append(i)
    print(arr)


def exam28():
    n = int(input())
    triangle = [[1]]
    for i in range(1, n):
        row = [1]  # 每一行的第一个数字是1
        # 计算中间的元素，每个元素是上一行的相邻两元素之和
        for j in range(1, i):
            row.append(triangle[i - 1][j - 1] + triangle[i - 1][j])
        row.append(1)  # 每一行的最后一个数字是1
        triangle.append(row)
    for row in triangle:
        print(' '.join(map(str, row)))


def exam29():
    n = int(input())
    count = 0
    arr = list(input().split())
    a = input()
    if a in arr:
        for i in arr:
            count += 1
            if a == i:
                break
        print(count)
    else:
        print("-1")


def exam30():
    a, b, c = map(float, input().split())
    if int(a) == 1:
        d = (b+c) / 2*1.08
        print("%.3f" % d)
    elif int(a) == 0:
        d = b*0.923 + c / 2
        print("%.3f" % d)


def exam31():
    n, m = map(int, input().split())
    arr = [[list(input().split())] for i in range(m)]


def exam32():
    n = 2024
    for i in range(n+1):
        for j in range(n+1):
            if i * j == 2024 and i%2==1:
                print(i)



def exam33():
    import math
    n = 2024
    count = 0
    while True:
        count += 1
        n = int(math.sqrt(n))
        if n == 1:
            break
    print(count)

def exam34():
    import math
    n = 0
    while True:
        n += 1
        if n *n *n >= 2024:
            break
    print(n)
    print(pow(n, 3)-2024)


def exam35():#2 三 3 四 4 五 5 六 6 日 7 一
    import calendar
    count = 0
    a = 0
    for i in range(1901, 2025):
        if calendar.isleap(i):
            arr = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            for k in arr:
                for j in range(k):

                    sum = str(j)
                    if sum == '1' and (a + 1)% 7 == 0:
                        count += 1
                    elif len(sum) == 1:
                        continue
                    elif sum[1] == "1" and (a + 1)% 7 == 0:
                        count += 1
                    a += 1
        else:
            arr = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            for k in arr:
                for j in range(k):
                    a += 1
                    sum = str(j)
                    if sum == '1' and (a + 1)% 7 == 0:
                        count += 1
                    elif len(sum) == 1:
                        continue
                    elif sum[1] == "1" and (a + 1)% 7 == 0:
                        count += 1
    print(count)
exam35()


def exam36():
    n = int(input())
    if n < 15:
        count = 0
    else:
        count = int(n / 15)*2
    print(count)


def exam37():
    n = int(input())
    a = str(n)
    arr = []
    for i in a:
        arr.append(i)
    print(max(int(arr[i]) for i in range(len(a))))


def exam38():
    a, b = map(int, input().split("-"))
    if 0 < a < 1000000000 and 0 < b < 1000000000:
        print(a-b)
    else:
        print("数据过大")


def exam39():
    n = int(input())
    arr1 = list(input().split(" "))
    k = int(input())
    if len(arr1) != n:
        print("数列不符合·")
    else:
        arr1.sort()
        arr1.pop()
        print(arr1)


def exam40():#冒泡排序
    n = int(input())
    arr = list(map(int, input().split()))
    for i in range(1, n):
        for j in range(n - i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j +1],arr[j]
    print(arr)


def exam41():#选择排序
    n = int(input())
    arr = list(map(int, input().split()))
    for i in range(n-1):
        mini = arr[i]
        miniid = i
        for j in range(i, n):
            if arr[j] < mini:
                mini = arr[j]
                miniid = j
        arr[i], arr[miniid] = arr[miniid], arr[i]
    print(" ".join(map(str, arr)))

def exam42():#插入排序
    n = int(input())
    a = list(map(int, input().split()))

    for i in range(1, n):
        value = a[i]
        insert_idx = 0
        for j in range(i - 1, -1, -1):
            if a[j] > value:
                 a[j+1] = a[j]
            else:
                insert_idx = j + 1
                break
        a[insert_idx] = value

    print(" ".join(map(str, a)))


def exam43():
    def partition(a, left, right):
        idx = left + 1
        for i in range(left + 1, right + 1):
            if a[i] <= a[left]:
                a[i], a[idx] = a[idx], a[i]
                idx += 1
        a[left], a[idx - 1] = a[idx - 1], a[left]
        print(a)
        return idx - 1


    def quicksort(a, left, right):
        if left < right:
            mid = partition(a, left, right)
            quicksort(a, left, mid -1)
            quicksort(a, mid + 1, right)

def exam45():
    MOD = 10 ** 9 + 7

    # 计算9^10000 % (10^9 + 7)
    nine_pow = pow(9, 10000, MOD)

    # 计算7^10000 % (10^9 + 7)
    seven_pow = pow(7, 10000, MOD)

    # 计算(9^10000 - 7^10000) % (10^9 + 7)
    result = (nine_pow - seven_pow) % MOD

    print(result)

def exam46():
    n = int(input())
    arr = []
    for i in range(n):
        arr.append(input())
    for i in arr:
        a, b, c = i.split(" ")
        b1, b2, b3 = str(b).split(":")
        b2 = int(int(b2) / int(c)) * int(c)
        b = f"{b1}:{str(b2)}:{b3}"
        i = f"{a} {b}"
        print(i)


def exam47():
    def count_pairs(n, m, grid):
        diagonal_counts = {}

        # 步骤 2: 遍历网格并更新计数
        for a in range(n):
            for b in range(m):
                v = grid[a][b]
                d1 = a - b
                d2 = a + b
                if v not in diagonal_counts:
                    diagonal_counts[v] = {}
                if d1 not in diagonal_counts[v]:
                    diagonal_counts[v][d1] = 0
                diagonal_counts[v][d1] += 1
                if d2 not in diagonal_counts[v]:
                    diagonal_counts[v][d2] = 0
                diagonal_counts[v][d2] += 1

        # 步骤 3: 计算格子对的数量
        total_pairs = 0
        for v in diagonal_counts:
            for count in diagonal_counts[v].values():
                total_pairs += count * (count - 1)

        return total_pairs // 2

    # 示例输入
    n, m = 3, 2
    grid = [
        [1, 2],
        [2, 3],
        [3, 2]
    ]

    # 计算并输出结果
    print(count_pairs(n, m, grid))

def exam48():
    def binary_sum(n):
        return bin(n).count('1')

    def quaternary_sum(n):
        if n == 0:
            return 0
        total = 0
        while n > 0:
            total += n % 4
            n //= 4
        return total

    count = 0
    for n in range(1, 2025):
        if binary_sum(n) == quaternary_sum(n):
            count += 1

    print(count)


def exam49():
    count = 0
    n = int(input())
    m = int(input())
    for i in range(n):
        if m % 3 == 0:
            count += 6
        elif m % 3 == 1:
            for _ in range(m//3):
                count += 6
            count += 1
        elif m % 3 == 2:
            for _ in range(m//3):
                count += 6
            count += 4
    print(count)


def exam50():
    n = int(input())
    count = 0
    arr1 = list(input().split())
    arr3 = arr1
    arr2 = list(input().split())
    arr4 = arr2
    idx = -1
    for i in range(len(arr3)):
        if i > idx:
            mun = str(arr3[i])
            if "0" in mun or "2" in mun or "4" in mun:
                idx = i
            else:
                continue
            count += 1
            for k in range(len(arr4)):
                if k > idx:
                    mun1 = str(arr4[k])
                    if "0" in mun1 or "2" in mun1 or "4" in mun1:
                        idx = k
                    else:
                        continue
                    count += 1
                    break
                else:
                    continue
        else:
            continue
    print(count)


def exam51():
    def floyd(n, edges):
        dist = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        for u, v, w in edges:
            dist[u - 1][v - 1] = w
            dist[v - 1][u - 1] = w

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

        return dist

    def count_pairs(n, L, R, dist):
        count = 0
        for i in range(n):
            for j in range(i + 1, n):
                max_edge = max(dist[i][j])
                if L <= max_edge <= R:
                    count += 1
        return count

    # 读取输入
    N, M, L, R = map(int, input().split())
    edges = []
    for _ in range(M):
        u, v, w = map(int, input().split())
        edges.append((u, v, w))

    # 应用弗洛伊德算法
    dist = floyd(N, edges)

    # 统计满足条件的城市对数量
    result = count_pairs(N, L, R, dist)
    print(result)
    for i in dist:
        print(i)


def exam52():
    a = ""
    count = 0
    arr = []
    for i in range(1, 2024):
        a = a + str(i)
    for i in a:
        arr.append(i)
    print(arr)
    for i in range(2023):
        if arr[i] == "2":
            for j in range(2023):
                if j > i:
                    if arr[j] == "0":
                        for k in range(2023):
                            if k > j > i:
                                if arr[k] == "2":
                                    for p in range(2023):
                                        if p > k > j > i:
                                            if arr[p] == "3":
                                                count += 1
                                            else:
                                                continue
                                        else:
                                            continue
                                else:
                                    continue
                            else:
                                continue
                    else:
                        continue
                else:
                    continue
        else:
            continue
    print(count)


def exam53():
    def is_prime(n):
        """判断一个数是否为质数"""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def count_double_primes_in_range(start, end):
        """在指定范围内查找所有双子数"""
        double_primes = []
        for num in range(start, end + 1):
            # 尝试将 num 分解为 p^2 * q^2 的形式
            found = False
            for p in range(2, int(num ** 0.5) + 1):
                if is_prime(p):
                    if num % (p * p) == 0:
                        q_squared = num // (p * p)
                        q = int(q_squared ** 0.5)
                        if q * q == q_squared and is_prime(q) and p != q:
                            double_primes.append(num)
                            found = True
                            break
            if not found:
                continue
        return double_primes

    # 定义区间
    start = 2333
    end = 23333333333333

    # 查找区间内的双子数
    double_primes = count_double_primes_in_range(start, end)

    # 打印结果
    print(f"在区间 [{start}, {end}] 内的双子数有 {len(double_primes)} 个")
    # 如果需要查看具体的双子数，可以取消注释下面的行
    # print(double_primes)


def exam54():
    while True:
        n = int(input())
        if n % 2 == 0:
            arr = list(map(int, input().split(" ")))
            if len(arr) != n:
                print("位数不符合")
            else:
                break
        else:
            print("请输入偶数")
    from collections import Counter

    new_arr = [k for k, v in Counter(arr).items() if v == 1]

    print(int(len(new_arr)/2))


def exam55():
    while True:
        n, m = map(int, input().split())
        arr1 = list(map(int, input().split(" ")))
        arr2 = list(map(int, input().split(" ")))
        if len(arr1) != n or len(arr2) != m:
            print("位数不符合")
        else:
            break
    arr3 = []
    arr4 = []
    a = 0
    for i in arr1:
        i = a + i
        arr3.append(i)
        a = i
    a = 0
    for i in arr2:
        i = a + i
        arr4.append(i)
        a = i
    if len(arr3) > len(arr4):
        print(len(arr3)-len(arr4))
    else:
        print(len(arr4)-len(arr3))


def exam56():
    n = int(input())
    arrx = []
    arry = []
    arrlen = []
    for _ in range(n):
        x, y = input().split(" ")
        arrx.append(x)
        arry.append(y)
    import math
    for i in range(n):
        for j in range(i+1, n):
            len1 = math.sqrt(pow(int(arrx[i])-int(arrx[j]), 2)+pow(int(arry[i])-int(arry[j]), 2))
            arrlen.append(len1)
    print(arrlen)
    print(len(arrlen))
    from itertools import combinations

    def can_form_triangle(a, b, c):
        return a + b > c and a + c > b and b + c > a

    def count_isosceles_triangles(lst):
        count = 0
        # 生成所有可能的三个数的组合
        for combo in combinations(lst, 3):
            if can_form_triangle(*combo):
                # 检查是否为等腰三角形
                if combo[0] == combo[1] or combo[1] == combo[2] or combo[0] == combo[2]:
                    count += 1
        return count

    print(count_isosceles_triangles(arrlen))


def exam57():
    t = 233333 / 17
    dx1 = 15 * t
    dx2 = 343720 - dx1
    dy2 = dx2/15*17
    print(dy2)


def exam58():
    n = int(input())
    arr = []
    count = 0
    a = 0
    for i in range(1, n+1):
        mun = str(i)
        for j in mun:
            arr.append(j)
        arr.reverse()
        for l in range(1, len(arr)+1):
            if l % 2 == 1:
                if int(arr[l-1]) % 2 == 1:
                    a = 1
                else:
                    a = 0
                    break
            else:
                if int(arr[l - 1]) % 2 == 0:
                    a = 1
                else:
                    a = 0
                    break
        if a == 1:
            count += 1
        arr = []
    print(count)


def exam59():
    n, d = map(float, input().split())
    n = int(n)
    a = d * pow(2, n)
    b = f"{int(a)}.5 "
    if a > float(b):
        a = int(a) + 1
    else:
        a = int(a)
    print(a)


def exam60():
    import math
    from itertools import combinations
    while True:
        n = int(input())
        arr1 = list(map(int, input().split(" ")))
        if len(arr1) != n:
            print("位数不符合")
        else:
            break

    def lcm(a, b):
        return abs(a * b) // math.gcd(a, b)

    def run(a, b, c):
        op = lcm(lcm(a, b), c)/(lcm(a, b) * lcm(a, c) * lcm(b, c))
        s = a * b * c * op
        return s
    r = 0
    result = []
    for combo in combinations(arr1, 3):
        s = run(*combo)
        if s > r:
            r = s
            result.append(combo[0])
            result.append(combo[1])
            result.append(combo[2])
    print(" ".join(map(str, result)))


def exam61():
    from itertools import combinations
    while True:
        n = int(input())
        arr1 = list(map(int, input().split(" ")))
        if len(arr1) != n:
            print("位数不符合")
        else:
            break
    a = 0
    b = 0
    arr4 = []
    for i in range(len(arr1)):
        for combo in combinations(arr1, i):
            arr3 = [x for x in arr1 if x not in combo]
            for j in range(len(combo)):
                a += combo[j]
            for k in range(len(arr3)):
                b += arr3[k]
            c = abs(a - b)
            arr4.append(c)
            a = 0
            b = 0

    print(min(int(arr4[i]) for i in range(len(arr4))))


def exam62():
    def max_MouthSum(matrix):
        n = len(matrix)
        m = len(matrix[0])
        max_sum = float('-inf')

        for x1 in range(n):
            for y1 in range(m):
                for x2 in range(x1 + 1, n + 1):
                    y2 = y1 + (x2 - x1)
                    if y2 > m:  # 确保 y2 不超出列的范围
                        break
                    mouth_sum = 0
                    # 左边一竖
                    for x in range(x1, x2):
                        mouth_sum += matrix[x][y1]
                    # 上面一横
                    for y in range(y1, y2):
                        mouth_sum += matrix[x1][y]
                    # 右边一竖
                    for x in range(x1, x2):
                        mouth_sum += matrix[x][y2]
                    # 下面一横
                    for y in range(y1, y2):
                        mouth_sum += matrix[x2][y]
                    # 减去重复计算的四个角
                    mouth_sum -= matrix[x1][y1] + matrix[x1][y2] + matrix[x2][y1] + matrix[x2][y2]
                    max_sum = max(max_sum, mouth_sum)
        return max_sum

    # 读取输入
    n, m = map(int, input().split())
    matrix = []
    for _ in range(n):
        row = list(map(int, input().split()))
        matrix.append(row)

    # 计算最大和
    max_sum = max_MouthSum(matrix)

    # 输出结果
    print(max_sum)
n,p,q = map(int, input().split())
xies = []
for _ in range(n):
    xies.append(list(map(int, input().split())))
left_xie = {}
right_xie = {}
for xie in xies:
    lr,size,color = xie
    if lr == 0:
        if size not in left_xie:
            left_xie[size] = []
        left_xie[size].append(color)
    else:
        if size not in right_xie:
            right_xie[size] = []
        right_xie[size].append(color)
price = 0
for size in set(left_xie.keys()).intersection(set(right_xie.keys())):
    left_colors = left_xie[size]
    right_colors = right_xie[size]

    left_price = {}
    for color in left_colors:
        left_price[color] = left_price.get(color, 0) + 1
    right_price = {}

    for color in right_colors:
        right_price[color] = right_price.get(color, 0) + 1

    same_color_pairs = 0
    for color in set(left_price.keys()).intersection(right_price.keys()):
        same_color_pairs += min(left_price[color], right_price[color])

    price += same_color_pairs*p
    price_pairs = min(len(left_colors), len(right_colors))
    price += (price_pairs - same_color_pairs) * p

    print(price)
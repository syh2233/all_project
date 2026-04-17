import ast

s = input().strip()                            # 读取一行，比如 [[1,3],[2,6],[8,10],[15,18]]
intervals = [list(map(int, seg)) for seg in ast.literal_eval(s)]
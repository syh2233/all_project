"""
题目：有效的括号
给定一个只包含字符 '('，')'，'{'，'}'，'['，']' 的字符串 s，判断字符串是否是有效的。
有效字符串需满足：
左括号必须用相同类型的右括号闭合。
左括号必须以正确的顺序闭合。

示例
输入：s = "()"
输出：True
输入：s = "()[]{}"
输出：True
输入：s = "(]"
输出：False
输入：s = "([)]"
输出：False
输入：s = "{[]}"
输出：True

提示
1 <= s.length <= 10⁴
s 仅由 '()[]{}' 组成
思路提示
用 栈 来保存未匹配的左括号。
遇到左括号，就压栈。
遇到右括号，就检查栈顶是否是对应的左括号：
如果匹配，就弹出栈顶继续。
如果不匹配，直接返回 False。
遍历结束后，如果栈为空，说明完全匹配，返回 True；否则返回 False。
"""
s = str(input())
stack = []
pairs = {
    ')': '(',   # 右括号 -> 左括号
    ']': '[',
    '}': '{'
}
for c in s:
    if stack == []:
        stack.append(c)
        continue
    if c in pairs.keys():
        if stack[-1] == pairs[c]:
            stack.pop()
            continue
        else:
            print(f"False")
    else:
        stack.append(c)
if stack == []:
    print(f"True")
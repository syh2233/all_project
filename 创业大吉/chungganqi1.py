import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
from matplotlib.font_manager import FontProperties

# 设置matplotlib的字体，以确保中文和负号可以正确显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题

# 给定的数据
X = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
Vo = np.array([-3.18, -8.72, -10.2, -10.28, -10.33, -10.36, -10.38, -10.39, -10.4, -10.41])

# 绘制V-X曲线
plt.figure(figsize=(10, 6))
plt.plot(X, Vo, marker='o', linestyle='-', color='b')
plt.title('Vo-X曲线图')
plt.xlabel('X (mm)')
plt.ylabel('Vo (V)')
plt.grid(True)
plt.show()

# 使用最小二乘法拟合直线
slope, intercept, r_value, p_value, std_err = linregress(X, Vo)

# 计算线性区域的灵敏度S和线性度
S = slope  # 灵敏度S是Vo对X的斜率
linearity = r_value**2  # 线性度是R平方值

print(f"灵敏度S: {S:.4f} V/mm")
print(f"线性度: {linearity:.4f}")

# 绘制拟合直线
X_fit = np.linspace(min(X), max(X), 100)
Vo_fit = intercept + slope * X_fit
plt.figure(figsize=(10, 6))
plt.plot(X, Vo, 'o', label='实验数据')
plt.plot(X_fit, Vo_fit, 'r-', label='拟合直线')
plt.title('Vo-X曲线图及拟合直线')
plt.xlabel('X (mm)')
plt.ylabel('Vo (V)')
plt.legend()
plt.grid(True)
plt.show()
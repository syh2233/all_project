import pandas as pd

# 读取Excel文件
df = pd.read_excel('查价格.xlsx', sheet_name='Sheet1')
sku11 = df['货号']
unique_sku = sku11.drop_duplicates()
column_data = unique_sku.tolist()

# 将列表分成10个列表
list_count = 10
chunk_size = len(column_data) // list_count

# 按顺序分割列表
split_lists = [column_data[i:i + chunk_size] for i in range(0, len(column_data), chunk_size)]

# 格式化每个SKU编号
formatted_lists = []
for i, sublist in enumerate(split_lists):
    formatted_sublist = [f"{sku}:{i + 1}" for sku in sublist]
    formatted_sublist_str = "|".join(formatted_sublist)  # 将子列表中的元素用|连接成字符串
    formatted_lists.append(formatted_sublist_str)

# 输出结果
list = []
for i, sublist_str in enumerate(formatted_lists):
    print(f"List {i + 1}: {sublist_str}")
    list.append(sublist_str)
print(list)

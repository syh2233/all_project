import pandas as pd

df = pd.read_excel(io=r'C:\Users\沈家\Desktop\cheshi.xlsx')
df1 = df['url'].str.split(',', expand=True)
result_df = pd.concat([df, df1], axis=1)
result_df.to_excel(r'C:\Users\沈家\Desktop\cheshi.xlsx', index=False)
# a = ['年份', '地区', '类型', '导演', '主演']
# with pd.ExcelWriter(r'C:\Users\沈家\Desktop\中国台湾.xlsx', engine='openpyxl', mode='a') as writer:
#     workbook = writer.book
#     worksheet = writer.sheets['Sheet1']
#     for index, value in enumerate(a, start=5):
#         worksheet.cell(row=1, column=index).value = value
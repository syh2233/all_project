import pandas as pd

rode = input("请输入文件编码:")
rode_re = "E:\\2000\\" + rode + "\\" + rode + ".xlsx"
df_split1 = pd.read_excel(rode_re, sheet_name='Sheet5', usecols=['Category'], engine='openpyxl')
df_split = df_split1['Category'].astype(str).str.split('->', expand=True)
df_splitname = pd.DataFrame()
df_splitcat = pd.DataFrame()
df_splitname['name'] = df_split[0]
df_splitcat['cat'] = df_split[1]
with pd.ExcelWriter(rode_re, engine='openpyxl', mode='a') as writer:
    workbook = writer.book
    worksheet = writer.sheets['Sheet5']
    for row in range(len(df_splitname)):
        cell = worksheet.cell(row=row + 2, column=13)
        cell.value = df_splitname.iloc[row]['name']
        cell = worksheet.cell(row=row + 2, column=14)
        cell.value = df_splitname.iloc[row]['name']
        cell = worksheet.cell(row=row + 2, column=3)
        cell.value = df_splitcat.iloc[row]['cat']
        cell = worksheet.cell(row=row + 2, column=4)
        cell.value = df_split1.iloc[row]['Category']
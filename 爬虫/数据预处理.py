import pandas as pd


class data_processing(object):

    def __init__(self):
        # 创建参数
        rode = input("请输入文件编码:")
        self.lang = input("请输入语言:")
        self.file_path = r'C:\Users\沈家\Desktop\Content.xlsx'
        self.sheet_name = 'Content'
        self.rode_re = "E:\\2000\\" + rode + "\\" + rode + ".xlsx"
        self.output_file = self.rode_re
        self.output_sheet_name = 'Sheet5'

    def read(self, file_path, sheet_name):
        # 读取数据
        self.df_sku = pd.read_excel(file_path, sheet_name=sheet_name, usecols=['sku'], engine='openpyxl')
        self.df_img = pd.read_excel(file_path, sheet_name=sheet_name, usecols=['img'], engine='openpyxl')
        self.df_color = pd.read_excel(file_path, sheet_name=sheet_name, usecols=['color'], engine='openpyxl')
        self.df_size = pd.read_excel(file_path, sheet_name=sheet_name, usecols=['size'], engine='openpyxl')
        self.df_title = pd.read_excel(file_path, sheet_name=sheet_name, usecols=['title'], engine='openpyxl')
        df_price = pd.read_excel(file_path, sheet_name=sheet_name, usecols=['price'], engine='openpyxl')
        self.df_price = df_price.astype(str)
        self.df_desc = pd.read_excel(file_path, sheet_name=sheet_name, usecols=['desc'], engine='openpyxl')
        self.df_brand = pd.read_excel(file_path, sheet_name=sheet_name, usecols=['brand'], engine='openpyxl')
        self.df_date = pd.read_excel(file_path, sheet_name=sheet_name, usecols=['date'], engine='openpyxl')
        self.df_PageUrl = pd.read_excel(file_path, sheet_name=sheet_name, usecols=['PageUrl'], engine='openpyxl')

    def dispose(self, df_color, df_title):
        # 数据处理
        dictionary_color = df_color['color'].to_dict()
        dictionary_title = df_title['title'].to_dict()
        capitalized_color = {key: str(value).capitalize() for key, value in dictionary_color.items()}
        capitalized_title = {key: str(value).capitalize() for key, value in dictionary_title.items()}
        df_color = pd.DataFrame(list(capitalized_color.items()), columns=['key', 'color'])
        df_title = pd.DataFrame(list(capitalized_title.items()), columns=['key', 'title'])
        self.df_dispose_color = df_color.drop(columns=['key'])
        self.df_dispose_title = df_title.drop(columns=['key'])

    def writer(self, output_file, output_sheet_name, df_sku, df_img, df_dispose_color, df_dispose_title, df_price,
               df_desc,
               df_brand, df_date, df_PageUrl, lang, df_size):
        # 将数据写入到新的Excel文件中
        with pd.ExcelWriter(output_file, engine='openpyxl', mode='a') as writer:
            workbook = writer.book
            worksheet = writer.sheets[output_sheet_name]
            a = ['featured_image', 'LANG', 'CAT-0', 'Category', 'SIZE', 'SKU', 'Style-Name', 'TITLE', 'Brand',
                 'Brand-name', 'model', 'Type', 'Gender', 'Gender-name', 'Color', 'Color-Name', 'desc', 'desc2',
                 'price', 'price2', 'Description', 'Keyword', 'IMG-Add', 'NPrice',	'OPrice', 'max', 'min', 'NSize',
                 'Date', 'PageUrl']
            for i, row1 in enumerate(range(1, len(df_sku)+1), start=1):
                cell = worksheet.cell(row=row1 + 1, column=4)
                cell.value = ('=VLOOKUP(AD' + str(i + 1) + ',Sheet4!A:B,2,FALSE)')
            for index, value in enumerate(a, start=1):
                worksheet.cell(row=1, column=index).value = value
            for row in range(len(df_sku)):
                cell = worksheet.cell(row=row + 2, column=6)
                cell.value = df_sku.iloc[row]['sku']
                cell = worksheet.cell(row=row + 2, column=1)
                cell.value = df_img.iloc[row]['img']
                cell = worksheet.cell(row=row + 2, column=15)
                cell.value = df_dispose_color.iloc[row]['color']
                cell = worksheet.cell(row=row + 2, column=16)
                cell.value = df_dispose_color.iloc[row]['color']
                cell = worksheet.cell(row=row + 2, column=7)
                cell.value = df_dispose_title.iloc[row]['title']
                cell = worksheet.cell(row=row + 2, column=8)
                cell.value = df_dispose_title.iloc[row]['title']
                cell = worksheet.cell(row=row + 2, column=19)
                cell.value = df_price.iloc[row]['price']
                cell = worksheet.cell(row=row + 2, column=20)
                cell.value = df_price.iloc[row]['price']
                cell = worksheet.cell(row=row + 2, column=17)
                cell.value = df_desc.iloc[row]['desc']
                cell = worksheet.cell(row=row + 2, column=18)
                cell.value = df_desc.iloc[row]['desc']
                cell = worksheet.cell(row=row + 2, column=9)
                cell.value = df_brand.iloc[row]['brand']
                cell = worksheet.cell(row=row + 2, column=10)
                cell.value = df_brand.iloc[row]['brand']
                cell = worksheet.cell(row=row + 2, column=29)
                cell.value = df_date.iloc[row]['date']
                cell = worksheet.cell(row=row + 2, column=30)
                cell.value = df_PageUrl.iloc[row]['PageUrl']
                cell = worksheet.cell(row=row + 2, column=2)
                cell.value = lang
                cell = worksheet.cell(row=row + 2, column=5)
                cell.value = df_size.iloc[row]['size']

    def data_processing(self):
        # self.__init__()
        self.read(self.file_path, self.sheet_name)
        self.dispose(self.df_color, self.df_title)
        self.writer(self.output_file, self.output_sheet_name, self.df_sku, self.df_img, self.df_dispose_color,
                    self.df_dispose_title,
                    self.df_price, self.df_desc, self.df_brand, self.df_date, self.df_PageUrl, self.lang, self.df_size)

    def run(self):
        self.data_processing()


if __name__ == '__main__':
    data_processing = data_processing()
    data_processing.run()
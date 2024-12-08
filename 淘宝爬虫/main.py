from DrissionPage import ChromiumPage
import re
import pandas as pd

driver = ChromiumPage()
Xreal_beam_pro_url = 'https://detail.tmall.com/item.htm?spm=a21n57.1.item.2.3b4a5325fap7JU&priceTId=2147813017210377164087471ea11c&utparam=%7B%22aplus_abtest%22:%22a5736e758474a155ced3b085925c0e39%22%7D&id=792822950990&ns=1&abbucket=4'
雷鸟魔盒_url = 'https://detail.tmall.com/item.htm?spm=a21n57.1.item.1.678f648aU6vIz5&priceTId=2147827717210564582591619e4175&utparam=%7B%22aplus_abtest%22:%22edbb818f6c2e6bdb7db7b8eeb3f99fe3%22%7D&id=793452108891&ns=1&abbucket=4'
ROKID_AR_LITE_url = 'https://detail.tmall.com/item.htm?spm=a21n57.1.item.1.4fcc1ffagD2LHW&priceTId=215041e017210565332056984e634a&utparam=%7B%22aplus_abtest%22:%225b6c95ba86b1d206f1c9b1cce1b9cc68%22%7D&id=787332669759&ns=1&abbucket=4&skuId=5376217093647'
driver.get(Xreal_beam_pro_url)
driver.listen.start('https://h5api.m.tmall.com/h5/mtop.alibaba.review.list.for.new.pc.detail/1.0/?jsv=')
driver.ele('css:.ShowButton--showButton--YUEsNpz').click(by_js=True)
driver.wait(2)

url_list = []
for i in range(7):
    res = driver.listen.wait()
    url_list.append(res.url)
# url_list1 = []
# 创建一个空的DataFrame
df = pd.DataFrame(columns=["Value"])

# 收集所有要添加到DataFrame的数据
data_to_append = []

for i in range(7):
    driver = ChromiumPage()
    driver.get(url_list[i])
    resp = driver.listen.wait()  # 确保listen.wait()是正确的调用方式
    text = resp.response.body

    # 正则表达式查找所有匹配项
    values = re.findall(r'"reviewWordContent":"(.*?)"', text, re.DOTALL)

    for value in values:
        data_to_append.append({"Value": value})

    # 使用pd.concat一次性添加所有数据到DataFrame
df = pd.concat([df, pd.DataFrame(data_to_append)], ignore_index=True)

    # 保存DataFrame到Excel文件
df.to_excel("Xreal beam pro.xlsx", index=False)
# df.to_excel("雷鸟魔盒.xlsx", index=False)
# df.to_excel("ROKID AR LITE.xlsx", index=False)

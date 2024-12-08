from aip import AipOcr

""" 你的 APPID AK SK """
APP_ID = '115684026'
API_KEY = 'ETJzZirHn2RTV9dERihNscEr'
SECRET_KEY = 'xAWLClWKupwt8oh4I44LfipivzHYndyO'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
print(client)

""" 读取文件 """


def get_file_content(filePath):
    with open(filePath, "rb") as fp:
        return fp.read()


image = get_file_content('syh1.png')

res = client.
res_image = client.basicGeneral(image)
for i in res_image['words_result']:
    print(i['words'])




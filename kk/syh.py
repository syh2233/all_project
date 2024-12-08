from aip import AipImageClassify

""" 你的 APPID AK SK """
APP_ID = '115829818'
API_KEY = 'fCYxh0APk3yYbUp2vcH0Cfcj'
SECRET_KEY = 'mVRnOx7JAtWekI7fe3feT5zwTkuO8Jxo'

client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)
print(client)

# def get_file_content(filePath):
#     with open(filePath, "rb") as fp:
#         return fp.read()
#
#
# image = get_file_content('syh.png')
# res_image = client(image)
# print(res_image)
import re
import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm

base_url = "https://movie.douban.com/subject/36877322/comments"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

with open('默杀影评.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['用户名', '评论时间', '评论地点', '评论内容'])

    for page in tqdm(range(10), desc="爬取进度"):
        start = page * 20
        url = f"{base_url}?start={start}&limit=20&status=P&sort=new_score"
        response = requests.get(url, headers=headers, timeout=2)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            comments = soup.find_all('div', class_='comment')

            for comment in comments:
                username = comment.find('a',
                                        href=re.compile(r'https://www.douban.com/people/*/')).text.strip() if comment.find(
                    'a', href=re.compile(r'https://www.douban.com/people/*/')) else '未知'
                comment_time = comment.find('span', class_='comment-time').text.strip() if comment.find('span',
                                                                                                        class_='comment-time') else '未知'
                comment_location = comment.find('span', class_='comment-location').text.strip() if comment.find('span',
                                                                                                                class_='comment-location') else '未知'
                comment_content = comment.find('span', class_='short').text.strip() if comment.find('span',
                                                                                                    class_='short') else '未知'
                writer.writerow([username, comment_time, comment_location, comment_content])
        else:
            print(f"请求失败，状态码：{response.status_code}")

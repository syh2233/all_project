import threading
import book1
import time



def ss(url):
    book1.book(url)


def url_thread():
    print("begin")
    url_list = []
    for url in list:
        url_list.append(
            threading.Thread(target=ss, args=(url,))
        )
    print(url_list)


    for thread in url_list:
        thread.start()

    for thread in url_list:
        thread.join()

    print("end")

if __name__ == "__main__":
    list = []
    for url_t in range(1, 6):
        list.append(
            f'https://booktoki349.com/novel/p{url_t}?sst=as_update&sod=desc&book=%EC%9D%BC%EB%B0%98%EC%86%8C%EC%84%A4|{url_t}')
        url_t += 1
    stat = time.time()
    url_thread()
    end = time.time()
    print("time:", end - stat, )


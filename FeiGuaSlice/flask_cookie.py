import os
from flask import Flask, request
from puppeteer_login import zz_main


def run_cookie():
    username = "19921970501"  # 淘宝用户名
    pwd = "pr1714"  # 密码
    url = 'https://dy.feigua.cn/home/price'
    cookie = zz_main(username, pwd, url)
    # print(cookie)
    return cookie


# cookie = run_cookie()
# print(cookie)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    if os.path.exists('cookie.txt'):
        os.remove('cookie.txt')
        print('cookie删除成功!!!')
        # print('读取cookie')
        # with open('cookie.txt', 'r', encoding='utf-8') as file:
        #     cookie = file.read()
    cookie = run_cookie()
    print(cookie)
    return cookie


if __name__ == "__main__":
    # app.run(debug=True, threaded=True)  # 开启多线程
    app.run()

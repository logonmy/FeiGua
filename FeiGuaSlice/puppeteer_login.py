import time
import random
import asyncio, requests
from pyppeteer.launcher import launch  # 控制模拟浏览器用
from fake_useragent import UserAgent

ua = UserAgent().random


def input_time_random():
    return random.randint(100, 151)


def screen_size():
    """使用tkinter获取屏幕大小"""
    import tkinter
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    return width, height


# 获取登录后cookie
async def get_cookie(page):
    print('开始保存cookie!!!')
    cookies_list = await page.cookies()
    cookies = ''
    for cookie in cookies_list:
        str_cookie = '{0}={1};'
        str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
        cookies += str_cookie
    with open('cookie.txt', 'w', encoding='utf-8') as f:
        f.write(cookies)
    return cookies


async def inject_js(page):
    js1 = "() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => undefined } }) }"
    js2 = "() =>{ window.navigator.chrome = { runtime: {},  }; }"
    js3 = "() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }"
    js4 = "() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }"
    await page.evaluateOnNewDocument(js1)
    await page.evaluateOnNewDocument(js2)
    await page.evaluateOnNewDocument(js3)
    await page.evaluateOnNewDocument(js4)


def retry_if_result_none(result):
    return result is None


async def mouse_slide(page=None, frame=None):
    print('mouse_slide')
    try:
        if frame:
            await frame.hover("#nc_1_n1z")
        else:
            print('开始滑动!!!')
            time.sleep(2)
            await page.hover("#nc_1_n1z")
            await page.mouse.down()
            await page.mouse.move(2000, 0, {"delay": random.randint(1000, 2000)})
            # await page.mouse.move(2000, 0, {"steps": random.randint(1000, 2000)})
            await page.mouse.up()
    except Exception as e:
        print("mouse error retry... or please check your code")
        return None
    else:
        await asyncio.sleep(random.uniform(1, 2))
        # 判断是否通过
        slider_result = ""
        time.sleep(2)
        try:
            slider_result = await page.Jeval(".nc-lang-cnt", "node => node.textContent")
            print(slider_result)
        except Exception as e:
            pass
        if slider_result == "加载中":
            time.sleep(2)
        if slider_result != "验证通过":
            print("verify fail error info:", slider_result)  # TODO
            return None, page
        else:
            print("verify pass")
            return 1, page


# 点击登陆
async def click_login(page, username, pwd):
    """
        1 作为一个整体，因是异步，导航等待触发，去执行点击操作，点击操作完，触发导航结束
        2 只有导航结束才能进行登陆结果判断
        3 看到其他大神写的是先按回车键，不是很明白，模拟回车键相当于登陆了，页面跳转后执行点击就会报错，所以这儿直接把回车操作干掉，有点疑惑，还希望懂的老哥指点一下
    """
    # await asyncio.gather(page.waitForNavigation(), page.evaluate("document.getElementById('J_SubmitStatic').click()"))
    await asyncio.gather(page.waitForNavigation(), page.evaluate(
        'document.querySelector("#js-phone-login > a.btn-login.js-account-logon").click()'))
    # 检测点击登陆后是否出现滑块验证
    print('已经点击登录!!!')
    # await get_cookie(page)
    return await get_cookie(page)


# 点击登陆 原版
async def click_login_old(page, username, pwd):
    """
    	1 作为一个整体，因是异步，导航等待触发，去执行点击操作，点击操作完，触发导航结束
        2 只有导航结束才能进行登陆结果判断
        3 看到其他大神写的是先按回车键，不是很明白，模拟回车键相当于登陆了，页面跳转后执行点击就会报错，所以这儿直接把回车操作干掉，有点疑惑，还希望懂的老哥指点一下
    """
    # await asyncio.gather(page.waitForNavigation(), page.evaluate("document.getElementById('J_SubmitStatic').click()"))
    await asyncio.gather(page.waitForNavigation(), page.evaluate(
        'document.querySelector("#js-phone-login > a.btn-login.js-account-logon").click()'))
    # 检测点击登陆后是否出现滑块验证
    print('已经点击登录!!!')
    try:
        slider = await page.Jeval("#acs-profile", "node => node.style")
        if slider:
            print("after click login slider appear")
            flag, page = await mouse_slide(page)
            if flag:
                # 点击登陆出现滑块验证，密码框是被清空的，所以需要重新输入密码
                await page.type("#TPL_password_1", pwd, {"delay": input_time_random()})
                await asyncio.gather(page.waitForNavigation(),
                                     page.evaluate(
                                         'document.querySelector("#js-phone-login > a.btn-login.js-account-logon").click()'))
                try:
                    await page.waitForSelector(".account-id", {"timeout": 15000})
                    print(page.url)
                    return await get_cookie(page)
                except:
                    print("timeout wait for element: .account-id")
                    return
    except:
        print('点击登录,滑块成功!!!')
        pass

    # 检测是否有账号密码错误
    print('检查是否有账号密码错误!!!')
    try:
        global error
        error = await page.Jeval("#J_Message .error", "node => node.textContent")
        print("error:", error)
        print("account_info:", username)
    except Exception as e:
        error = None
    finally:
        if error:
            print("确保账号安全重新输入")
        else:
            try:
                # 等待登陆成功页面某一元素的出现
                print('okk')
                await page.waitForSelector(".account-id", {"timeout": 10000})
                print(page.url)
                return await get_cookie(page)
            except:
                print("timeout wait for element: .account-id")


async def main(username, pwd, url):
    width, height = screen_size()
    browser = await launch({
        "headless": False,
        # 重新指定临时数据路径，解决windows系统 OSError: Unable to remove Temporary User Data报错问题
        # "userDataDir": r"F:\temporary",
        # 有头的不要加这句话，容易导致浏览器进程无法结束
        "args": [f'--window-size={width},{height}', '--disable-infobars'],  # ['--no-sandbox'],
        'dumpio': True},
        handleSIGINT=False,  # 这三个可以使flask调用puppeteer
        handleSIGTERM=False,
        handleSIGHUP=False
    )  # "dumpio": True 解决浏览器卡住问题
    """浏览器启动的时候，自动使用cookies信息或者缓存填写了账号输入框，通过系新建上下文，可以解决多个浏览器数据共享的问题，暂时没想到其他的解决方案"""
    context = await browser.createIncognitoBrowserContext()
    page = await context.newPage()
    await page.setViewport({  # 最大化窗口
        "width": width,
        "height": height
    })
    # page = await browser.newPage() # 启动个新的浏览器页面
    # 新定义的注入js函数每次导航或者加载新的页面时会自动执行js注入 比起page.evaluate()每打开一个页面都要单独注入一次好用
    await inject_js(page)
    await page.setUserAgent(ua)
    # goto到指定网页并且等到网络空闲为止
    await page.goto(url)
    time.sleep(5)
    # await page.evaluate('''document.getElementById("J_Quick2Static").click()''')
    # 点击登录注册
    login_click = await page.xpath('//a[text()="登录/注册"]')
    await login_click[0].click()
    time.sleep(1)
    phone_login = await page.xpath('//div[@class="login-code"]//a[text()="手机登录"]')
    await phone_login[0].click()
    time.sleep(3)
    # await page.type("#fm-login-id", username, {"delay": input_time_random() - 60})  # 毫秒
    # await page.type("#fm-login-password", pwd, {"delay": input_time_random()})
    await page.evaluate(
        '''document.querySelector("#js-phone-login > form > div:nth-child(1) > input[type=text]").value="19921970501";''')
    time.sleep(2)
    await page.evaluate(
        '''document.querySelector("#js-phone-login > form > div:nth-child(2) > input[type=password]").value="pr1714";''')
    await asyncio.sleep(random.random() + 0.5)  # 毫秒
    print('账号密码已经输入!!!')
    submit_login = await page.xpath('//a[text()="登 录"]')
    await submit_login[0].click()
    print('开始判断有无滑块!!!')
    # 判断是否有滑块
    slider = await page.Jeval("#acs-profile", "node => node.style")
    # slider = await page.querySelector("#acs-profile")
    # resp = await page.content()  # 页面元素内容
    # print(resp)
    if slider:
        print("slider appear")
        flag, page = await mouse_slide(page=page)
        ############################################33
        # # 处理刷新重新验证的情况
        # fresh = ""
        # try:
        #     fresh = await page.Jeval(".errloading", "node => node.textContent")
        # except:
        #     pass
        # if fresh:
        #     # 刷新滑块验证
        #     await page.hover("a[href='javascript:noCaptcha.reset(1)']")  # 模拟鼠标移动到被选择元素上
        #     await page.mouse.down()
        #     await page.mouse.up()
        #     await asyncio.sleep(random.uniform(1, 2))
        #     try:
        #         # page.J相当于page.querySelector()
        #         await page.J(".nc-lang-cnt[data-nc-lang='_startTEXT']")
        #         print("refresh slider success: begin verify slide again...")
        #         # 二次滑块验证
        #         flag, page = await mouse_slide(page=page)
        #         if flag:
        #             await click_login(page, username, pwd)
        #         else:
        #             await browser.close()
        #             print("second verify slider faild: quit")
        #             return
        #     except:
        #         print("refresh slider failed: please check your code")
        #         return
        # if flag:
        #     await click_login(page, username, pwd)
        # else:
        #     print("login failed: please check out your code")
        #     return
        # 针对飞瓜写
        if flag:
            print('haha')
            cookie = await click_login(page, username, pwd)
            print('登录成功!!!')
            # print(cookie)
            time.sleep(3)
            await browser.close()
            return cookie
        else:
            print('登录失败!!!')

    else:
        print("No slider")
        await click_login(page, username, pwd)
    # time.sleep(50)
    # await get_cookie(page)

    # time.sleep(5)
    # await browser.close()


def zz_main(username, pwd, url):
    # 这两行解决async 运行多线程时报错RuntimeError: There is no current event loop in thread 'Thread-2'
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    # loop = asyncio.get_event_loop()  # 协程，开启个无限循环的程序流程，把一些函数注册到事件循环上。当满足事件发生的时候，调用相应的协程函数。
    m = main(username, pwd, url)
    # loop.run_until_complete(m)  # 将协程注册到事件循环，并启动事件循环
    # 下方代码获取返回值
    get_future = asyncio.ensure_future(m)  # 相当于开启一个future
    # loop.run_until_complete(get_future)  # 事件循环

    new_loop.run_until_complete(get_future)  # 事件循环
    # print('最后:', get_future.result())
    return get_future.result()


if __name__ == '__main__':
    # username = "19921970501"  # 淘宝用户名
    username = "18854869806"  # 飞瓜用户名
    # pwd = "pr1714"  # 密码
    pwd = "wendy123456"  # 密码
    url = 'https://dy.feigua.cn/home/price'
    cookie = zz_main(username, pwd, url)
    print('最后:', cookie)

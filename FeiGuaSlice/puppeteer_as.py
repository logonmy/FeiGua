# -*- coding:utf-8 -*-
import asyncio
from pyppeteer import launch, chromium_downloader


def screen_size():
    '使用tkinter获取屏幕大小'
    import tkinter
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    return width, height


async def main():
    width, height = screen_size()
    '''
    利用launch方法传入args设定窗口大小，而后面那个disable-infobars则是去除那个浏览器的“chrome当前正在受自动化测试软件控制”这个选项卡
    '''
    browser = await launch(headless=False, args=[f'--window-size={width},{height}', '--disable-infobars'])
    page = await browser.newPage()
    # 设置请求头userAgent
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36')
    # 最大化窗口
    await page.setViewport({
        'width': width,
        'height': height
    })
    await page.goto('http://www.baidu.com/')
    await asyncio.sleep(10)
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())


######### xpath
import os

os.environ['PYPPETEER_HOME'] = 'D:\Program Files'
import asyncio
from pyppeteer import launch


def screen_size():
    """使用tkinter获取屏幕大小"""
    import tkinter
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    return width, height


async def main():
    js1 = '''() =>{

        Object.defineProperties(navigator,{
        webdriver:{
            get: () => false
            }
        })
    }'''

    js2 = '''() => {
        alert (
            window.navigator.webdriver
        )
    }'''
    browser = await launch({'headless': False, 'args': ['--no-sandbox'], })

    page = await browser.newPage()
    width, height = screen_size()
    await page.setViewport({  # 最大化窗口
        "width": width,
        "height": height
    })
    await page.goto('https://h5.ele.me/login/')
    await page.evaluate(js1)
    await page.evaluate(js2)
    input_sjh = await page.xpath('//form/section[1]/input[1]')
    click_yzm = await page.xpath('//form/section[1]/button[1]')
    input_yzm = await page.xpath('//form/section[2]/input[1]')
    but = await page.xpath('//form/section[2]/input[1]')
    print(input_sjh)
    await input_sjh[0].type('*****手机号********')
    await click_yzm[0].click()
    ya = input('请输入验证码：')
    await input_yzm[0].type(str(ya))
    await but[0].click()
    await asyncio.sleep(3)
    await page.goto('https://www.ele.me/home/')
    await asyncio.sleep(100)
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
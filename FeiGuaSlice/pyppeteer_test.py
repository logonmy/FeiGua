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
    resp = await page.content()
    print(resp)
    await asyncio.sleep(10)
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
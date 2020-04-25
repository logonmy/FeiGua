import random
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumTest(object):
    """用来测试selenium相关脚本"""

    def __init__(self):
        self.url = "https://dy.feigua.cn/home/price"
        self.__options = webdriver.ChromeOptions()
        self.__options.binary_location = "F:\chrome-win\chrome.exe"
        # self.__options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # self.__options.add_experimental_option('useAutomationExtension', False)
        self.__options.add_argument('--window-size=1920x1080')
        self.driver = webdriver.Chrome(chrome_options=self.__options)
        # 过检测
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })

        # # 过检测准备工作
        # self.execute_chrome_protocol_js(
        #     protocol="Page.addScriptToEvaluateOnNewDocument",
        #     params={"source": """
        #            Object.defineProperty(navigator, 'webdriver', {
        #            get: () => false,
        #            });"""})
        # self.__options.binary_location = "C:\chrome-win\chrome.exe"
        # self.__options.add_argument('--dns-prefetch-disable')
        # self.__options.add_argument('--disable-gpu')  # 规避bug
        # self.__options.add_argument('--user-agent={}'.format(
        #     'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'))
        # self.__options.add_argument('--user-agent={}'.format(ua()))
        # self.__options.add_argument('--headless')
        # self.__options.add_argument('window-size=1920x1080')
        # self.__options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
        # self.__options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
        # self.__options.add_argument('--no-sandbox')
        # self.__options.add_argument('--disable-gpu')
        # self.__options.add_argument('--disable-dev-shm-usage')
        # self.pref = {'profile.managed_default_content_settings.images': 2}
        # self.__options.add_experimental_option('prefs', self.pref)
        # self.__options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # self.driver = webdriver.Chrome(chrome_options=self.__options)
        self.wait = WebDriverWait(self.driver, 20, 0.5)

    def get_data(self):
        """请求页面"""
        self.driver.get(self.url)
        time.sleep(random.uniform(0.5, 1))
        # click_login_js = 'document.querySelector("body > div.header.headerScroll.eye-protector-processed > div > div > a").click()'
        # self.driver.execute_script(click_login_js)
        self.driver.find_element_by_xpath('//a[text()="登录/注册"]').click()
        time.sleep(random.uniform(0.5, 1))
        self.driver.find_element_by_xpath('//div[@class="login-code"]//a[text()="手机登录"]').click()
        time.sleep(random.uniform(0.5, 1))
        input_user_js = 'document.querySelector("#js-phone-login > form > div:nth-child(1) > input[type=text]").value="19921970501";'
        input_pwd_js = 'document.querySelector("#js-phone-login > form > div:nth-child(2) > input[type=password]").value="123456";'
        self.driver.execute_script(input_user_js)
        time.sleep(random.uniform(0.5, 1))
        self.driver.execute_script(input_pwd_js)
        time.sleep(random.uniform(0.5, 1))
        login_js = 'document.querySelector("#js-phone-login > a.btn-login.js-account-logon").click();'
        self.driver.execute_script(login_js)
        # time.sleep(random.uniform(0.5, 1))
        # for i in range(1, 5):
        #     distance = i * 80
        #     slice_js = 'document.getElementById("nc_1_n1z").style.left="{}px";document.getElementById("nc_1__bg").style.width="{}px";'.format(str(distance), str(distance))
        #     self.driver.execute_script(slice_js)
        # # self.wait.until(EC.presence_of_element_located((By.ID, "nc_1_n1z")))
        #     time.sleep(random.uniform(0.5, 1))
        # login_js = 'document.querySelector("#js-phone-login > a.btn-login.js-account-logon").click();'
        # self.driver.execute_script(login_js)

if __name__ == "__main__":
    st = SeleniumTest()
    st.get_data()

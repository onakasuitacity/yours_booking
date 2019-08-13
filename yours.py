# import
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # http://www.seleniumqref.com/api/python/element_set/Python_special_send_keys.html
from selenium.webdriver.support.ui import Select # https://qiita.com/redoriva/items/aa9fa4c0bf2aeb8e1bff
from selenium.webdriver.chrome.options import Options # https://qiita.com/orangain/items/db4594113c04e8801aad
from selenium.webdriver.common.by import By # https://kurozumi.github.io/selenium-python/locating-elements.html
import time
import datetime as dt
import getpass

# constants
today = int(dt.datetime.strptime(str(dt.date.today()),"%Y-%m-%d").timestamp())
endtimes = [today + 43800 + 600*k for k in range(2)] + [today + 47400 + 600*k for k in range(2)]
strict_endtimes = [today + 43800, today + 47400]
limit_datetime = dt.datetime.strptime(str(dt.date.today()),"%Y-%m-%d") + dt.timedelta(hours=11)
flag = False

# webdriver configuration
options = Options()
options.add_argument("--headless")
options.add_argument("--incognito") # シークレットモード
driver = webdriver.Chrome("ENTER YOUR CHROMEDRIVE PATH", options=options)
driver.implicitly_wait(2) # 主に予約枠のaタグの要素が取得できるようになるまでの最大許容時間。更新頻度も兼ねている。

# login information
mail = input("Enter your e-mail address : ")
password = getpass.getpass(prompt="Password : ")

# processing
try:
    # login
    driver.get("https://esp03.dt-r.com/gmo-yours/member/login.php")
    driver.find_element(By.NAME, "login_id").send_keys(mail)
    driver.find_element(By.NAME, "login_passwd").send_keys(password)
    driver.find_element(By.CLASS_NAME, "button_next").click()
    
    if driver.current_url[-3:] != "php":
        print("Logged in successfully.")
    else:
        print("Login information was wrong.")
        raise ValueError()
    
    # booking
    driver.get("https://esp03.dt-r.com/gmo-yours/booking/booking.php?search_main_plan_id=1")
    
    while(dt.datetime.now() < limit_datetime):
        driver.refresh()
        
        # 下記aタグが存在する＝予約に空きがある
        elements = driver.find_elements(By.CSS_SELECTOR, "#calendar_table_area>table>tbody>tr:nth-child(2)>td:nth-child(2)>a")
        if len(elements):
            for element in elements:
                URL = element.get_attribute("href")
                if int(URL[-10:]) in endtimes: # unixtimeで判断
                    driver.get(URL)

                    # 予約する
                    driver.find_element(By.CLASS_NAME, "button_next").click()

                    # 予約できたか確認。できてない場合はURLにパラメータとして?err_no=1などがつくため、末尾がphpかどうかで判断
                    if driver.current_url[-3:] == "php":
                        if int(URL[-10:]) in strict_endtimes:
                            print("Booked successfully in strict time.")
                            flag = True # 処理を終わるための準備

                            if endtimes == strict_endtimes: # 予約を同日に2つ取っているので、先に取った方をキャンセルする
                                driver.get("https://esp03.dt-r.com/gmo-yours/member/booking_list.php?mode=reservation")
                                driver.find_element(By.CSS_SELECTOR, "#info_list>tbody>tr:nth-child(3)>td:nth-child(5)>a>div").click()
                                # キャンセルする
                                driver.find_element(By.CLASS_NAME, "button_next").click()
                            
                            break # for loopから抜ける

                        else:
                            print("Booked successfully, but not in strict time.")
                            print("Continue to try to book in strict time.")
                            endtimes = strict_endtimes
                            # 予約ページに戻ってやり直す
                            driver.get("https://esp03.dt-r.com/gmo-yours/booking/booking.php?search_main_plan_id=1")
                    else:
                        # 予約ページに戻ってやり直す
                        driver.get("https://esp03.dt-r.com/gmo-yours/booking/booking.php?search_main_plan_id=1")
            
            if flag:
                break # while loopから抜ける
    
except:
    print("Raised some error.")

driver.quit()

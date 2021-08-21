# coding:utf-8
# 載入需要的套件
import time
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import pandas as pd

# 資料陣列
list_restaurant = []
list_adrress = []
list_opening_hours = []
list_contact = []
list_total_star = []
list_person = []
list_star = []
list_date = []
list_review = []
list_thumb = []

def scrapGooelgMap(keyword):
    print("scrapGooelgMap init.")

    # 開啟瀏覽器視窗(Chrome)
    print("開啟Chrome.")
    driver = webdriver.Chrome(executable_path = "./chromedriver")
    # 開啟瀏覽器視窗(Chrome) 無頭模式
    # option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    # driver = webdriver.Chrome(executable_path = r'.\chromedriver.exe', chrome_options = option)

    # 更改網址以前往不同網頁
    print("前往Google Map.")
    driver.get("https://www.google.com/maps/@22.707076,120.4380425,10.46z")

    # 定位搜尋框
    #element = driver.find_element_by_class_name("gLFyf.gsfi")
    element = driver.find_element_by_id("searchboxinput")

    #---TODO---寫成方法讓他自動跑迴圈send_keys<餐廳資料>
    # 傳入字串
    print("傳送Kerword[" + keyword + "].")
    element.send_keys(keyword)
    # 清除字串
    # element.clear()
    #搜尋
    #button = driver.find_element_by_class_name("gNO89b")
    button = driver.find_element_by_id("searchbox-searchbutton")
    print("點擊搜尋.")
    button.click()

    # Loading
    time.sleep(5)
    #判斷是否直接進入餐廳資訊頁
    while True:
        url = driver.current_url
        # print(url[-13:])
        if(url[-13:] == "data=!3m1!4b1"):
            time.sleep(5)
            items = driver.find_element_by_xpath("//*[@id='pane']/div/div[1]/div/div/div[last()]/div[1]/div[1]/div/a")      
            # cd C:\Users\Cathy\OneDrive\桌面\zhong\
            # link = items.get_attribute("href")
            # print(link)s
            items.click()
            print('<Loading Succuss>已定位到元素')
            break
        elif'data' not in url:
            #driver.refresh()
            button.click()
            time.sleep(3)
        else:    
            # print(url)
            print('進入餐廳')
            break

    #抓取餐廳資訊
    time.sleep(5)
    try:
        soup = BeautifulSoup(driver.page_source,'html.parser')
        #print(soup)
        time.sleep(2)
        restaurant = soup.find('h1',{"class":'section-hero-header-title-title gm2-headline-5'}).find('span').text
        adrress = soup.find('div',{"class":'ugiz4pqJLAG__primary-text gm2-body-2'}).text
        opening_hours = soup.find('div',{"class":'section-open-hours-container cX2WmPgCkHi__container-hoverable'}).get('aria-label')
        contact_1 = soup.find('button',{"data-tooltip":'複製電話號碼'})
        contact=contact_1.find('div',{"class":'ugiz4pqJLAG__primary-text gm2-body-2'}).text
        #contact = soup.find('div',{"class":'ugiz4pqJLAG__primary-text gm2-body-2'}).text
        total_star = soup.find('span',{"class":'fFNwM35iXVH__section-star-display'}).text
    #    print(restaurant)
    #    print(adrress)
    #    print(opening_hours)
    #    print(contact)
    #    print(total_star)
    except:
      driver.refresh()
    print(restaurant)
    print(adrress)
    print(opening_hours)
    print(contact)
    print(total_star)
    time.sleep(5)
    # More Comment
    #將評論由新到舊排序
    while True:
        try:
            time.sleep(5)
            #driver.find_element_by_class_name('widget-pane-link').click()
            # try:
            #     sort = driver.find_element_by_xpath("//*[@id='pane']/div/div[1]/div/div/div[34]/div[2]/div")
            # except:
            #     sort = driver.find_element_by_xpath("//*[@id='pane']/div/div[1]/div/div/div[35]/div[2]/div")
            #sort = driver.find_element_by_xpath("//div[@data-value='排序']")            
            sort = driver.find_element_by_css_selector("[data-value='排序']")

            #sore = driver.find_element_by_link_text("排序")
            sort.click()
            time.sleep(2)
            sort_lastest = driver.find_element_by_xpath("//*[@id='action-menu']/ul/li[2]")
            sort_lastest.click() 
            print('<More Comment Success>已定位到元素')
            break
        except:
            print("<More Comment Faild>尚未定位到元素!")
              

    # get current url
    time.sleep(1)
    print (driver.current_url)
    print('<get url>已定位到元素')

    # 獲取網頁原始碼
    print("取得網頁原始碼")
    soup = BeautifulSoup(driver.page_source,'html.parser')
    #print(soup)

    time.sleep(3)
    # 評論分頁
#    pane = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[3]')
    pane = driver.find_element_by_class_name('section-layout.section-scrollbox.mapsConsumerUiCommonScrollable__scrollable-y.mapsConsumerUiCommonScrollable__scrollable-show')
    stop_loading=False
    while stop_loading == False :
        print("模擬滑鼠下滑")
        # 如果時間有年這個字 停止下滑
        soup = BeautifulSoup(driver.page_source,'html.parser')    
        spans=soup.find_all('span',{"class":'section-review-publish-date'})
        date_range = [span.get_text() for span in spans]
        if len(spans)>500:
            stop_loading=True
        # print (date_range)
        for i in date_range :
            # print(i)
            if '年' in i: # 正式是年 測試是月
                print("已取得年跳出迴圈")
                stop_loading = True
            # else:
            #     print('OK')
        #評論分頁下滑
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pane)
        time.sleep(1)
        
    # 獲取評論資料框架
    all_reviews = soup.find_all('div',{"class":'section-review mapsConsumerUiCommonRipple__ripple-container gm2-body-2'})
    # 以第一則評論為例
    # ar = all_reviews[0] # 第幾則評論
    # count = 0
    #print(ar)
    count = 0
    for ar in all_reviews:
        person = ar.find('div',{"class":'section-review-title'}).find('span').text
        star = ar.find('span',{"class":'section-review-stars'}).get('aria-label')
        date = ar.find('span',{"class":'section-review-publish-date'}).text
        review = ar.find('span',{"class":'section-review-text'}).text
        try:
            thumb = ar.find('span',{"class":'section-review-thumbs-up-count'}).text
        except:
            thumb = '0'
        #---TODO---寫入陣列縫起來
        if '年' not in date:
            count += 1
            print("資料寫入List [第" + str(count) + "筆]")
            list_restaurant.append(restaurant)
            list_adrress.append(adrress)
            list_opening_hours.append(opening_hours)
            list_contact.append(contact)
            list_total_star.append(total_star)
            list_person.append(person)
            list_star.append(star)
            list_date.append(date)
            list_review.append(review)
            list_thumb.append(thumb)

    # print(len(person))
    # print(star)
    # print(date)
    # print(review)
    # print(thumb)
    # print(count)


    #返回上一頁
    #driver.back()
    # 關閉瀏覽器視窗
    driver.close() 

    # 評論分頁下滑
    # pane = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]')
    # driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pane)

if __name__ == '__main__':
    # Keyword
    top_restaurant = ['七賢路鴨肉飯', '鴨肉珍', '老牌周燒肉飯', '香園牛肉麵', '老二腿庫飯', 
                    '仁武烤鴨', '大高雄鵝肉', '橋頭太成肉包', '小雅茶飲', '品元糖口']
    
    #scrapGooelgMap(top_restaurant[9])
    for i in top_restaurant:
        scrapGooelgMap(i)

    # print(list_restaurant)
    # print(list_adrress)
    # print(list_opening_hours)
    # print(list_contact)
    # print(list_total_star)
    # print(list_person)
    # print(list_star)
    # print(list_date)
    # print(list_review)
    # print(list_thumb)

    print("匯出zip .CSV")
    data = zip(list_restaurant, 
               list_adrress, 
               list_opening_hours,
               list_contact,
               list_total_star,
               list_person,
               list_star,
               list_date,
               list_review,
               list_thumb)
    df = pd.DataFrame(list(data), 
                      columns = ['Restaurant',
                                 'Adrress',
                                 'Opening_Hours',
                                 'Contact',
                                 'Total_Star',
                                 'Person',
                                 'Star',
                                 'Date',
                                 'Review',
                                 'Thumb'])
    df.to_csv('Export.csv', sep='|', index = None)
    print("程式執行結束.")
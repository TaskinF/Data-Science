from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as BS
import pandas as pd
import time

months = { 1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}

dates = [ "2023-4"]#enter the dates you want to scrape

def render_page(url,type):
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(7)
    if type =="C":
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'wuSettings'))
        )
        element.click()
        time.sleep(7)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="wuSettings-quick"]/div/a[2]')))
        element.click()
        time.sleep(7)
        r = driver.page_source
        print("wait for the page to load")
        time.sleep(10)
        driver.quit()
    elif type=="F":
        r = driver.page_source

        print("wait for the page to load")
        time.sleep(10)

        driver.quit()

    return r

def get_head(container):
    head = container.find('thead')
    
    data_head = []
    for i in head.find_all('td'):
        data_head.append(i.get_text())
    return data_head
     

def get_data(page,dates,type):
    
    for d in dates:
            day_number = months[int(d.split("-")[1])]
            time.sleep(4)
            print( "starting " + str(d))
            output = pd.DataFrame()
             
            url = str(str(page) + str(d))

            r = render_page(url,type)

            soup = BS(r, "html.parser",)
            container = soup.find('lib-city-history-observation')
            check = container.find('tbody')
            
            data_head = get_head(container)
            print(data_head)

            nocheck = check.find('tr')

            data_body= []
            count = 0
            data  = nocheck.find_all('tr', class_='ng-star-inserted')
            for i in data:
                    
                    if count>day_number and count<len(data)-(day_number+1):
                        trial = i.get_text().split(" ")
                        data_body.append(trial[3])
                       
                    else:
                        trial = i.get_text()
                        data_body.append(trial)
                        
                    count+=1

            for i in range(len(data_body)//(day_number+1)):
                output[data_head[i]] = data_body[i*(day_number+1)+1:(i+1)*(day_number+1)]
            
            output.to_csv(str(d)+"1.csv", index = False, header=True)
            print(str(str(d) + ' finished!'))
           
    return output
    
def create_dates(start, year):
    dates = []
    for i in range(year):
        for j in range(1,13):
            
                dates.append(str(start+i) + '-' + str(j))
        
    return dates

page = "https://www.wunderground.com/history/monthly/tr/gaziemir/LTBJ/date/"

# dates = create_dates(2020, 5)

monthly = get_data(page,dates,"C")
print(monthly)



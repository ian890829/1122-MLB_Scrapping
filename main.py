from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
import requests
import time
import csv

year = 2003
wtefile=[]
while(year<2024):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach',True)
    driver = webdriver.Chrome(options= options, service=Service(ChromeDriverManager().install()))
    path = 'https://www.mlb.com/stats/'+str(year)+'?playerPool=ALL'
    driver.get(path)
    d = requests.get(path)
    b = driver.find_element(By.ID,'onetrust-accept-btn-handler')
    b.click()
    time.sleep(2)

    dar = []

        
    while(True):
        #try:
        driver.implicitly_wait(20)
        standardc = driver.find_element(By.XPATH,'//*[@id="stats-app-root"]/section/section/div[3]/div[1]/div/table/tbody')
        try:
            landan=driver.find_element(By.XPATH,'/html/body/main/div[2]/section/section/div[3]/div[2]/div[1]')
        except:
            a=0
        if(landan.text=='Sorry, no results.'):
            driver.refresh()
            print("refreshing "+str(year))
            continue
        while(not any(c.isalpha() for c in standardc.text)):
            standardc = driver.find_element(By.XPATH,'//*[@id="stats-app-root"]/section/section/div[3]/div[1]/div/table/tbody')

        a = standardc.text.split('\n')
        
        for i in range(1,len(a),4):
            j = i+2
            b = a[j].split(' ')
            b.insert(0,a[i])
            b.insert(0,str(year))
            dar.append(b)
        try:
            time.sleep(1)
            standardd = driver.find_element(By.CSS_SELECTOR,"[aria-label = 'next page button']")
            standardd.click()
        except:
            break
        # except StaleElementReferenceException:
        #     continue

   
    #data = pd.DataFrame(dar,columns = ['Player','TEAM','G','AB','R','H','2B','3B','HR','RBI','BB','SO','SB','CS','AVG','OBP','SLG','OPS'])
    page1button = driver.find_element(By.XPATH,'/html/body/main/div[2]/section/section/div[3]/div[2]/div/div/div[2]/div[1]/button')
    page1button.click()

    expandbutton = driver.find_element(By.XPATH,'//*[@id="stats-app-root"]/section/section/div[1]/div[2]/div/div[1]/div/div[2]/button')
    expandbutton.click()

    dar2 = []

    while(True):
        driver.implicitly_wait(20)
        standardc = driver.find_element(By.XPATH,'//*[@id="stats-app-root"]/section/section/div[3]/div[1]/div/table/tbody')
        try:
            landan=driver.find_element(By.XPATH,'/html/body/main/div[2]/section/section/div[3]/div[2]/div[1]')        
            if(landan.text=='Sorry, no results.'):#No Result handling
                driver.refresh()
                print("refreshing "+str(year))
                continue
        except:
            a=0

        while(not any(c.isalpha() for c in standardc.text)):#empty text handling
            standardc = driver.find_element(By.XPATH,'//*[@id="stats-app-root"]/section/section/div[3]/div[1]/div/table/tbody')
        a = standardc.text.split('\n')
        for i in range(3,len(a),4):
            b = a[i].split(' ')
            del b[0]
            dar2.append(b)
        try:
            time.sleep(1)
            standardd = driver.find_element(By.CSS_SELECTOR,"[aria-label = 'next page button']")
            standardd.click()
        except:
            break

    for i in range(len(dar)):
        dar[i]+=dar2[i]
    csvfile="Player_Hittings23.csv"
    with open(csvfile,'a',newline="") as fp:
        writer=csv.writer(fp)
        if(year==2003):
            writer.writerow(['Year','Player','TEAM','G','AB','R','H','2B','3B','HR','RBI','BB','SO','SB','CS','AVG','OBP','SLG','OPS','PA','HBP','SAC','SF','GIDP','GO/AO','XBH','TB','IBB','BABIP','ISO','AB/HR','BB/K','BB%','SO%'])
        for row in dar:
            writer.writerow(row)
    year+=1
    driver.close()
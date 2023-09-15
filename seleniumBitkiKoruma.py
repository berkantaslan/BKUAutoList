from time import sleep
import pandas as pd
from selenium import webdriver
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import math
from tqdm import tqdm
import os
import sys

class getList:

    def __init__(self,
                link='https://bku.tarimorman.gov.tr/BKURuhsat/Index',
                driver='chrome',
                driver_path='chromedriver.exe'):
        """
        :param str link: link to acces to router login page
        :param str username: username to acces to router
        :param str password: password to acces to router
        :param str driver: browser name
        :param str driver_path: browser driver path
        :return:
        """
        self.link = link

        self.driver = driver

        self.driver_path = driver_path
        
        options = Options()
        
        options.add_argument('--disable-gpu')
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('disable-infobars')
        options.add_argument("--disable-extensions")
        options.add_argument('--disable-logging')
        options.add_argument('--disable-blink-features=AutomationControlled')
        # options.add_argument("--proxy-server='direct://'")
        # options.add_argument("--proxy-bypass-list=*")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--password-store=basic")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--enable-automation")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-xss-auditor")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-webgl")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("no-default-browser-check")
        options.add_argument("no-first-run")
        options.add_argument('log-level=3')
        options.add_argument('--ignore-ssl-errors')

        self.drivers = {'chrome':webdriver.Chrome}

        driver_service = Service(executable_path = "chromedriver.exe")

        browser = self.drivers[self.driver](service=driver_service, options=options)

        browser.implicitly_wait(10)

        browser.get(self.link)

        sleep(3)

        select = Select(browser.find_element(By.XPATH, ("//*[@id='tablo_length']/label/select")))

        select.select_by_value('100')

        sleep(3)

        webtable_df1 = pd.read_html(browser.find_element(By.XPATH, ("//*[@id='tablo']")).get_attribute('outerHTML'))[0]
        
        totalbku = browser.find_element(By.XPATH, ("//*[@id='tablo_info']")).get_attribute('outerHTML')
        
        ara1 = re.compile(r'\d.\d\d\d')
        
        ara2 = re.compile(r'\d\d.\d\d\d')
        
        ara3 = re.compile(r'\d\d\d.\d\d\d')
        
        if ara1.search(str(totalbku)):
        
            totalbku = ara1.search(str(totalbku))
            
        if ara2.search(str(totalbku)):
        
            totalbku = ara2.search(str(totalbku))
            
        if ara3.search(str(totalbku)):
        
            totalbku = ara3.search(str(totalbku))
        
        totalbku = int(str(totalbku.group()).replace('.', ''))
        
        totalpage = math.ceil(totalbku/100)
        
        button = browser.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/div[3]/div/table/tbody/tr[1]/td[8]/a")
        
        browser.execute_script('arguments[0].click()', button)
        
        ayrinti = pd.read_html(browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[2]/table")).get_attribute('outerHTML'))[0]
        
        ayrinti_df1 = ayrinti.transpose() # , index = ["Formulasyonu", "Aktif Madde", "Ruhsat Numarası", "Ruhsat Tarihi", "Ruhsat Grubu", "Raf Ömrü Süre", "Geçerlilik Süresi", "Ruhsat Sahibi Firma", "Adresi", "İthalatçı Firma / Üretici Firma", "Adresi"]
        
        ayrinti_df1.columns = ayrinti_df1.iloc[0]
        
        ayrinti_df1.drop(labels=0, axis=0, inplace=True, index=None)
        
        ayrinti_df1.reset_index(inplace=True)
        
        ayrinti_df1.drop(["index"], axis = 1, inplace = True)
        
        try:
                
            ayrinti_df1.drop(['Fabrika', 'Fabrika Adresi'], axis=1, inplace=True)
            
            ayrinti_df1.rename(columns={'Üretici Firma (Yabancı)': 'İthalatçı Firma / Üretici Firma'}, inplace=True)
        
        except:
            
            pass
        
        ayrinti_df = ayrinti_df1
        
        browser.back()
        
        for i in range(2, 101):

            button = browser.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/div[3]/div/table/tbody/tr[{0}]/td[8]/a".format(i))
        
            browser.execute_script('arguments[0].click()', button)
            
            ayrinti = pd.read_html(browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[2]/table")).get_attribute('outerHTML'))[0]
            
            ayrinti_df2 = ayrinti.transpose() # , index = ["Formulasyonu", "Aktif Madde", "Ruhsat Numarası", "Ruhsat Tarihi", "Ruhsat Grubu", "Raf Ömrü Süre", "Geçerlilik Süresi", "Ruhsat Sahibi Firma", "Adresi", "İthalatçı Firma / Üretici Firma", "Adresi"]
            
            ayrinti_df2.columns = ayrinti_df2.iloc[0]
            
            ayrinti_df2.drop(labels=0, axis=0, inplace=True, index=None)
            
            ayrinti_df2.reset_index(inplace=True)
            
            ayrinti_df2.drop(["index"], axis = 1, inplace = True)
            
            try:
                
                ayrinti_df2.drop(['Fabrika', 'Fabrika Adresi'], axis=1, inplace=True)
                
                ayrinti_df2.rename(columns={'Üretici Firma (Yabancı)': 'İthalatçı Firma / Üretici Firma'}, inplace=True)
            
            except:
                
                pass
            
            # sleep(1)
            
            browser.back()
            
            ayrinti_df = [ayrinti_df, ayrinti_df2]
            
            ayrinti_df = pd.concat(ayrinti_df, ignore_index=True)
            
        # print("Done 1/{0}".format(totalpage))
        
        button = browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[1]/div[4]/div/div/ul/li[9]/a"))
        
        browser.execute_script('arguments[0].click()', button)
            
        webtable_df2 = pd.read_html(browser.find_element(By.XPATH, ("//*[@id='tablo']")).get_attribute('outerHTML'))[0]
        
        button = browser.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/div[3]/div/table/tbody/tr[1]/td[8]/a")
        
        browser.execute_script('arguments[0].click()', button)
        
        ayrinti = pd.read_html(browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[2]/table")).get_attribute('outerHTML'))[0]
        
        ayrinti_df3 = ayrinti.transpose() # , index = ["Formulasyonu", "Aktif Madde", "Ruhsat Numarası", "Ruhsat Tarihi", "Ruhsat Grubu", "Raf Ömrü Süre", "Geçerlilik Süresi", "Ruhsat Sahibi Firma", "Adresi", "İthalatçı Firma / Üretici Firma", "Adresi"]
        
        ayrinti_df3.columns = ayrinti_df3.iloc[0]
        
        ayrinti_df3.drop(labels=0, axis=0, inplace=True, index=None)
        
        ayrinti_df3.reset_index(inplace=True)
        
        ayrinti_df3.drop(["index"], axis = 1, inplace = True)
        
        try:
                
            ayrinti_df3.drop(['Fabrika', 'Fabrika Adresi'], axis=1, inplace=True)
            
            ayrinti_df3.rename(columns={'Üretici Firma (Yabancı)': 'İthalatçı Firma / Üretici Firma'}, inplace=True)
        
        except:
            
            pass

        ayrinti_df = [ayrinti_df, ayrinti_df3]
        
        ayrinti_df = pd.concat(ayrinti_df, ignore_index=True)
        
        browser.back()
        
        for k in range(2, 101):

            button = browser.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/div[3]/div/table/tbody/tr[{0}]/td[8]/a".format(k))
        
            browser.execute_script('arguments[0].click()', button)
            
            ayrinti = pd.read_html(browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[2]/table")).get_attribute('outerHTML'))[0]
            
            ayrinti_df4 = ayrinti.transpose() # , index = ["Formulasyonu", "Aktif Madde", "Ruhsat Numarası", "Ruhsat Tarihi", "Ruhsat Grubu", "Raf Ömrü Süre", "Geçerlilik Süresi", "Ruhsat Sahibi Firma", "Adresi", "İthalatçı Firma / Üretici Firma", "Adresi"]
            
            ayrinti_df4.columns = ayrinti_df4.iloc[0]
            
            ayrinti_df4.drop(labels=0, axis=0, inplace=True, index=None)
            
            try:
            
                ayrinti_df4.drop(['Fabrika', 'Fabrika Adresi'], axis=1, inplace=True)
                
                ayrinti_df4.rename(columns={'Üretici Firma (Yabancı)': 'İthalatçı Firma / Üretici Firma'}, inplace=True)
            
            except:
                
                pass
            
            ayrinti_df4.reset_index(inplace=True)
            
            ayrinti_df4.drop(["index"], axis = 1, inplace = True)
            
            # sleep(1)
            
            browser.back()
            
            ayrinti_df = [ayrinti_df, ayrinti_df4]
    
            ayrinti_df = pd.concat(ayrinti_df, ignore_index=True)
        
        # print("Done 2/{0}".format(totalpage))
        
        for j in tqdm (range(1, totalpage), desc="Done", ascii=False, ncols= 120, initial = 2, unit ="pages"): # dynamic_ncols=True
            
            # if j == 0 or j == 1:
                
            #     pass
            
            # else:
            
            button = browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[1]/div[4]/div/div/ul/li[9]/a"))
        
            browser.execute_script('arguments[0].click()', button)
            
            add_df = pd.read_html(browser.find_element(By.XPATH, ("//*[@id='tablo']")).get_attribute('outerHTML'))[0]
            
            webtable_df2 = [webtable_df2, add_df]
            
            webtable_df2 = pd.concat(webtable_df2, ignore_index=True)
            
            for l in range(1, 101):

                button = browser.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/div[3]/div/table/tbody/tr[{0}]/td[8]/a".format(l))
            
                browser.execute_script('arguments[0].click()', button)
                
                ayrinti = pd.read_html(browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[2]/table")).get_attribute('outerHTML'))[0]
                
                ayrinti_df5 = ayrinti.transpose() # , index = ["Formulasyonu", "Aktif Madde", "Ruhsat Numarası", "Ruhsat Tarihi", "Ruhsat Grubu", "Raf Ömrü Süre", "Geçerlilik Süresi", "Ruhsat Sahibi Firma", "Adresi", "İthalatçı Firma / Üretici Firma", "Adresi"]
                
                ayrinti_df5.columns = ayrinti_df5.iloc[0]
                
                ayrinti_df5.drop(labels=0, axis=0, inplace=True, index=None)
                
                try:
                
                    ayrinti_df5.drop(['Fabrika', 'Fabrika Adresi'], axis=1, inplace=True)
                    
                    ayrinti_df5.rename(columns={'Üretici Firma (Yabancı)': 'İthalatçı Firma / Üretici Firma'}, inplace=True)
                
                except:
                    
                    pass
                
                ayrinti_df5.reset_index(inplace=True)
                
                ayrinti_df5.drop(["index"], axis = 1, inplace = True)
                
                # sleep(1)
                
                browser.back()
                
                ayrinti_df = [ayrinti_df, ayrinti_df5]
        
                ayrinti_df = pd.concat(ayrinti_df, ignore_index=True)
        
        webtable_df3 = pd.read_html(browser.find_element(By.XPATH, ("//*[@id='tablo']")).get_attribute('outerHTML'))[0]
        
        totalbku = browser.find_element(By.XPATH, ("//*[@id='tablo_info']")).get_attribute('outerHTML')
        
        if ara1.search(str(totalbku)):
        
            totalbku = ara1.search(str(totalbku))
            
        if ara2.search(str(totalbku)):
        
            totalbku = ara2.search(str(totalbku))
            
        if ara3.search(str(totalbku)):
        
            totalbku = ara3.search(str(totalbku))
            
        totalbku = int(str(totalbku.group()).replace('.', ''))
        
        lastpageBKU = totalbku%100
        
        for m in range(1, lastpageBKU-1):
            
            if m ==  lastpageBKU-10:
                
                totalbku = browser.find_element(By.XPATH, ("//*[@id='tablo_info']")).get_attribute('outerHTML')
        
                if ara1.search(str(totalbku)):
                
                    totalbku = ara1.search(str(totalbku))
                    
                if ara2.search(str(totalbku)):
                
                    totalbku = ara2.search(str(totalbku))
                    
                if ara3.search(str(totalbku)):
                
                    totalbku = ara3.search(str(totalbku))
                    
                totalbku = int(str(totalbku.group()).replace('.', ''))
                
                if m > totalbku:
                    
                    break

            button = browser.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/div[3]/div/table/tbody/tr[{0}]/td[8]/a".format(m))
        
            browser.execute_script('arguments[0].click()', button)
            
            ayrinti = pd.read_html(browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[2]/table")).get_attribute('outerHTML'))[0]
            
            ayrinti_df6 = ayrinti.transpose() # , index = ["Formulasyonu", "Aktif Madde", "Ruhsat Numarası", "Ruhsat Tarihi", "Ruhsat Grubu", "Raf Ömrü Süre", "Geçerlilik Süresi", "Ruhsat Sahibi Firma", "Adresi", "İthalatçı Firma / Üretici Firma", "Adresi"]
            
            ayrinti_df6.columns = ayrinti_df6.iloc[0]
            
            ayrinti_df6.drop(labels=0, axis=0, inplace=True, index=None)
            
            ayrinti_df6.reset_index(inplace=True)
            
            ayrinti_df6.drop(["index"], axis = 1, inplace = True)
            
            try:
                
                ayrinti_df6.drop(['Fabrika', 'Fabrika Adresi'], axis=1, inplace=True)
                
                ayrinti_df6.rename(columns={'Üretici Firma (Yabancı)': 'İthalatçı Firma / Üretici Firma'}, inplace=True)
            
            except:
                
                pass
            
            ayrinti_df = [ayrinti_df, ayrinti_df6]
        
            ayrinti_df = pd.concat(ayrinti_df, ignore_index=True)
            
            # sleep(1)
            
            browser.back()
        
        webtable_df = [webtable_df1, webtable_df2, webtable_df3]
        
        webtable_df = pd.concat(webtable_df, ignore_index=True)
        
        webtable_df_all = [webtable_df, ayrinti_df]
                
        webtable_df_all = pd.concat(webtable_df_all, axis=1)
        
        webtable_df_all.to_excel("BitkiKorumaUrunListesi.xlsx")
        
        print("Done {0}/{1} as %100 and data file is created.".format(totalpage, totalpage))

        browser.quit()

if __name__ == '__main__':
    
    # try:
        
    getList(driver='chrome', driver_path="chromedriver.exe")
        
    # except:
        
    #     os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
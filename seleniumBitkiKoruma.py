from time import sleep
import pandas as pd
from selenium import webdriver
import selenium
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import math
from tqdm import tqdm
import os
import sys
import warnings
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

warnings.simplefilter(action='ignore')

translationTable = str.maketrans("ğĞıİöÖüÜşŞçÇ", "gGiIoOuUsScC")

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

        browser.maximize_window()
        
        browser.implicitly_wait(10)

        browser.get(self.link)

        sleep(3)
        
        WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='tablo_length']/label/select")))
        
        select = Select(browser.find_element(By.XPATH, ("//*[@id='tablo_length']/label/select")))

        select.select_by_value('100')

        sleep(1)
        
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
        
        webtables_df = pd.read_html(browser.find_element(By.XPATH, ("//*[@id='tablo']")).get_attribute('outerHTML'))[0]
        
        newcolumns = pd.Index(["Bitki Koruma Ürünü", "Ruhsat Durumu", "Aktif Madde", "Ruhsat Sahibi Firma", "Ruhsat Tarihi", "Ruhsat No", "Formulasyon", "Detaylar", "Ruhsat Grubu", "Raf Ömrü Süre", "Geçerlilik Süresi", "Ruhsat Sahibi Firma Adı", "Ruhsat Sahibi Firma Adresi", "İthalatçı Firma / Üretici Firma Adı", "İthalatçı Firma / Üretici Firma Adresi", "Üretici Firma (Yabancı) Adı", "Üretici Firma (Yabancı) Adresi", "Fabrika Adı", "Fabrika Adresi", "Bitki Adı", "Zararlı Organizma", "Tavsiye Durumu", "Dozu", "Son İlaçlama ile Hasat Arası Süre", "Tavsiye Tarihi", "Uyarı", "Yerli mi?", "Konum", "Hastalık Latince İsmi"])
                
        table_df = pd.DataFrame(data=np.empty((totalbku*15, 29), dtype=str),columns=newcolumns)
        
        s = 0
        
        sehirler=["Adana", "Adıyaman", "Afyon", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "İçel (Mersin)", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"]
        
        sehir = sehirler.copy()
        
        for y in range(len(sehir)):
            
            sehir[y] = sehirler[y].lower() # totalpage
        
        for j in tqdm (range(0, totalpage), desc="Done", ascii=False, ncols= 120, initial = 0, unit ="pages"): # 1, initial = 2, dynamic_ncols=True mininterval=5
                        
            webtables_dfadd = pd.read_html(browser.find_element(By.XPATH, ("//*[@id='tablo']")).get_attribute('outerHTML'))[0]
            
            webtables_df = webtables_dfadd.copy()
            
            for i in range(1, 101): # 101
                
                for k in range(len(webtables_df.columns)):
                    
                    table_df.iloc[(i+s-1)+100*j][table_df.columns[k]] = webtables_df.iloc[(i-1)][table_df.columns[k]]

                    bitkiAdi = table_df.iloc[(i+s-1)+100*j][table_df.columns[0]]
                    
                    konum = table_df.iloc[(i+s-1)+100*j][table_df.columns[3]]
                    
                    for z in range(len(sehir)):
                        
                        matchsehirler = re.search(sehir[z].translate(translationTable), konum.lower().translate(translationTable))
                        
                        matchizmir = re.search("izmir", konum.lower().translate(translationTable))
                        
                        matchIZMIR = re.search("IZMIR", konum.upper().translate(translationTable))
                        
                        if matchsehirler:
                            
                            konum = sehirler[z]
                            
                        elif matchizmir or matchIZMIR:
                            
                            konum = "İzmir"
                            
                        else:
                            
                            matchsehirler = re.search(sehir[z].upper().translate(translationTable), konum.upper().translate(translationTable))
                            
                            matchizmir = re.search("İZMİR", konum.upper().translate(translationTable))
                            
                            matchIZMIR = re.search("IZMIR", konum.upper().translate(translationTable))
                            
                            if matchsehirler:
                            
                                konum = sehirler[z]
                                
                            elif matchizmir or matchIZMIR:
                            
                                konum = "İzmir"
                            
                        table_df.iloc[(i+s-1)+100*j]["Konum"] = konum
                
                    matchbitkiAdi = re.search(r"İMAL", bitkiAdi)
                    
                    if matchbitkiAdi:
                        
                        table_df.iloc[(i+s-1)+100*j]["Yerli mi?"] = "Evet"
                        
                    else:
                        table_df.iloc[(i+s-1)+100*j]["Yerli mi?"] = "Hayır"
                    
                errors = ["NoSuchElementException", "ElementNotInteractableException"]
                
                WebDriverWait(browser, timeout = 20000, poll_frequency=.2, ignored_exceptions=errors).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/div/div[2]/div[1]/div[3]/div/table/tbody/tr[{0}]/td[8]/a".format(i))))
                
                button = browser.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/div[3]/div/table/tbody/tr[{0}]/td[8]/a".format(i))
    
                browser.execute_script('arguments[0].click()', button)
                
                errors = ["NoSuchElementException", "ElementNotInteractableException"]
                
                WebDriverWait(browser, timeout = 20000, poll_frequency=.2, ignored_exceptions=errors).until(EC.visibility_of_all_elements_located((By.XPATH, ("/html/body/div/div[2]/div[2]/table"))))
                
                ayrinti = pd.read_html(browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[2]/table")).get_attribute('outerHTML'))[0]
                
                ayrinti_df = ayrinti.transpose()
                
                ayrinti_df.columns = ayrinti_df.iloc[0]
                
                ayrinti_df.drop(labels=0, axis=0, inplace=True)
                
                ayrinti_df.reset_index(inplace=True)
                
                ayrinti_df.columns.values[0] = "Formulasyon"
                
                ayrinti_df.columns.values[2] = "Ruhsat No"
                
                if len(ayrinti_df.columns) == 12:
                    
                    if ayrinti_df.columns.values[10] == "İthalatçı Firma / Üretici Firma":
                
                        ayrinti_df.columns.values[10] = "İthalatçı Firma / Üretici Firma Adı"
                    
                        ayrinti_df.columns.values[11] = "İthalatçı Firma / Üretici Firma Adresi"
                    
                if len(ayrinti_df.columns) == 14:
                    
                    if ayrinti_df.columns.values[10] == "Üretici Firma (Yabancı)":
                
                        ayrinti_df.columns.values[10] = "Üretici Firma (Yabancı) Adı"
                    
                        ayrinti_df.columns.values[11] = "Üretici Firma (Yabancı) Adresi"
                        
                        ayrinti_df.columns.values[12] = "Fabrika Adı"
                
                ayrinti_df.rename(columns={'Ruhsat Sahibi Firma': 'Ruhsat Sahibi Firma Adı'}, inplace=True)
                
                ayrinti_df.columns.values[9] = "Ruhsat Sahibi Firma Adresi"
                
                for l in range(8, len(ayrinti_df.columns)+8):
                
                    try:
                        
                        table_df.iloc[(i+s-1)+100*j][table_df.columns[l]] = ayrinti_df.iloc[0][table_df.columns[l]]
                    
                    except:
                        
                        pass
                                        
                try:
                    
                    WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/div/div[2]/div[3]/div[1]/div[2]/div/label/select")))
                                    
                    select = Select(browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[3]/div[1]/div[2]/div/label/select")))

                    select.select_by_value('100')
                    
                except:
                    
                    sleep(5)
                    
                    WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/div/div[2]/div[3]/div[1]/div[2]/div/label/select")))
                    
                    select = Select(browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[3]/div[1]/div[2]/div/label/select")))

                    select.select_by_value('100')
                
                sleep(1)
                
                totalhastalik = browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[3]/div[1]/div[1]/div")).get_attribute('outerHTML')
                                
                for h in range(len(totalhastalik)):
                    
                    if totalhastalik[h] == ">":
                        
                        totalhastalik = totalhastalik[h+1:]
                        
                        for t in range(len(totalhastalik)):
                        
                            if totalhastalik[t] == "k":
                                
                                totalhastalik = totalhastalik[:t-1]
                                
                                a = int(totalhastalik)
                                
                                break
                            
                            else: 
                                
                                pass
                            
                        break
                            
                    else:
                        
                        pass
                
                c = s
                
                for n in range(a-1):
                    
                    table_df.loc[i+c+100*j] = table_df.loc[i+c-1+100*j].copy()

                    c += 1
                    
                o = int(a/100)
                    
                for m in range(a): # a-1
                    
                    if o == 2:
                        
                        WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/div/div[2]/div[3]/div[4]/div/div/ul/li[{0}]/a".format(o+3))))
                        
                        button = browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[3]/div[4]/div/div/ul/li[{0}]/a".format(o+3)))
                        
                        browser.execute_script('arguments[0].click()', button)
                        
                    if o == 1:
                        
                        WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/div/div[2]/div[3]/div[4]/div/div/ul/li[{0}]/a".format(o+3))))
                        
                        button = browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[3]/div[4]/div/div/ul/li[{0}]/a".format(o+3)))
                        
                        browser.execute_script('arguments[0].click()', button)
                        
                    try:
                        
                        WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/div/div[2]/div[3]/div[3]/div/table/tbody/tr[{0}]/td[7]/a".format(m%100+1))))
                
                        button = browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[3]/div[3]/div/table/tbody/tr[{0}]/td[7]/a".format(m%100+1)))
                    
                        browser.execute_script('arguments[0].click()', button)
                        
                        uyaribilgisi = browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[1]/dl/dd[9]/label"))
                        
                        table_df.iloc[(i+s-1)+100*j][table_df.columns[25]] = uyaribilgisi.text
                        
                        browser.back()
                        
                    except:
                        
                        pass
                        
                    for v in range(a):
                        
                        try:
                        
                            hastalikbilgisi = pd.read_html(browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[3]/div[3]/div/table")).get_attribute('outerHTML'))[0]
                            
                            hastalikbilgisi = hastalikbilgisi.iloc[v]
                        
                            for b in range(19, len(hastalikbilgisi)+19):
                            
                                if b == 20:
                                    
                                    table_df.iloc[(i+s-1)+100*j][table_df.columns[b]] = hastalikbilgisi[table_df.columns[b]]
                                    
                                    hastalikadi = hastalikbilgisi["Zararlı Organizma"]
                                    
                                    hastalikadi = str(hastalikadi)
                                    
                                    if hastalikadi == "" or hastalikadi == "nan" or hastalikadi == None:
                                        
                                        table_df.iloc[(i+s-1)+100*j]["Hastalık Latince İsmi"] = ""
                                    
                                    else:
                                        
                                        for h in range(len(hastalikadi)):
                                    
                                            if hastalikadi[h] == "(":
                                                
                                                latinceBitkiAdı = hastalikadi[h+1:len(hastalikadi)-1]
                                                
                                                if hastalikadi[-1] == ")":
                                                
                                                    latinceBitkiAdı = latinceBitkiAdı[:-1]
                                                
                                                table_df.iloc[(i+s-1)+100*j]["Hastalık Latince İsmi"] = latinceBitkiAdı
                                
                                elif b == 25:
                                    
                                    pass
                                
                                else:
                                    
                                    table_df.iloc[(i+s-1)+100*j][table_df.columns[b]] = hastalikbilgisi[table_df.columns[b]]
                        
                        except:
                            
                            pass
                        
                    if m < a-1:
                        
                        s += 1
                
                browser.back()
                
            WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/div/div[2]/div[1]/div[4]/div/div/ul/li[9]/a")))
                
            button = browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[1]/div[4]/div/div/ul/li[9]/a"))
                
            browser.execute_script('arguments[0].click()', button)
            
            table_df.to_excel("BitkiKorumaUrunListesi.xlsx")
            
        j = j + 1
        
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
        
        webtables_df = pd.read_html(browser.find_element(By.XPATH, ("//*[@id='tablo']")).get_attribute('outerHTML'))[0]
        
        for p in range(1, totalbku+1): # totalbku
                
            for d in range(len(webtables_df.columns)):
                    
                table_df.iloc[(i+s+p-1)+100*j][table_df.columns[d]] = webtables_df.iloc[(p-1)][table_df.columns[d]]

                bitkiAdi = table_df.iloc[(i+s+p-1)+100*j][table_df.columns[0]]
                
                konum = table_df.iloc[(i+s+p-1)+100*j][table_df.columns[3]]
                    
                for z in range(len(sehir)):
                        
                    matchsehirler = re.search(sehir[z].translate(translationTable), konum.lower().translate(translationTable))
                    
                    matchizmir = re.search("izmir", konum.lower().translate(translationTable))
                    
                    matchIZMIR = re.search("IZMIR", konum.upper().translate(translationTable))
                    
                    if matchsehirler:
                        
                        konum = sehirler[z]
                        
                    elif matchizmir or matchIZMIR:
                        
                        konum = "İzmir"
                        
                    else:
                        
                        matchsehirler = re.search(sehir[z].upper().translate(translationTable), konum.upper().translate(translationTable))
                        
                        matchizmir = re.search("İZMİR", konum.upper().translate(translationTable))
                        
                        matchIZMIR = re.search("IZMIR", konum.upper().translate(translationTable))
                        
                        if matchsehirler:
                        
                            konum = sehirler[z]
                            
                        elif matchizmir or matchIZMIR:
                        
                            konum = "İzmir"
                        
                    table_df.iloc[(i+s+p-1)+100*j]["Konum"] = konum
                        
                matchbitkiAdi = re.search(r"İMAL", bitkiAdi)
                    
                if matchbitkiAdi:
                    
                    table_df.iloc[(i+s+p-1)+100*j]["Yerli mi?"] = "Evet"
                    
                else:
                    
                    table_df.iloc[(i+s+p-1)+100*j]["Yerli mi?"] = "Hayır"
                    
            errors = ["NoSuchElementException", "ElementNotInteractableException"]
                
            WebDriverWait(browser, timeout = 20000, poll_frequency=.2, ignored_exceptions=errors).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/div/div[2]/div[1]/div[3]/div/table/tbody/tr[{0}]/td[8]/a".format(i))))
            
            button = browser.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/div[3]/div/table/tbody/tr[{0}]/td[8]/a".format(i))
            
            browser.execute_script('arguments[0].click()', button)

            errors = ["NoSuchElementException", "ElementNotInteractableException"]
                
            WebDriverWait(browser, timeout = 20000, poll_frequency=.2, ignored_exceptions=errors).until(EC.visibility_of_all_elements_located((By.XPATH, ("/html/body/div/div[2]/div[2]/table"))))
                
            ayrinti = pd.read_html(browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[2]/table")).get_attribute('outerHTML'))[0]

            ayrinti_df = ayrinti.transpose()
            
            ayrinti_df.columns = ayrinti_df.iloc[0]
            
            ayrinti_df.drop(labels=0, axis=0, inplace=True)
            
            ayrinti_df.reset_index(inplace=True)
            
            ayrinti_df.columns.values[0] = "Formulasyon"
            
            ayrinti_df.columns.values[2] = "Ruhsat No"
            
            if len(ayrinti_df.columns) == 12:
                
                if ayrinti_df.columns.values[10] == "İthalatçı Firma / Üretici Firma":
            
                    ayrinti_df.columns.values[10] = "İthalatçı Firma / Üretici Firma Adı"
                
                    ayrinti_df.columns.values[11] = "İthalatçı Firma / Üretici Firma Adresi"
                
            if len(ayrinti_df.columns) == 14:
                
                if ayrinti_df.columns.values[10] == "Üretici Firma (Yabancı)":
            
                    ayrinti_df.columns.values[10] = "Üretici Firma (Yabancı) Adı"
                
                    ayrinti_df.columns.values[11] = "Üretici Firma (Yabancı) Adresi"
                    
                    ayrinti_df.columns.values[12] = "Fabrika Adı"
            
            ayrinti_df.rename(columns={'Ruhsat Sahibi Firma': 'Ruhsat Sahibi Firma Adı'}, inplace=True)
            
            ayrinti_df.columns.values[9] = "Ruhsat Sahibi Firma Adresi"
            
            for l in range(8, len(ayrinti_df.columns)+8):
            
                try:
                    
                    table_df.iloc[(i+s+p-1)+100*j][table_df.columns[l]] = ayrinti_df.iloc[0][table_df.columns[l]]
                
                except:
                    
                    pass
                
            try:
                
                WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/div/div[2]/div[3]/div[1]/div[2]/div/label/select")))
                                    
                select = Select(browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[3]/div[1]/div[2]/div/label/select")))

                select.select_by_value('100')
                
            except:
                
                sleep(5)
                
                WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/div/div[2]/div[3]/div[1]/div[2]/div/label/select")))
                
                select = Select(browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[3]/div[1]/div[2]/div/label/select")))

                select.select_by_value('100')
            
            sleep(1)
                
            totalhastalik = browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[3]/div[1]/div[1]/div")).get_attribute('outerHTML')
            
            for h in range(len(totalhastalik)):
                
                if totalhastalik[h] == ">":
                    
                    totalhastalik = totalhastalik[h+1:]
                    
                    for t in range(len(totalhastalik)):
                    
                        if totalhastalik[t] == "k":
                            
                            totalhastalik = totalhastalik[:t-1]
                            
                            a = int(totalhastalik)
                            
                            break
                        
                        else: 
                            
                            pass
                        
                    break
                        
                else:
                    
                    pass
            
            c = s
            
            for n in range(a-1):
                
                table_df.loc[i+c+p+100*j] = table_df.loc[i+c+p-1+100*j].copy()

                c += 1
                
            o = int(a/100)
                
            for m in range(a):
                
                if o == 2:
                    
                    WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/div/div[2]/div[3]/div[4]/div/div/ul/li[{0}]/a".format(o+3))))
                        
                    button = browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[3]/div[4]/div/div/ul/li[{0}]/a".format(o+3)))
                    
                    browser.execute_script('arguments[0].click()', button)
                    
                if o == 1:
                    
                    WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/div/div[2]/div[3]/div[4]/div/div/ul/li[{0}]/a".format(o+3))))
                    
                    button = browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[3]/div[4]/div/div/ul/li[{0}]/a".format(o+3)))
                    
                    browser.execute_script('arguments[0].click()', button)
                
                try:
                    
                    WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/div/div[2]/div[3]/div[3]/div/table/tbody/tr[{0}]/td[7]/a".format(m%100+1))))
                
                    button = browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[3]/div[3]/div/table/tbody/tr[{0}]/td[7]/a".format(m%100+1)))
                
                    browser.execute_script('arguments[0].click()', button)
                    
                    uyaribilgisi = browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[1]/dl/dd[9]/label"))
                    
                    table_df.iloc[(i+s+p-1)+100*j][table_df.columns[25]] = uyaribilgisi.text
                    
                    browser.back()
                    
                except:
                    
                    pass
                        
                for v in range(a):
                    
                    try:
                    
                        hastalikbilgisi = pd.read_html(browser.find_element(By.XPATH, ("/html/body/div/div[2]/div[3]/div[3]/div/table")).get_attribute('outerHTML'))[0]
                        
                        hastalikbilgisi = hastalikbilgisi.iloc[v]
                    
                        for b in range(19, len(hastalikbilgisi)+19):
                        
                            if b == 20:
                                
                                table_df.iloc[(i+s+p-1)+100*j][table_df.columns[b]] = hastalikbilgisi[table_df.columns[b]]
                                
                                hastalikadi = hastalikbilgisi["Zararlı Organizma"]
                                
                                hastalikadi = str(hastalikadi)
                                
                                if hastalikadi == "" or hastalikadi == "nan" or hastalikadi == None:
                                    
                                    table_df.iloc[(i+s+p-1)+100*j]["Hastalık Latince İsmi"] = ""
                                
                                else:
                                    
                                    for h in range(len(hastalikadi)):
                                
                                        if hastalikadi[h] == "(":
                                            
                                            latinceBitkiAdı = hastalikadi[h+1:len(hastalikadi)-1]
                                            
                                            if hastalikadi[-1] == ")":
                                                
                                                latinceBitkiAdı = latinceBitkiAdı[:-1]
                                            
                                            table_df.iloc[(i+s+p-1)+100*j]["Hastalık Latince İsmi"] = latinceBitkiAdı
                            
                            elif b == 25:
                                    
                                pass
                            
                            else:
                                
                                table_df.iloc[(i+s+p-1)+100*j][table_df.columns[b]] = hastalikbilgisi[table_df.columns[b]]
                    
                    except:
                        
                        pass
                    
                if m < a-1:
                    
                    s += 1
    
            browser.back()
            
        browser.quit()
            
        table_df.to_excel("BitkiKorumaUrunListesi.xlsx") 

        print("Done {0}/{1} as %100 and data file is created.".format(totalpage, totalpage))

if __name__ == '__main__':
        
    getList(driver='chrome', driver_path="chromedriver.exe")
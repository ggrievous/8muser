import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from threading import Thread
import urllib.request
import requests 
import shutil


options = Options()
options.headless = True
chrome_driver_path = r"C:\Users\NH\PycharmProjects\SeleniumTest\drivers\chromedriver.exe"
base_url = "https://www.8muses.com"


def fetch_image_url(url,filename,download_location):
    driver = webdriver.Chrome(chrome_driver_path, chrome_options=options)
    driver.get(url)
    page = driver.page_source
    soup = BeautifulSoup(page,"lxml")
    image_url = "http:"+soup.find("img",{"class":"image"})['src']
    driver.close()
    download_image(image_url,filename,download_location)

    
def download_image(image_url,filename,download_location):
    r = requests.get(image_url,stream=True, headers={'User-agent': 'Mozilla/5.0'})
    if r.status_code == 200:
        with open(os.path.join(download_location,str(filename)+".png"), 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    print("Downloaded page {pagenumber}".format(pagenumber=filename))


if __name__=="__main__":
    print("Album Url : ")
    album_url = input()
    print("Download Location : ")
    download_location = input()
    driver = webdriver.Chrome(chrome_driver_path, chrome_options=options)
    print("Loading Comic...")
    driver.get(album_url)
    album_html = driver.page_source
    print("Comic successfully loaded")
    soup = BeautifulSoup(album_html,"lxml")
    comic_name = soup.find("title").text.split("|")[0]
    download_location = os.path.join(download_location,comic_name)
    os.mkdir(download_location)
    print("Finding comic's pages")
    images = soup.find_all("a",{"class":"c-tile t-hover"})
    page_urls = []
    threads = []
    for image in images:
        page_urls.append(base_url + image['href'])
    print("Found {} pages".format(len(page_urls)))
    '''for i in range(len(page_urls)):
        thread = Thread(target=fetch_image_url,args=(page_urls[i],i,download_location,))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()'''
    for i in range(len(page_urls)):
        fetch_image_url(page_urls[i],i,download_location)
    driver.quit()

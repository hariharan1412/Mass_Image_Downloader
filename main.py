from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


import time
import os
import shutil

# PASTE YOUR CHROMEDRIVER PATH
PATH = ""

class image_downloader:

    def __init__(self) -> None:
        
        #YOUR QUERY STRING
        self.query = input(" Enter the Type of Image : ")
        
        #TOTAL NUMBER OF IMAGES WANT TO DOWNLOAD 
        self.max_count = int(input(" No.of.Images to download : "))


        options = Options()
        options.add_argument("--headless")

        #URL TO DOWNLOAD IMAGE 
        img_url = "https://yandex.com/images/search?text=" + self.query
        self.web = webdriver.Chrome(executable_path=PATH , options=options)

        self.web.implicitly_wait(30)
        self.web.get(img_url)

        time.sleep(2)
    
        self.web.find_element(By.XPATH , "//div[@data-type='o']").click()

        #LIST TO STORE LINKS
        self.link_list = set()

        #CREATE A NEW DIRECTORY
        self.new_dir_path = self.make_new_dir(self.query)

    def make_new_dir(self, query): #CREATES NEW DIRECTORY

        cwd = os.getcwd()
        print(cwd) 
        new_dir_path = os.path.join(cwd,query)
        if os.path.exists(new_dir_path):
            shutil.rmtree(new_dir_path)
        os.mkdir(new_dir_path)

        print("Directory '% s' created" % query)
        return new_dir_path

    def get_links(self): #GET LINKS OF THE IMAGES
        
        for i in range(1 , self.max_count+1):

            n = 0

            while True and n < 300:
            
                link = self.web.find_element(By.XPATH , "//img[@class='MMImage-Origin']")
                text = link.get_attribute('src')

                if text[-4:] == ".jpg":
                    break

                else:
                    time.sleep(0.1)
                    n += 1

            self.link_list.add(text)
            link.click()
            
            print("S.no : " , i)


    def download_img(self): #DOWNLOAD IMAGES FROM THE LINK OBTAINED FROM THE PREVIOUS FUNCTION i.e get_links()
    
        i = 0

        for url in self.link_list:
        
            i += 1
            print("url : ", url , "i : ",i)

            def down_img( url):
            
                self.web.get(url)
                full_img = self.web.find_element(By.TAG_NAME , 'img')
                full_img.screenshot(f"downloads/{i}.png")

                full_img.screenshot(f"{self.new_dir_path}/{self.query}-{i}.png")

                print(f"{self.query}-{i}.png downloaded")

            down_img(url)


if __name__ == "__main__":

    img = image_downloader()
    img.get_links()
    img.download_img()

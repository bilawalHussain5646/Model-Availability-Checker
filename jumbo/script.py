import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import json
import multiprocessing
import tkinter as tk
import tkinter.font as tkFont
import threading
import os
import concurrent.futures

# Search by keyword 
# Count brands products and then return the dataframe 

# driver = webdriver.Chrome()

def FetchBrandsInfo(driver,link,keyword,brands_list):
    driver.get(link)
    # driver.implicitly_wait(10)
    # time.sleep(10)
    brands = {}
    for brand in brands_list:
        brands[brand.lower()] = 0
        # brands[brand]=0


    
    # brands  --> List of brands     
    # driver.get(link)
    ids=  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".col-lg-9.border-box.products-list.products-list-en")))
    # ids = ids.find_elements(By.CSS_SELECTOR,".list-view")
    
    
    all_divs  = ids.find_elements(By.CSS_SELECTOR, ".flex.gap-0.flex-col.w-full")
    counter = 0
    for div in all_divs:
    # get all elements with the tag "a"
        
        title = div.find_element(By.TAG_NAME,"h2")
        # title.text
        title_value = title.text.lower()
        for key in brands.keys():
            key = key.lower()
            # print(title.text.find(key))
            if (title_value.find(key) != -1):
                brands[key]+=1 
                break
        
        counter+=1
        if counter >=20:
            break
        
    
    
    print(brands)

    missing_brand = []
    sum_of_counts = 0
    for key,value in brands.items():    
        sum_of_counts = sum_of_counts+value
    
    print(sum_of_counts)
   

    if sum_of_counts <=19:
        counter= 0
        for div in all_divs:
        # get all elements with the tag "a"
            
            title = div.find_element(By.TAG_NAME,"h2")
            # title.text
            productfound = False
            title_value = title.text.lower()
            for key in brands.keys():
                key = key.lower()
                # print(title.text.find(key))
                if (title_value.find(key) != -1):
                    productfound = True
                    break

            if productfound == False:
                missing_brand.append(title_value)
                print(title_value)
            counter+=1
            if counter >=20:
                break

    return brands,missing_brand
   

      

# # Fetch the links in list 
# df = pd.read_excel("links.xlsx")["Links"].values
# list_of_urls = df
# # print(list_of_urls)



# Go to each link
# 
# -----------------------------

def Run():
    df_sharaf_dg_categories_keywords = pd.read_excel("search_keywords.xlsx")
    df_sharaf_dg_brands = pd.read_excel("input.xlsx")
    list_of_categories = df_sharaf_dg_categories_keywords.Category.unique()


    # Fetch categores and keywords 
    # Fetch the brands in list 

    categories_data = []


    categories_data = [{
                "name": category,
                "keywords": df_sharaf_dg_categories_keywords.query("Category =='"+category+"'")["Keywords"].values,
                "brands": df_sharaf_dg_brands.query("Category == '"+category+"'")["Brands"].values
            } for category in list_of_categories] 

    print(categories_data)
    driver = webdriver.Chrome()
    final_data = {}

    # for i in range(0, 1):
    for i in range(0, len(categories_data)):
        df=  pd.DataFrame(columns=['Category','Keywords','Brands','Counts'])
        data = []
        for keyword in categories_data[i]["keywords"]:
            link = f"https://www.jumbo.ae/search/{keyword}"
            brands,missing_brand = FetchBrandsInfo(driver,link,keyword,categories_data[i]["brands"])
            counting_brands = len(brands)
            list_of_brands_keys = list(brands.keys())
            print("------------", list_of_brands_keys)


            list_of_brands_values =list(brands.values())


            for z in range(0,counting_brands):
                df = df.append({
                    "Category":categories_data[i]["name"],
                    "Keywords": keyword,
                    "Brands": list_of_brands_keys[z],
                    "Counts": list_of_brands_values[z],

                },ignore_index=True)

            if missing_brand != []:
                for mb in missing_brand:
                    df = df.append({
                        "Category":categories_data[i]["name"],
                        "Keywords": keyword,
                        "Brands": mb,
                        "Counts": 1,
                    },ignore_index=True)

            data.append({
                "keyword": keyword,
                "counts": brands
            })
            # We have to see the brands and take the data of each brand 
        with pd.ExcelWriter("output.xlsx",mode="a",if_sheet_exists='replace') as writer:
            df.to_excel(writer,sheet_name=categories_data[i]["name"])
        
        final_data[categories_data[i]["name"]] = data
    # categories_data

    # print(final_data)
    #  ---------------------------------
    # Category  |  Keyword  |  Brands   | Counts 
    # 
    print(df)


# print("Total Rows:",df["rows"][0])



        # df=  df.groupby('Category')
        # worksheet = writer.sheets['Data']
        

























# def extract_data_by_category(driver, url,cat_name,check_once):

#     # url = "https://uae.sharafdg.com/?q=Air%20Purifier&post_type=product"
#     driver.get(url)
#     try:
#         ids = driver.find_element(By.ID,"hits")
    
#         all_divs  = ids.find_elements(By.CSS_SELECTOR, ".slide")

#         all_data = []
#         count =1
#         for div in all_divs:
#         # get all elements with the tag "a"
            
#             title = div.find_element(By.TAG_NAME,"h4")
#             link = div.find_element(By.TAG_NAME,"a")
#             img = div.find_element(By.TAG_NAME,"img")
#             price = div.find_element(By.CSS_SELECTOR,".price")
#             if title.text.find('Samsung') != -1 or title.text.find("LG") != -1 or title.text.find("Dyson") != -1:
#                 title_name = title.text
#                 price_ = price.text,
#                 image_url = img.get_attribute("src")
#                 img_link = link.get_attribute("href")
#                 full_title_arr = title.text.split()
#                 brand_name = full_title_arr[0]
                
                
#                 mpn,sku,total_images,rating,review = fetch_pdp(driver,link.get_attribute("href"),check_once)
#                 check_once+=1
                
#                 data = {
#                     "Date": datetime.today(),
#                     "Region": "MEA",
#                     "Country": "UAE",
#                     "Retailer": "Sharafdg",
#                     "category":  cat_name,
#                     "brand": brand_name,
#                     "Rank": count,
#                     "mpn": mpn,
#                     "sku": sku,
#                     "title":title_name,
#                     "link": img_link,
#                     "price":price_,
#                     "image url":image_url,
#                 }
        
#                 all_data.append(data)
#             count+=1
            
#         # print(all_data)

#         # close the web driver


#         df = pd.DataFrame(all_data)
#         # print(df)
#         return df
#     except:
#         return False


# driver = webdriver.Chrome()
# # Reading the excel sheet
# df = pd.read_excel("categories/search_by_category.xlsx")

# # Created the empty list to store the list of urls 
# list_of_urls = []
# list_of_categories= []

# for dt in df['category_names']:
#     list_of_categories.append(dt)

# # Looping through each url to fetch the data 
# for dt in df['urls']:
#     list_of_urls.append(dt)
# # print(df)

# # Created an empty dataframe
# dataframe_final = pd.DataFrame()

# # Looping through each url in the list and extracting the data 
# i=0 
# check_once = 0
# while i < len(list_of_urls):

#     # storing the extracted data in df to be used in future
#     rtnData=extract_data_by_category(driver,list_of_urls[i],list_of_categories[i],check_once)
#     if type(rtnData) == bool:
#         pass
#     else:
#     # appending the extracted data in the empty dataframe 
#         dataframe_final = pd.concat([dataframe_final,rtnData])
#         # dataframe_final.append(df)
        
#         # printing dataframe final to show that the data is storing perfectly 
#         print(dataframe_final) 

#         # Printing completed to show that the urls are fetching the data 
#         print("completed")
#         i+=1
#     check_once+=1

# # Closing the browser 
# driver.quit()

# # Printing the dataframe with all the data 
# print(dataframe_final)

# # Storing the dataframe in the text.xlsx file 
# dataframe_final.to_excel(excel_writer = "output/search_by_category_without_sharafdgonly.xlsx")





class App:

    def __init__(self, root):
        #setting title
        root.title("Jumbo Crawler")
        ft = tkFont.Font(family='Arial Narrow',size=13)
        #setting window size
        width=640
        height=480
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        root.configure(bg='black')

        ClickBtnLabel=tk.Label(root)
       
      
        
        ClickBtnLabel["font"] = ft
        
        ClickBtnLabel["justify"] = "center"
        ClickBtnLabel["text"] = "Jumbo Crawler"
        ClickBtnLabel["bg"] = "black"
        ClickBtnLabel["fg"] = "white"
        ClickBtnLabel.place(x=120,y=190,width=150,height=70)
    

        
        Lulu=tk.Button(root)
        Lulu["anchor"] = "center"
        Lulu["bg"] = "#009841"
        Lulu["borderwidth"] = "0px"
        
        Lulu["font"] = ft
        Lulu["fg"] = "#ffffff"
        Lulu["justify"] = "center"
        Lulu["text"] = "START"
        Lulu["relief"] = "raised"
        Lulu.place(x=375,y=190,width=150,height=70)
        Lulu["command"] = self.start_func




  

    def ClickRun(self):

        running_actions = [Run]

        thread_list = [threading.Thread(target=func) for func in running_actions]

        # start all the threads
        for thread in thread_list:
            thread.start()

        # wait for all the threads to complete
        for thread in thread_list:
            thread.join()
    
    def start_func(self):
        thread = threading.Thread(target=self.ClickRun)
        thread.start()

    
        

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
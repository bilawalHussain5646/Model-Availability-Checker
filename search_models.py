import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
import tkinter.font as tkFont
import threading
from selenium.webdriver.chrome.options import Options

def fetch_pdp_Sharaf_DG(driver, url,check_once):
            model_id = ""

            
            try:
                if check_once == 0:
                    driver.execute_script("window.open('');")
                    check_once+=1
                driver.switch_to.window(driver.window_handles[1])
                driver.get(url)
                time.sleep(10)
                # driver.set_page_load_timeout(30)
                
                try:
                    ids = driver.find_element(By.XPATH,"//meta[@itemprop='mpn']")
                    model_id = ids.get_attribute("content")
                except:
                    # driver.close()
                    # driver.switch_to.window(driver.window_handles[0])
                    model_id = ""
                

        


                
                

                # driver.close()
                driver.switch_to.window(driver.window_handles[0])
                return model_id,check_once
            except:
                return model_id,check_once
    
def fetch_pdp_LULU(driver, url,check_once):
            model_id = ""

            
            try:
                if check_once == 0:
                    driver.execute_script("window.open('');")
                    check_once+=1
                driver.switch_to.window(driver.window_handles[1])
                driver.get(url)
                time.sleep(10)
                # driver.set_page_load_timeout(30)
                
                try:
                    ids = driver.find_element(By.XPATH,"//*[contains(text(), 'Model')]")
                    parent = ids.find_element(By.XPATH, '..')
                    children = parent.find_elements(By.XPATH, '*')
                    skip_first = False
                    for child in children:
                        if skip_first == False:
                             skip_first = True
                        else:
                            model_id=child.text
                            break
                    skip_first = False
                    # print(model_id)
                except:
                    # driver.close()
                    # driver.switch_to.window(driver.window_handles[0])
                    model_id = ""
                

        


                
                

                # driver.close()
                driver.switch_to.window(driver.window_handles[0])
                return model_id,check_once
            except:
                return model_id,check_once


def fetch_pdp_Emax(driver, url,check_once):
            model_id = ""

            
            try:
                if check_once == 0:
                    driver.execute_script("window.open('');")
                    check_once+=1
                driver.switch_to.window(driver.window_handles[1])
                driver.get(url)
                time.sleep(10)
                # driver.set_page_load_timeout(30)
                
                try:
                    meta_data = driver.find_element(By.XPATH,"//meta[@property='product:mpn']")
                    model_id = meta_data.get_attribute("content")
                except:
                    # driver.close()
                    # driver.switch_to.window(driver.window_handles[0])
                    model_id = ""
                

        


                
                

                # driver.close()
                driver.switch_to.window(driver.window_handles[0])
                return model_id,check_once
            except:
                driver.switch_to.window(driver.window_handles[0])
                return model_id,check_once
 
def Emax_Web(driver,list_of_categories,data,Sharaf_DG):
        output_df = pd.DataFrame(columns=['Search Name','Model','Emax','Top20','Link'])
        
        model_number = 0
        for cate in list_of_categories:
            df = data[data['Category'] == cate]
            # print(df)
            list_of_models = df["Model"]
            list_of_original_models = df["Actual Model"]
            
            # We got the models of one category
            check_once = 0
            for models in list_of_models:
                    print(list_of_original_models[model_number])
                    print("Model: ",models)
                    df_link = Sharaf_DG[Sharaf_DG['Category'] == cate]
                    keyword = models
                    # print(df_link["Links"])
                    dyno_link = df_link["Links"].iloc[0]
                    # print(dyno_link)
                    each_page = 0
                    
                    model_ids :list = []
                    driver.get(dyno_link)
                    time.sleep(5)
                    # try:
                    # all_pages_ul = driver.find_element(By.CSS_SELECTOR,".css-tuzc44")
                    # Pagination id = "hits-pagination"
                    list_of_li = driver.find_elements(By.CSS_SELECTOR,".product-desc")
                    # print(int(list_of_li[-2].text))
                    output_check = {}
                    counter = 0
                    for one_li in list_of_li:
                        product_link_temp = one_li.find_element(By.TAG_NAME, "a")
                        product_link_temp = product_link_temp.get_attribute("href")

                        # Open this link and then take mpn 
                        mpn,check_once = fetch_pdp_Emax(driver,product_link_temp,check_once)

                        if models.lower() in  mpn.lower():
                            product_link = one_li.find_element(By.TAG_NAME, "a")
                            product_link = product_link.get_attribute("href")
                            output_check= {
                                    "Search Name":models,
                                    "Model": list_of_original_models[model_number],
                                    "Emax": "o",
                                    "Link": product_link
                            }
                            
                            print(models,"Found")
                            break
                        counter+=1
                    
                    if counter == len(list_of_li):
                        output_check= {
                                "Search Name":models,
                                "Model": list_of_original_models[model_number],
                                "Emax": "x",
                                "Top20":"x",
                                "Link": ""
                        }
                        print(models,"Not Found")
                    else:

                        # Top 20 here 
                        
                        driver.get(f"https://uae.emaxme.com/search?q={cate}")
                        time.sleep(5)
                        # try:
                        # all_pages_ul = driver.find_element(By.CSS_SELECTOR,".css-tuzc44")
                        # Pagination id = "hits-pagination"
                        list_of_li = driver.find_elements(By.CSS_SELECTOR,".product-desc")
                        # print(int(list_of_li[-2].text))
                        
                        counter = 0
                        for one_li in list_of_li:
                            product_link_temp = one_li.find_element(By.TAG_NAME, "a")
                            product_link_temp = product_link_temp.get_attribute("href")
                            mpn,check_once = fetch_pdp_Emax(driver,product_link_temp,check_once)

                            if models.lower() in  mpn.lower():
                                output_check["Top20"] = "o"
                                break
                            counter +=1

                            if counter == 20:
                                output_check["Top20"] = "x"
                                break
                        # Till here top 20
                    
                    
                    output_df = output_df.append(output_check,ignore_index=True)
                    model_number+=1
                        
                
                        
                    


        with pd.ExcelWriter("emax.xlsx",mode="a",if_sheet_exists='replace') as writer:
            output_df.to_excel(writer,sheet_name="Emax")


def Carrefour_Web(driver,list_of_categories,data,Sharaf_DG):
        output_df = pd.DataFrame(columns=['Search Name','Model','Carrefour','Top20','Link'])
        
        model_number = 0
        for cate in list_of_categories:
            df = data[data['Category'] == cate]
            # print(df)
            list_of_models = df["Model"]
            list_of_original_models = df["Actual Model"]
            
            # We got the models of one category
            check_once = 0
            for models in list_of_models:
                    print(list_of_original_models[model_number])
                    print("Model: ",models)
                    df_link = Sharaf_DG[Sharaf_DG['Category'] == cate]
                    keyword = models
                    # print(df_link["Links"])
                    dyno_link = df_link["Links"].iloc[0]
                    # print(dyno_link)
                    each_page = 0
                    
                    model_ids :list = []
                    driver.get(dyno_link)
                    time.sleep(5)
                    # try:
                    # all_pages_ul = driver.find_element(By.CSS_SELECTOR,".css-tuzc44")
                    # Pagination id = "hits-pagination"
                    list_of_li = driver.find_elements(By.CSS_SELECTOR,".css-tuzc44")
                    # print(int(list_of_li[-2].text))
                    output_check = {}
                    counter = 0
                    for one_li in list_of_li:
                        if models.lower() in  one_li.text.lower():
                            product_link = one_li.find_element(By.TAG_NAME, "a")
                            product_link = product_link.get_attribute("href")
                            output_check= {
                                    "Search Name":models,
                                    "Model": list_of_original_models[model_number],
                                    "Carrefour": "o",
                                    "Link": product_link
                            }
                            
                            print(models,"Found")
                            break
                        counter+=1
                    
                    if counter == len(list_of_li):
                        output_check= {
                                "Search Name":models,
                                "Model": list_of_original_models[model_number],
                                "Carrefour": "x",
                                "Link": ""
                        }
                        print(models,"Not Found")


                    # Top 20 here 
                    
                    driver.get(f"https://www.carrefouruae.com/mafuae/en/v4/search?keyword={cate}")
                    time.sleep(5)
                    # try:
                    # all_pages_ul = driver.find_element(By.CSS_SELECTOR,".css-tuzc44")
                    # Pagination id = "hits-pagination"
                    list_of_li = driver.find_elements(By.CSS_SELECTOR,".css-tuzc44")
                    # print(int(list_of_li[-2].text))
                    
                    counter = 0
                    for one_li in list_of_li:
                        
                        if models.lower() in  one_li.text.lower():
                            output_check["Top20"] = "o"
                            break
                        counter +=1

                        if counter == 20:
                             output_check["Top20"] = "x"
                             break
                    # Till here top 20
                    
                    
                    output_df = output_df.append(output_check,ignore_index=True)
                    model_number+=1
                        
                
                        
                    


        with pd.ExcelWriter("carrefour.xlsx",mode="a",if_sheet_exists='replace') as writer:
            output_df.to_excel(writer,sheet_name="Carrefour")


def Sharaf_DG_Web(driver,list_of_categories,data,Sharaf_DG):
        output_df = pd.DataFrame(columns=['Model','Sharaf_DG',"Top20","links"])
        # This is the output dataframe object with following columns i.e. Model, Sharaf Dg, Top20, Links

        # List of categories 
        for cate in list_of_categories:

            df = data[data['Category'] == cate]
            # print(df)
            list_of_models = df["Model"]
            # We got the models of one category
            check_once = 0

            for models in list_of_models:
                if check_once == 0:
                    print("Model: ",models)
                    df_link = Sharaf_DG[Sharaf_DG['Category'] == cate]
                    keyword = models
                    # print(df_link["Links"])
                    dyno_link = df_link["Links"].iloc[0]
                    # print(dyno_link)
                    each_page = 0
                    model_ids :list = []
                    driver.get(dyno_link)
                    time.sleep(5)
                    try:
                        all_pages_ul = driver.find_element(By.ID,"hits-pagination")
                        # Pagination id = "hits-pagination"
                        list_of_li = all_pages_ul.find_elements(By.TAG_NAME,"li")
                        # print(int(list_of_li[-2].text))
                        total_pages = int(list_of_li[len(list_of_li)-2].text)
                        print(total_pages)
                        time.sleep(15)
                        
                    except:
                        
                        total_pages = 1
                    
                    while each_page < total_pages:
                        Pages = f"&page_number={each_page+1}"
                        driver.get(dyno_link+Pages)
                        time.sleep(5)
                        ids = driver.find_element(By.ID,"hits")
                
                        all_divs  = ids.find_elements(By.CSS_SELECTOR, ".slide")
                        
                        for div in all_divs:
                            try:
                                link = div.find_element(By.TAG_NAME,"a").get_attribute("href")
                                model_id,check_once = fetch_pdp_Sharaf_DG(driver,link,check_once)
                                print(model_id)
                                # Save this model id in the list and use it later 
                                # 
                                model_ids.append(model_id)
                            except:
                                 pass

                    
                        each_page += 1
                
                # Compare here now
                total_models = len(model_ids)
                counter = 0
                for each_model in model_ids: 
                    if each_model.find(models) != -1:
                        output_df = output_df.append({
                                "Model":models,
                                "Sharaf_DG": "O",
                        },ignore_index=True)
                        print(models,"Found")
                        break
                    counter+=1

                if counter == total_models:
                    output_df = output_df.append({
                            "Model":models,
                            "Sharaf_DG": "X",
      
                    },ignore_index=True)
                    print(models,"Not Found")


        
            
                    
                
            


            # driver.get(dyno_link)
            # time.sleep(5)
            # try:
            #     ids = driver.find_element(By.ID,"hits")
            #     all_divs  = ids.find_elements(By.CSS_SELECTOR, ".slide")
            #     number_of_products = len(all_divs)
            #     sharaf_dg_output = "O"
            #     print("Sharf dg Found")

            # except:
            #     sharaf_dg_output = "X"
            #     print("Sharf dg Not Found")
            
            # # Lulu From here 
            # df_link = LULU[LULU['Category'] == cate]
            # keyword = models
            # # print(df_link["Links"])
            # dyno_link = df_link["Links"].iloc[0].format(keyword=keyword)
            # # print(dyno_link)
            # driver.get(dyno_link)
            # time.sleep(5)
            # # try:
            # ids = driver.find_element(By.ID,"moreLoadedProducts")
            # all_divs  = ids.find_elements(By.CSS_SELECTOR, ".product__list--item")
            # # print(len(all_divs))
            # if len(all_divs) <=0:
            #     lulu_output = "X"
            #     print("Lulu Not Found")
            # else:
            #     lulu_output = "O"
            #     print("Lulu Found")
            # # except:
            # #     lulu_output = "X"
            # #     print("Lulu Not Found")

            # # Jumbo From here 
            # df_link = Jumbo[Jumbo['Category'] == cate]
            # keyword = models
            # # print(df_link["Links"])
            # dyno_link = df_link["Links"].iloc[0].format(keyword=keyword)
            # # print(dyno_link)
            # driver.get(dyno_link)
            # time.sleep(5)
            # try:
            #     ids=  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".col-lg-9.border-box.products-list.products-list-en")))
            #     # ids = ids.find_elements(By.CSS_SELECTOR,".list-view")
            #     all_divs  = ids.find_elements(By.CSS_SELECTOR, ".flex.gap-0.flex-col.w-full")
            #     if len(all_divs) <=0:
            #         jumbo_output = "X"
            #         print("Jumbo Not Found")
            #     else:
            #         jumbo_output = "O"
            #         print("Jumbo Found")
                
            #     output_df = output_df.append({
            #             "Model":keyword,
                        
            #             "Sharaf_DG": sharaf_dg_output,
            #             "Lulu": lulu_output,
            #             "Jumbo": jumbo_output,
                        
            #     },ignore_index=True)
                
            # except:
            #     jumbo_output="X"
            #     output_df = output_df.append({
            #             "Model":keyword,
                        
            #             "Sharaf_DG": sharaf_dg_output,
            #             "Lulu": lulu_output,
            #             "Jumbo": jumbo_output,
                        
            #     },ignore_index=True)
            #     print("Jumbo Not Found")


        with pd.ExcelWriter("output.xlsx",mode="a",if_sheet_exists='replace') as writer:
            output_df.to_excel(writer,sheet_name="Sharaf DG")

def InfiniteScrolling(driver):
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(4)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height



def Lulu_Web(driver,list_of_categories,data,Sharaf_DG):
        output_df = pd.DataFrame(columns=['Model','LULU','Top20','Link'])
        for cate in list_of_categories:
            df = data[data['Category'] == cate]
            # print(df)
            list_of_models = df["Model"]
            # We got the models of one category
            check_once = 0
            check_once_top20 = 0
            for models in list_of_models:
                if check_once == 0:
                    print("Model: ",models)
                    df_link = Sharaf_DG[Sharaf_DG['Category'] == cate]
                    keyword = models
                    # print(df_link["Links"])
                    dyno_link = df_link["Links"].iloc[0]
                    # print(dyno_link)
           
                    model_ids :list = []
                    links :list = []
                    driver.get(dyno_link)
                    # Get scroll height
                    InfiniteScrolling(driver)
                    
                    driver.get(dyno_link)
                    time.sleep(5)
                    
                    all_divs  = driver.find_elements(By.CSS_SELECTOR, "div.product-box")
                    print(len(all_divs))
                    
                    for div in all_divs:
                        link = div.find_element(By.TAG_NAME,"a").get_attribute("href")
                        model_id = div.find_element(By.CSS_SELECTOR,"div[class='product-desc']").text
                        print(model_id)
                        # Save this model id in the list and use it later 
                        links.append(link)
                        model_ids.append(model_id)
                    check_once = 1


                total_models = len(model_ids)
                counter = 0
                for each_model in model_ids: 
                    if models.lower() in each_model.lower():
                        out_put_df = {
                                "Model":models,
                                "LULU": "o",
                                "Link": links[counter]
                        }
                        
                        print(models,"Found")
                        break
                    counter+=1
               
                if counter == total_models:
                    output_df = output_df.append({
                            "Model":models,
                            "LULU": "x",
                            "Top20": "x",
                            "Link": ""
      
                    },ignore_index=True)
                    # print(models,"Not Found")
                
                else:
                    #  Open new tab and run the link and check the product is in top 20 or not 
                    #  If its in top 20 then o 
                    #  Else x 
                    if check_once_top20 == 0:
                        list_of_top20 : list = []
                        driver.execute_script("window.open('');")
                        driver.switch_to.window(driver.window_handles[1])
                        driver.get(f"https://www.luluhypermarket.com/en-ae/search/?text={cate}%3Arelevance")
                        time.sleep(10)
                        # driver.set_page_load_timeout(30)

                        try:
                            ids  = driver.find_elements(By.CSS_SELECTOR, "div.product-box")
                            top20Counter = 0 
                            for div in ids:
                                model_id_top20 = div.find_element(By.CSS_SELECTOR,"div[class='product-desc']").text
                                list_of_top20.append(model_id_top20)
                                top20Counter+=1
                                if top20Counter == 20:
                                    break
                            check_once_top20 = 1
                            print("Success")
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                        except:
                            print("Failed")
                            driver.switch_to.window(driver.window_handles[0])
                            driver.close()
                    countertop20Check = 0
                    for md in list_of_top20:
                             
                        if models.lower() in md.lower():
                             out_put_df["Top20"] = "o"
                             output_df = output_df.append(out_put_df,ignore_index=True)  
                             break   
                        countertop20Check+=1
                        if countertop20Check == 20:
                            out_put_df["Top20"] = "x"
                            output_df = output_df.append(out_put_df,ignore_index=True)  
                        # Compare all oled models in the search and check whether its there or not

                            # Save this model id in the list and use it later 
                        # print(model_id)
                    
                # driver.close()
                    

                

        with pd.ExcelWriter("output.xlsx",mode="a",if_sheet_exists='replace') as writer:
            output_df.to_excel(writer,sheet_name="LULU")
        
def Jumbo_Web(driver,list_of_categories,data):

        for cate in list_of_categories:
            df = data[data['Category'] == cate]
            # print(df)
            list_of_models = df["Model"]
            # We got the models of one category
            check_once = 0
            for models in list_of_models:
                if check_once == 0:
                    print("Model: ",models)
                    df_link = Sharaf_DG[Sharaf_DG['Category'] == cate]
                    keyword = models
                    # print(df_link["Links"])
                    dyno_link = df_link["Links"].iloc[0]
                    # print(dyno_link)
                    each_page = 0
                    model_ids :list = []
                    driver.get(dyno_link)
                    time.sleep(5)
                    try:
                        all_pages_ul = driver.find_element(By.ID,"hits-pagination")
                        # Pagination id = "hits-pagination"
                        list_of_li = all_pages_ul.find_elements(By.TAG_NAME,"li")
                        # print(int(list_of_li[-2].text))
                        total_pages = int(list_of_li[len(list_of_li)-2].text)
                        print(total_pages)

                        
                    except:
                        
                        total_pages = 1
                    
                    while each_page < total_pages:
                        Pages = f"&page_number={each_page+1}"
                        driver.get(dyno_link+Pages)
                        time.sleep(5)
                        ids = driver.find_element(By.ID,"hits")
                
                        all_divs  = ids.find_elements(By.CSS_SELECTOR, ".slide")
                        
                        for div in all_divs:
                            link = div.find_element(By.TAG_NAME,"a").get_attribute("href")
                            model_id,check_once = fetch_pdp(driver,link,check_once)
                            print(model_id)
                            # Save this model id in the list and use it later 
                            # 
                            model_ids.append(model_id)


                    
                        each_page += 1
                
                # Compare here now
                if models in model_ids:
                    print(models,"Found")
                else:
                    print(models,"Not Found")


        
            
                    
                
            # Get total number of pages 
                # Open each page 
                # Get all the products links
                # Open one by one and compare the model number with the product model number
                # If found, save O 
                # Else save X
                # Move to next page


            # driver.get(dyno_link)
            # time.sleep(5)
            # try:
            #     ids = driver.find_element(By.ID,"hits")
            #     all_divs  = ids.find_elements(By.CSS_SELECTOR, ".slide")
            #     number_of_products = len(all_divs)
            #     sharaf_dg_output = "O"
            #     print("Sharf dg Found")

            # except:
            #     sharaf_dg_output = "X"
            #     print("Sharf dg Not Found")
            
            # # Lulu From here 
            # df_link = LULU[LULU['Category'] == cate]
            # keyword = models
            # # print(df_link["Links"])
            # dyno_link = df_link["Links"].iloc[0].format(keyword=keyword)
            # # print(dyno_link)
            # driver.get(dyno_link)
            # time.sleep(5)
            # # try:
            # ids = driver.find_element(By.ID,"moreLoadedProducts")
            # all_divs  = ids.find_elements(By.CSS_SELECTOR, ".product__list--item")
            # # print(len(all_divs))
            # if len(all_divs) <=0:
            #     lulu_output = "X"
            #     print("Lulu Not Found")
            # else:
            #     lulu_output = "O"
            #     print("Lulu Found")
            # # except:
            # #     lulu_output = "X"
            # #     print("Lulu Not Found")

            # # Jumbo From here 
            # df_link = Jumbo[Jumbo['Category'] == cate]
            # keyword = models
            # # print(df_link["Links"])
            # dyno_link = df_link["Links"].iloc[0].format(keyword=keyword)
            # # print(dyno_link)
            # driver.get(dyno_link)
            # time.sleep(5)
            # try:
            #     ids=  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".col-lg-9.border-box.products-list.products-list-en")))
            #     # ids = ids.find_elements(By.CSS_SELECTOR,".list-view")
            #     all_divs  = ids.find_elements(By.CSS_SELECTOR, ".flex.gap-0.flex-col.w-full")
            #     if len(all_divs) <=0:
            #         jumbo_output = "X"
            #         print("Jumbo Not Found")
            #     else:
            #         jumbo_output = "O"
            #         print("Jumbo Found")
                
            #     output_df = output_df.append({
            #             "Model":keyword,
                        
            #             "Sharaf_DG": sharaf_dg_output,
            #             "Lulu": lulu_output,
            #             "Jumbo": jumbo_output,
                        
            #     },ignore_index=True)
                
            # except:
            #     jumbo_output="X"
            #     output_df = output_df.append({
            #             "Model":keyword,
                        
            #             "Sharaf_DG": sharaf_dg_output,
            #             "Lulu": lulu_output,
            #             "Jumbo": jumbo_output,
                        
            #     },ignore_index=True)
            #     print("Jumbo Not Found")
 

def Run_Carrefour():




    # 0------------------------------------------------------------------------------
    # df_sharaf_dg_categories_keywords = pd.read_excel("search_keywords.xlsx")
    # df_sharaf_dg_brands = pd.read_excel("input.xlsx")
    data = pd.read_excel("Uae_list.xlsx",sheet_name="Models")
    Carrefour = pd.read_excel("Uae_list.xlsx",sheet_name="Carrefour")
    
    # print(data["Model"])
    
    # print(data["Category"].unique())
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
    list_of_categories = data["Category"].unique()

    Carrefour_Web(driver,list_of_categories,data,Carrefour)


def Run_EMAX():




    # 0------------------------------------------------------------------------------
    # df_sharaf_dg_categories_keywords = pd.read_excel("search_keywords.xlsx")
    # df_sharaf_dg_brands = pd.read_excel("input.xlsx")
    data = pd.read_excel("EMAX_models.xlsx",sheet_name="Models")
    Emax = pd.read_excel("EMAX_models.xlsx",sheet_name="EMAX")
    
    # print(data["Model"])
    
    # print(data["Category"].unique())
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
    list_of_categories = data["Category"].unique()

    Emax_Web(driver,list_of_categories,data,Emax)


def Run_Sharaf_DG():




    # 0------------------------------------------------------------------------------
    # df_sharaf_dg_categories_keywords = pd.read_excel("search_keywords.xlsx")
    # df_sharaf_dg_brands = pd.read_excel("input.xlsx")
    data = pd.read_excel("models.xlsx",sheet_name="Models")
    Sharaf_DG = pd.read_excel("models.xlsx",sheet_name="Sharaf_DG")
   
    # print(data["Model"])
    
    # print(data["Category"].unique())
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
    list_of_categories = data["Category"].unique()

    Sharaf_DG_Web(driver,list_of_categories,data,Sharaf_DG)
   
def Run_LULU():




    # 0------------------------------------------------------------------------------
    # df_sharaf_dg_categories_keywords = pd.read_excel("search_keywords.xlsx")
    # df_sharaf_dg_brands = pd.read_excel("input.xlsx")
    data = pd.read_excel("models.xlsx",sheet_name="Models")
    # Sharaf_DG = pd.read_excel("models.xlsx",sheet_name="Sharaf_DG")
    LULU = pd.read_excel("models.xlsx",sheet_name="LULU")
    # Jumbo = pd.read_excel("models.xlsx",sheet_name="Jumbo")
    # output_df = pd.DataFrame(columns=['Model','Sharaf_DG'])
    # print(data["Model"])
    
    # print(data["Category"].unique())
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
    list_of_categories = data["Category"].unique()

    # Sharaf_DG_Web(driver,list_of_categories,data,Sharaf_DG)
    Lulu_Web(driver,list_of_categories,data,LULU)
   
def Run_Jumbo():




    # 0------------------------------------------------------------------------------
    # df_sharaf_dg_categories_keywords = pd.read_excel("search_keywords.xlsx")
    # df_sharaf_dg_brands = pd.read_excel("input.xlsx")
    data = pd.read_excel("models.xlsx",sheet_name="Models")
    Sharaf_DG = pd.read_excel("models.xlsx",sheet_name="Sharaf_DG")
    LULU = pd.read_excel("models.xlsx",sheet_name="LULU")
    Jumbo = pd.read_excel("models.xlsx",sheet_name="Jumbo")
    output_df = pd.DataFrame(columns=['Model','Sharaf_DG'])
    # print(data["Model"])
    
    # print(data["Category"].unique())
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome()
    list_of_categories = data["Category"].unique()

    # Sharaf_DG_Web(driver,list_of_categories,data,Sharaf_DG)
    # Lulu_Web(driver,list_of_categories,data,LULU)
    Jumbo_Web(driver,list_of_categories,data,Jumbo)

        


        
            
    


# Main App 
class App:

    def __init__(self, root):
        #setting title
        root.title("UAE Model Check")
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
        ClickBtnLabel["text"] = "UAE Model Check"
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

        running_actions = [
            Run_Sharaf_DG, 

            # Run_LULU,
            # Run_Carrefour,         
            # Run_EMAX,
            # Run_Jumbo          # waiting for models (paused)

        ]

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


# Run()

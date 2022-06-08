from lib2to3.pgen2 import driver
import time 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd 

# Function to get the product elements 
def get_urls_list():
    """ Gets the product elements from first three pages under the top 
        sales tab and returns a list which contains product urls of 
        individual products. 
    """

    #web elements of the products in the given page 
    urls_list = []
    # For iterating over three pages
    for page in range(3):
        prod = driver.find_elements_by_class_name("col-xs-2-4")
        print("The len of single page prod : ",len(prod))
        urls = get_urls(prod)
        urls_list += urls
        # Time for all webelements to load 
        time.sleep(3)
        # Scrolling through the website, to overcome lazy loading 
        driver.execute_script("window.scrollTo(0, window.scrollY + 200)")
        time.sleep(3)
        get_next_page()
    return urls_list

def get_next_page():
    """ clicks the next page 
        
    """
    driver.find_element_by_xpath('//*[@id="main"]/div/div[3]/div/div[4]/div[2]/div/div[3]/div/button[8]').click

def get_urls(products):
    """ Gets the urls of the given product element 
        and returns a list of urls 

        products : A list which contains product elements
        under the specified class name
    """
    # list to store the extracted urls
    urls = []    
    for item in products:
        try:
            WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"col-xs-2-4")))
            driver.execute_script("window.scrollTo(0, window.scrollY + 200)")
            a = item.find_element_by_tag_name("a").get_property("href")
            #Append to the urls list
            urls.append(a)
        except:
            print("Exception thrown")
    return urls

def get_product_details(urls):
    """ Scrapes the details from each url and stores in a dictionary
        and returns the dictionary inside a list 

        urls : A list which contains urls of different product in the list 
    """
    print("length of the list urls : ",len(urls))
    temp_list = []
    
    for ele in range(1, len(urls)):
        driver.get(url = urls[ele])
        time.sleep(3)
        print("Count of the product : ",ele)
        # title of the product 
        try:
            prod_title = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[3]/div/div[1]/span').text
        except:
            prod_title = None
        # price of the product 
        try:
            price = driver.find_element_by_class_name("pmmxKx").text
        except:
            price = None
        # brand of the product 
        try:
            brand = driver.find_element_by_class_name("kQy1zo").text
        except:
            brand = None
        # description of the product 
        try:
            description = driver.find_element_by_class_name('hrQhmh').text
        except:
            description = None
        # Units sold for the product 
        try: 
            units_sold = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div[3]/div[1]').text
        except:
            units_sold = None
        try:
            rating = driver.find_element_by_class_name('MrYJVA').text
        except:
            rating = None 
        # Define a dictionary with details we need
        r = {   
            "Title":prod_title,
            "Product Url": urls[ele],
            "Price":price,
            "Brand": brand,
            "Rating": rating,
            "Units Sold": units_sold,
            "Product Description": description
        }
        temp_list.append(r)
    driver.close()
    return temp_list

def get_as_csv(temp_list):
    """ Stores the scrapped data from the website to a csv file 

        temp_list : A list which contains the product details 
    """
    # converting the list into a dataframe 
    df = pd.DataFrame(temp_list)
    print("Inside get_as_csv")
    df.to_csv("scrapped_data10.csv", index=False)
    
def main(website):
    driver.get(website)
    driver.maximize_window()
    url_list  = get_urls_list()
    temporary_list_1 = get_product_details(url_list)
    get_as_csv(temporary_list_1)


if __name__ == "__main__":
    # Location of chromedrive in local system 
    website = input("Enter the website link : ")
    PATH = "C:/Users/josephan/Desktop/Python_files/chromedriver"
    driver = webdriver.Chrome(PATH)
    # website to be scrapped from https://shopee.sg/Beauty-Personal-Care-cat.11012301?page=0&sortBy=sales
    main(website)
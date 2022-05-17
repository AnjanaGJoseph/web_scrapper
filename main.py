from operator import le
import time 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd 

# Function to get the product elements 
def get_product_elements():
    """ Gets the product elements under the page top 
        sales and returns a list of product elements. 
    """

    #web elements of the products in the given page 
    #class_name = input("Enter the product container class name : ")
    '''products_ele_list = []
    #For scrapping data from next 3 pages
    for page in range(2):
        products = driver.find_elements_by_class_name("col-xs-2-4")
        products_ele_list.append(products)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.find_element_by_xpath('//*[@id="main"]/div/div[3]/div/div[4]/div[2]/div/div[3]/div/button[8]').click()
    print("Total num of products is : ",len(products_ele_list))'''
    products = driver.find_elements_by_class_name("col-xs-2-4")
    return products


def get_urls(products):
    """ Gets the urls of the given product element 
        and returns a list of urls 

        products : A list which contains product elements
        under the specified class name
    """
    # list to store the extracted urls
    urls = []    
    for item in products:
        #driver.implicitly_wait(5)
        try:
            WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"col-xs-2-4")))
            driver.execute_script("window.scrollTo(0, window.scrollY + 200)")
            a = item.find_element_by_tag_name("a").get_property("href")
            #Append to the urls list
            print("The link is",a)
            urls.append(a)
        except:
            #driver.implicitly_wait(10)
            print("Exception thrown")
            #print('Page Refresh!')
            #driver.refresh()
    return urls



def get_product_details(urls):
    """ Scrapes the details from each url and stores in a dictionary
        and returns the dictionary inside a list 

        urls : A list which contains urls of different product in the list 
    """
    print("length of the list urls : ",len(urls))
    temp_list = []
    for ele in urls:
        driver.get(url=ele)
        time.sleep(5)
        # title of the product 
        prod_title = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[3]/div/div[1]/span').text
        # price of the product 
        price = driver.find_element_by_class_name("pmmxKx")
        # brand of the product 
        try:
            brand = driver.find_element_by_class_name("kQy1zo").text
        except:
            brand = None
        # Stock availability of the product 
        #stock = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div').text
        # description of the product 
        try:
            description = driver.find_element_by_class_name('hrQhmh').text
        except:
            description = None
        # Units sold for the product 
        units_sold = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div[3]/div[1]').text
        # Define a dictionary with details we need
        r = {
            "Title":prod_title,
            "Product Url": ele,
            "Price":price.text,
            "Brand": brand,
            #"Stock": stock,
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
    df.to_csv("scrapped_data7.csv")
    
def main(website):
    driver.get(website)
    driver.maximize_window()
    prod = get_product_elements()
    link = get_urls(prod)
    temporary_list = get_product_details(link)
    get_as_csv(temporary_list)



if __name__ == "__main__":
    # Location of chromedrive in local system 
    website = input("Enter the website link : ")
    PATH = "C:/Users/josephan/Desktop/Python_files/chromedriver"
    driver = webdriver.Chrome(PATH)
    #driver.implicitly_wait(5)
    # website to be scrapped from https://shopee.sg/Beauty-Personal-Care-cat.11012301?page=0&sortBy=sales
    main(website)
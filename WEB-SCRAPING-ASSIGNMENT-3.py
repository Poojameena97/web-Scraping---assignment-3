#!/usr/bin/env python
# coding: utf-8

# #                          Web Scraping Assignment - 3

# # Importing necessary libraries

# In[1]:


import pandas as pd
import selenium
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import requests
import re
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait


# # Q1:  Write a python program which searches all the product under a particular product vertical from www.amazon.in. The product verticals to be searched will be taken as input from user. For e.g. If user input is ‘guitar’. Then search for guitars.

# In[2]:


# connecting to the webdriver
driver=webdriver.Chrome(r"C:/Users/HP/Downloads/chromedriver_win32 (1)/chromedriver.exe")


# In[3]:


# getting the webpage of mentioned url
url = "https://www.amazon.in/"
driver.get(url)


# In[4]:


# entering the product that we want to search
user_input = input('Enter the product that we want to search : ')


# In[5]:


# searching the web element for user input
search = driver.find_element_by_id("twotabsearchtextbox")
search

# sending the user input to search bar
search.send_keys(user_input)

# locating the search button using xpath
search_btn = driver.find_element_by_xpath("//div[@class='nav-search-submit nav-sprite']/span/input")

# clicking on search button
search_btn.click()


# In[ ]:





# In[ ]:





# # Q2 : In the above question, now scrape the following details of each product listed in first 3 pages of your search results and save it in a data frame and csv. In case if any product vertical has less than 3 pages in search results then scrape all the products available under that product vertical. Details to be scraped are: "Brand Name", "Name of the Product", "Rating", "No. of Ratings", "Price", "Return/Exchange", "Expected Delivery", "Availability", "Other Details" and “Product URL”. In case, if any of the details are missing for any of the product then replace it by “-“.

# In[6]:


# fetching URLs to open the pages
urls = []          # empty list
for i in range(0,3):      # for loop to scrape 3 pages
    page_url = driver.find_elements_by_xpath("//a[@class='a-link-normal a-text-normal']")
    for i in page_url:
        urls.append(i.get_attribute("href"))
        next_btn = driver.find_element_by_xpath("//li[@class='a-last']/a")
        time.sleep(3)


# In[7]:


len(urls)


# In[8]:


# making empty list and fetching required data
brand_name = []
product_name = []
ratings = []
num_ratings = []
prices = []
exchange = []
exp_delivery = []
availability = []
other_details = []

for i in urls:
    driver.get(i)
    time.sleep(3)
    
    
    #fetching brand name 
    try:
        brand = driver.find_element_by_xpath("//a[@id='bylineInfo']")
        brand_name.append(brand.text)
    except NoSuchElementException:
        brand_name.append('-')
    
    
    # fetching Name of the Product
    try:
        product = driver.find_element_by_xpath("//span[@id='productTitle']")
        product_name.append(product.text)
    except NoSuchElementException:
        product_name.append('-')
        
        

     #fetching ratings
    try:
        rating = driver.find_element_by_xpath("//span[@class='a-size-base a-nowrap']/span")
        ratings.append(rating.text)
    except NoSuchElementException:
        ratings.append('-')
        
 
    #fetching  no of ratings
    try:
        num_rating = driver.find_element_by_xpath("//span[@id='acrCustomerReviewText']")
        num_ratings.append(num_rating.text)
    except NoSuchElementException:
        num_ratings.append('-')
        

    #fetching price of the product
    try:
        price = driver.find_element_by_xpath("//td[@class='a-span12']")
        prices.append(price.text)
    except NoSuchElementException:
        prices.append('-')
        
        
    #fetching return/exchange
    try:
        exch = driver.find_element_by_xpath("//span[@class='a-declarative']/div/a")
        exchange.append(exch.text)
    except NoSuchElementException:
        exchange.append('-')
        

    #fetching expected delivery
    try:
        delivery = driver.find_element_by_xpath("//div[@class='a-section a-spacing-mini']/b")
        exp_delivery.append(delivery.text)
    except NoSuchElementException:
        exp_delivery.append('-')
        

    #fetching availability information
    try:
        avail = driver.find_element_by_xpath("//span[@class='a-size-medium a-color-success']")
        availability.append(avail.text)
    except NoSuchElementException:
        availability.append('-')
        
    #other details
    try:
        oth_det = driver.find_element_by_xpath("//ul[@class='a-unordered-list a-vertical a-spacing-mini']")
        other_details.append(oth_det.text)
    except NoSuchElementException:
        other_details.append('-')
        


# In[9]:


print(len(brand_name),
len(product_name),
len(ratings),
len(num_ratings),
len(prices),
len(exchange),
len(exp_delivery),
len(availability),
len(other_details))


# In[11]:


# Creating the DataFrame for the scraped data

guitar = pd.DataFrame({})
guitar['Brand Name'] = brand_name
guitar['Name of the Product'] = product_name
guitar['Rating'] = ratings
guitar['No. of Ratings'] = num_ratings
guitar['Price'] = prices
guitar['Return/Exchange'] = exchange
guitar['Expected Delivery'] = exp_delivery
guitar['Availability'] = availability
guitar['Other Details'] = other_details
guitar['Product URL'] = urls
guitar


# In[12]:


#saving the data in csv
guitar.to_csv("Guitar.csv")


# In[13]:


driver.close()


# In[ ]:





# # Q3 : Write a python program to access the search bar and search button on images.google.com and scrape 100 images each for keywords ‘fruits’, ‘cars’ and ‘Machine Learning’.  

# In[14]:


# connecting to the webdriver
driver=webdriver.Chrome(r"C:/Users/HP/Downloads/chromedriver_win32 (1)/chromedriver.exe")


# In[17]:


# geting the webpage of mentioned url
url = "http://images.google.com/"

# creating empty list
urls = []
data = []

search_item = ["Fruits","Cars","Machine Learning"]
for item in search_item:
    driver.get(url)
    time.sleep(5)
    
    # finding webelement for search_bar
    search_bar = driver.find_element_by_tag_name("input")
    
    # sending keys to get the keyword for search bar
    search_bar.send_keys(str(item))
    
    # clicking on search button
    search_button = driver.find_element_by_xpath("//button[@class='Tg7LZd']").click()
    
    # scroling down the webpage to get some more images
    for _ in range(500):
        driver.execute_script("window.scrollBy(0,100)")
        
        imgs = driver.find_elements_by_xpath("//img[@class='rg_i Q4LuWd']")
    img_url = []
    for image in imgs:
        source = image.get_attribute('src')
        if source is not None:
            if(source[0:4] == 'http'):
                img_url.append(source)
    for i in img_url[:100]:
        urls.append(i)
        
for i in range(len(urls)):
    if i >= 300:
        break
    print("Doenloading {0} of {1} images" .format(i,300))
    response = requests.get(urls[i])
    
    file = open(r"E:\google\images"+str(i)+".jpg","wb")
    
    file.write(response.content)


# In[18]:


driver.close()


# In[ ]:





# # Q4 :  Write a python program to search for a smartphone(e.g.: Oneplus Nord, pixel 4A, etc.) on www.flipkart.com and scrape following details for all the search results displayed on 1st page. Details to be scraped: “Brand Name”, “Smartphone name”, “Colour”, “RAM”, “Storage(ROM)”, “Primary Camera”, “Secondary Camera”, “Display Size”, “Display Resolution”, “Processor”, “Processor Cores”, “Battery Capacity”, “Price”, “Product URL”. Incase if any of the details is missing then replace it by “- “. Save your results in a dataframe and CSV.

# In[2]:


# connecting to the webdriver
driver=webdriver.Chrome(r"C:/Users/HP/Downloads/chromedriver_win32 (1)/chromedriver.exe")


# In[3]:


# getting the webpage of mentioned url
url = "https://www.flipkart.com/"
driver.get(url)


# In[4]:


# closing login popup button
lonin_x_btn = driver.find_element_by_xpath("//div[@class='_2QfC02']//button").click()


# In[5]:


# search for web element
search_bar = driver.find_element_by_xpath("//input[@class='_3704LK']")

# sending keys to search product
search_bar.send_keys("pixel 4A")


# In[6]:


# location the search button using xpath
search_btn = driver.find_element_by_xpath("//button[@class='L0Z3Pu']")

# clicking on search button
search_btn.click()


# In[7]:


# fetching 1st page of URLs of smartphone
page1_url = []
urls = driver.find_elements_by_xpath("//a[@class='_1fQZEK']")
for url in urls:
    page1_url.append(url.get_attribute('href'))


# In[8]:


len(page1_url)


# In[9]:


# creating empty list
Smartphones = ({})
Smartphones['Brand'] = []
Smartphones['Phone name'] = []
Smartphones['Colour'] = []
Smartphones['RAM'] = []
Smartphones['Storage(ROM)'] = []
Smartphones['Primary Camera'] = []
Smartphones['Secondary Camera'] = []
Smartphones['Display Size'] = []
Smartphones['Display Resolution'] = []
Smartphones['Processor'] = []
Smartphones['Processor Cores'] = []
Smartphones['Battery Capacity'] = []
Smartphones['Price'] = []
Smartphones['URL'] = []


# In[10]:


# scraping data from each url of page 1
for url in page1_url:
    driver.get(url)
    print("Scraping URL = ",url)
    Smartphones['URL'].append(url)
    time.sleep(2)
    
    
    #clicking on read more button to get more information
    try:
        read_more = driver.find_element_by_xpath("//button[@class='_2KpZ6l _1FH0tX']")
        read_more.click()
    except NoSuchElementException:
        print("Exception occured while moving to next page")
    
    #scraping brand name of smartphone
    try:
        brand_tags = driver.find_element_by_xpath("//span[@class='B_NuCI']")
        Smartphones['Brand'].append(brand_tags.text.split()[0])
    except NoSuchElementException:
        Smartphones['Brand'].append('-')
    
    
    # scraping name of smartphones
    try:
        name_tags = driver.find_element_by_xpath("//div[@class='_3k-BhJ'][1]/table/tbody/tr[3]/td[2]/ul/li")
        Smartphones['Phone name'].append(name_tags.text)
    except NoSuchElementException:
        Smartphones['Phone name'].append('-')
        
    #scraping colour of smartphone
    try:
        color_tags = driver.find_element_by_xpath("//div[@class='_3k-BhJ'][1]/table/tbody/tr[4]/td[2]/ul/li")
        Smartphones['Colour'].append(color_tags.text)
    except NoSuchElementException:
        Smartphones['Colour'].append('-')
        
    # scraping RAM data of smartphone
    try:
        ram_tags = driver.find_element_by_xpath("//div[@class='_3k-BhJ'][4]/table[1]/tbody/tr[2]/td[2]/ul/li")
        Smartphones['RAM'].append(ram_tags.text)
    except NoSuchElementException:
        Smartphones['RAM'].append('-')
        
    #scraping ROM data of smartphones
    try:
        rom = driver.find_element_by_xpath("//div[@class='_3k-BhJ'][4]/table[1]/tbody/tr[1]/td[2]/ul/li")
        Smartphones['Storage(ROM)'].append(rom.text)
    except NoSuchElementException:
        Smartphones['Storage(ROM)'].append('-')
        
    # scraping  Primary camera data of smartphone
    try:
        pri =driver.find_element_by_xpath("//div[@class='_3k-BhJ'][5]/table[1]/tbody/tr[2]/td[2]/ul/li")
        Smartphones['Primary Camera'].append(pri.text)
    except NoSuchElementException:
        Smartphones['Primary Camera'].append('-')
        
    # scraping secondary camera data of smartphone
    try:
        sec = driver.find_element_by_xpath("//div[@class='_3k-BhJ'][5]/table[1]/tbody/tr[6]/td[1]")
        if sec != 'Secondary Camera' :
            if driver.find_element_by_xpath("//div[@class='_3k-BhJ'][5]/table[1]/tbody/tr[5]/td[1]").text == "Secondary Camera":
                sec_cam =driver.find_element_by_xpath("//div[@class='_3k-BhJ'][5]/table[1]/tbody/tr[5]/td[2]/ul/li")
            else :
                raise NoSuchElementException
        else :
            sec_cam = driver.find_element_by_xpath("//div[@class='_3k-BhJ'][5]/table[1]/tbody/tr[6]/td[2]/ul/li")
        Smartphones['Secondary Camera'].append(sec_cam.text)
    except NoSuchElementException:
        Smartphones['Secondary Camera'].append('-')
        
    
    #scraping display size data of smartphone
    try:
        disp = driver.find_element_by_xpath("//div[@class='_3k-BhJ'][2]/div")
        if disp.text != 'Display Features' : raise NoSuchElementException
        disp_size = driver.find_element_by_xpath("//div[@class='_3k-BhJ'][2]/table[1]/tbody/tr[1]/td[2]/ul/li")
        Smartphones['Display Size'].append(disp_size.text)
    except NoSuchElementException:
        Smartphones['Display Size'].append('-')
        
    
    #scraping display resolution of smartphone
    try:
        disp = driver.find_element_by_xpath("//div[@class='_3k-BhJ'][2]/div")
        if disp.text != 'Display Features' : raise NoSuchElementException
        disp_reso = driver.find_element_by_xpath("//div[@class='_3k-BhJ'][2]/table[1]/tbody/tr[2]/td[2]/ul/li")
        Smartphones['Display Resolution'].append(disp_reso.text)
    except NoSuchElementException:
        Smartphones['Display Resolution'].append('-')
        
        
    #scraping processor of smartphone
    try:
        pro = driver.find_element_by_xpath("//div[@class='_3k-BhJ'][3]/table[1]/tbody/tr[2]/td[1]]")
        if pro.text != 'Processor Type' : raise NoSuchElementException
        processor = driver.find_element_by_xpath("//div[@class='_3k-BhJ'][3]/table[1]/tbody/tr[2]/td[2]/ul/li")
        Smartphones['Processor'].append(processor.text)
    except NoSuchElementException:
        Smartphones['Processor'].append('-')
    
        
       
    # scraping processor core of smartphone
    try:
        core = driver.find_element_by_xpath("//div[@class='_3k-BhJ'][3]/table[1]/tbody/tr[3]/td[1]")
        if core.text != 'Processor Core' :
            core = driver.find_element_by_xpath("//div[@class='_3k-BhJ'][3]/table[1]/tbody/tr[2]/td[1]")
            if core.text != 'Processor Core' :
                raise NoSuchElementException
            else :
                cores = driver.find_element_by_xpath("//div[@class='_3k-BhJ'][3]/table[1]/tbody/tr[2]/td[2]/ul/li")
        else :
            cores = driver.find_element_by_xpath("//div[@class='_3k-BhJ'][3]/table[1]/tbody/tr[3]/td[2]/ul/li")
        Smartphones['Processor Cores'].append(disp_reso.text)
    except NoSuchElementException:
        Smartphones['Processor Cores'].append('-')
        
        
        
    # scraping the battery capacity of smartphone
    try:
        if driver.find_element_by_xpath("//div[@class='_3k-BhJ'][10]/div").text != "Battery & Power Features" :
            if driver.find_element_by_xpath("//div[@class='_3k-BhJ'][9]/div").text == "Battery & Power Features" :
                bat_tags = driver.find_element_by_xpath("//div[@class='_3k-BhJ'][9]/table/tbody/tr/td[1]")
                if bat_tags.text != "Battery Capacity" : raise NoSuchElementException
                bat_capa = driver.find_element_by_xpath("//div[@class='_3k-BhJ'][9]/table/tbody/tr/td[2]/ul/li")
            elif driver.find_element_by_xpath("//div[@class='_3k-BhJ'][8]/div").text == "Battery & Power Features" :
                bat_tags = driver.find_element_by_xpath("//div[@class='_3k-BhJ'][8]/table/tbody/tr/td[1]")
                if bat_tags.text != "Battery Capacity" : raise NoSuchElementException
                bat_capa = driver.find_element_by_xpath("//div[@class='_3k-BhJ'][8]/table/tbody/tr/td[2]/ul/li")
            else:
                raise NoSuchElementException
        else :
            bat_tags = driver.find_element_by_xpath("//div[@class='_3k-BhJ'][10]/table/tbody/tr/td[1]")
            if bat_tags.text != "Battery Capacity" : raise NoSuchElementException
            bat_capa = driver.find_element_by_xpath("//div[@class='_3k-BhJ'][10]/table/tbody/tr/td[2]/ul/li")
        Smartphones['Battery Capacity'].append(bat_capa.text)
    except NoSuchElementException:
        Smartphones['Battery Capacity'].append('-')
    
    
    
    
    # scraping price of smartphone
    try:
        price_tags = driver.find_element_by_xpath("//div[@class='_30jeq3 _16Jk6d']")
        Smartphones['Price'].append(price_tags.text)
    except NoSuchElementException:
          Smartphones['Price'].append('-')         


# In[11]:


# checking lengths of all scraped data

print(len(Smartphones['Brand']),len(Smartphones['Phone name']), len(Smartphones['Colour']),len(Smartphones['RAM']),len(Smartphones['Storage(ROM)']),len(Smartphones['Primary Camera']),len(Smartphones['Secondary Camera']), len(Smartphones['Display Size']), len(Smartphones['Display Resolution']), len(Smartphones['Processor']), len(Smartphones['Processor Cores']), len(Smartphones['Battery Capacity']), len(Smartphones['Price']), len(Smartphones['URL'])) 


# In[12]:


# framing the DataFrame

df = pd.DataFrame.from_dict(Smartphones)
df


# In[13]:


# saving the data in csv
df.to_csv("smartphones.csv")


# In[15]:


driver.close()


# In[ ]:





# # Q5 : Write a program to scrap geospatial coordinates (latitude, longitude) of a city searched on google maps.

# In[16]:


# connecting to the webdriver
driver=webdriver.Chrome(r"C:/Users/HP/Downloads/chromedriver_win32 (1)/chromedriver.exe")


# In[17]:


# getting mentioned url and opening google maps web page
url = 'https://www.google.co.in/maps'
driver.get(url)
time.sleep(2)


# In[18]:


# entering the city name in search bar
City = input('Enter City name that has to be searched : ')
search_bar = driver.find_element_by_id('searchboxinput')
search_bar.click()
time.sleep(2)

#sending keys to find cities
search_bar.send_keys(City)

#checking for webelement and clicking on search button
search_btn = driver.find_element_by_id("searchbox-searchbutton")
search_btn.click()
time.sleep(2)

try:
    url_str = driver.current_url
    print("URL Extracted: ", url_str)
    latitude_longitude = re.findall(r'@(.*)data',url_str)
    if len(latitude_longitude):
        lat_lng_list = latitude_longitude[0].split(",")
        if len(lat_lng_list)>=2:
            latitude = lat_lng_list[0]
            longitude = lat_lng_list[1]
        print("Latitude = {}, Longitude = {}".format(latitude, longitude))
except Exception as e:
        print("Error: ", str(e))


# In[19]:


driver.close()


# In[ ]:





# # Q6 : Write a program to scrap details of all the funding deals for second quarter (i.e. July 20 – September 20) from trak.in.

# In[20]:


# connecting to the webdriver
driver=webdriver.Chrome(r"C:/Users/HP/Downloads/chromedriver_win32 (1)/chromedriver.exe")


# In[21]:


# opening the url track.in
url = "https://trak.in/"
driver.get(url)
time.sleep(2)


# In[29]:


# getting xpath for funding deals and clicking on the button
fund_button = driver.find_element_by_xpath("//li[@id='menu-item-51510']/a").get_attribute('href')
driver.get(fund_button)

#Empty Lists
fund_deals = {}
fund_deals['Date'] = []
fund_deals['Startup Name'] = []
fund_deals['Industry/Vertical'] = []
fund_deals['Sub_Vertical'] = []
fund_deals['Location'] = []
fund_deals['Investor'] = []
fund_deals['Investment Type'] = []
fund_deals['Amount(in USD)'] = []


for i in range(48,51):
    
    # scraping data of data
    date = driver.find_elements_by_xpath("//table[@id='tablepress-{}']/tbody/tr/td[2]".format(i))
    for d in date:
        fund_deals['Date'].append(d.text)
        
    # scraping data of startup name
    startup_name = driver.find_elements_by_xpath("//table[@id='tablepress-{}']/tbody/tr/td[3]".format(i))
    for name in startup_name:
        fund_deals['Startup Name'].append(name.text)
        
    
    #scraping data of industry or vertical
    industry = driver.find_elements_by_xpath("//table[@id='tablepress-{}']/tbody/tr/td[4]".format(i))
    for ind in industry:
        fund_deals['Industry/Vertical'].append(ind.text)
        
    
    #scraping data of sub-vertical
    sub_vertical = driver.find_elements_by_xpath("//table[@id='tablepress-{}']/tbody/tr/td[5]".format(i))
    for sv in sub_vertical:
        fund_deals['Sub_Vertical'].append(sv.text)
        
        
    # scraping data of location
    location = driver.find_elements_by_xpath("//table[@id='tablepress-{}']/tbody/tr/td[6]".format(i))
    for loc in location:
        fund_deals['Location'].append(loc.text)
        
        
    # scraping data of investor
    investor = driver.find_elements_by_xpath("//table[@id='tablepress-{}']/tbody/tr/td[7]".format(i))
    for invest in investor:
        fund_deals['Investor'].append(invest.text)
        
        
    # scraping data of investment type
    investment_type = driver.find_elements_by_xpath("//table[@id='tablepress-{}']/tbody/tr/td[8]".format(i))
    for invtype in investment_type:
        fund_deals['Investment Type'].append(invtype.text)
        
        
    # scraping data of amount
    amount = driver.find_elements_by_xpath("//table[@id='tablepress-{}']/tbody/tr/td[9]".format(i))
    for amt in amount:
        fund_deals['Amount(in USD)'].append(amt.text)
    


# In[30]:


# checking lengths of all scraped data
print(len(fund_deals['Date']),
len(fund_deals['Startup Name']),
len(fund_deals['Industry/Vertical']),
len(fund_deals['Sub_Vertical']),
len(fund_deals['Location']),
len(fund_deals['Investor']),
len(fund_deals['Investment Type']),
len(fund_deals['Amount(in USD)'] 
))


# In[31]:


# creating DataFrame for scraped data
fund_data = pd.DataFrame(fund_deals)
fund_data


# In[32]:


# saving data in csv file
fund_data.to_csv("trak_in.csv")


# In[33]:


driver.close()


# In[ ]:





# # Q7 :  Write a program to scrap all the available details of best gaming laptops from digit.in.

# In[2]:


# connecting to the webdriver
driver=webdriver.Chrome(r"C:/Users/HP/Downloads/chromedriver_win32 (1)/chromedriver.exe")


# In[3]:


# opening the url digit.in
url = "https://www.digit.in/"
driver.get(url)
time.sleep(2)


# In[4]:


# searching for best Laptop
best_gam_laptops = driver.find_element_by_xpath("//div[@class='listing_container']//ul//li[9]").click()
time.sleep(3)


# In[5]:


# creating empty list
Laptop_Name = []
Operating_sys = []
Display = []
Processor = []
Memory = []
Weight = []
Dimensions = []
Graph_proc = []
Price = []


# In[6]:


#scraping the data of laptop names
laptop_name = driver.find_elements_by_xpath("//div[@class='right-container']/div/a/h3")
for name in laptop_name:
    Laptop_Name.append(name.text)
    
#scraping the data of operating system
try:
    op_sys = driver.find_elements_by_xpath("//div[@class='product-detail']/div/ul/li[1]/div/div")
    for os in op_sys:
        Operating_sys.append(os.text)
except NoSuchElementException:
    pass


#scraping data of display of the Laptop
try:
    display = driver.find_elements_by_xpath("//div[@class='product-detail']/div/ul/li[2]/div/div")
    for disp in display:
        Display.append(disp.text)
except NoSuchElementException:
    pass


# scraping data of processor
try:
    processor = driver.find_elements_by_xpath("//div[@class='Spcs-details'][1]/table/tbody/tr[5]/td[3]")
    for pro in processor:
        Processor.append(pro.text)
except NoSuchElementException:
    pass


# scraping the data of memory
try:
    memory = driver.find_elements_by_xpath("//div[@class='Spcs-details'][1]/table/tbody/tr[6]/td[3]")
    for memo in memory:
        Memory.append(memo.text)
except NoSuchElementException:
    pass


# scraping data of weight
try:
    weight = driver.find_elements_by_xpath("//div[@class='Spcs-details'][1]/table/tbody/tr[7]/td[3]")
    for wgt in weight:
        Weight.append(wgt.text)
except NoSuchElementException:
    pass


# scraping data of dimensions
try:
    dimension = driver.find_elements_by_xpath("//div[@class='Spcs-details'][1]/table/tbody/tr[8]/td[3]")
    for dim in dimension:
        Dimensions.append(dim.text)
except NoSuchElementException:
    pass


# scraping data of graph processor
try:
    graph = driver.find_elements_by_xpath("//div[@class='Spcs-details'][1]/table/tbody/tr[9]/td[3]")
    for gra in graph:
        Graph_proc.append(gra.text)
except NoSuchElementException:
    pass


# scraping the data of price
try:
    price = driver.find_elements_by_xpath("//td[@class='smprice']")
    for pri in price:
        Price.append(pri.text.replace('₹ ','Rs'))
except NoSuchElementException:
    pass


# In[7]:


print(len(Laptop_Name),
len(Operating_sys),
len(Display),
len(Processor),
len(Memory),
len(Weight),
len(Dimensions),
len(Graph_proc),
len(Price))


# In[8]:


#creating DataFrame for scraped data
Gaming_Laptop=pd.DataFrame({})
Gaming_Laptop['Laptop Name'] = Laptop_Name
Gaming_Laptop['Operating System'] =Operating_sys
Gaming_Laptop['Display'] = Display
Gaming_Laptop['Processor'] = Processor
Gaming_Laptop['Memory'] = Memory
Gaming_Laptop['Weight'] = Weight
Gaming_Laptop['Dimensions'] = Dimensions
Gaming_Laptop['Graphical Processor'] = Graph_proc
Gaming_Laptop['Price'] = Price
Gaming_Laptop


# In[9]:


# saving the data to csv
Gaming_Laptop.to_csv("Gaming_Laptops.csv")


# In[10]:


driver.close()


# In[ ]:





# In[ ]:





# # Q8 : Write a python program to scrape the details for all billionaires from www.forbes.com. Details to be scrapped: “Rank”, “Name”, “Net worth”, “Age”, “Citizenship”, “Source”, “Industry

# In[2]:


# connecting to the webdriver
driver=webdriver.Chrome(r"C:/Users/HP/Downloads/chromedriver_win32 (1)/chromedriver.exe")


# In[3]:


# getting the specified url
url = "https://www.forbes.com/?sh=41bd46d2254c"
driver.get(url)


# In[4]:


#let's get option button from the page
opt_btn = driver.find_element_by_xpath("//div[@class='header__left']//button")
opt_btn.click()
time.sleep(3)

#select billionaires from options
blns = driver.find_element_by_xpath("/html/body/div[1]/header/nav/div[3]/ul/li[1]")
blns.click()
time.sleep(3)
#select world billionaire
bln_list = driver.find_element_by_xpath("/html/body/div[1]/header/nav/div[3]/ul/li[1]/div[2]/ul/li[2]/a")
bln_list.click()
time.sleep(4)


# In[5]:


# scraping required data from the web page
# creating empty lists
Rank = []
Person_Name = []
Net_worth = []
Age = []
Citizenship = []
Source = []
Industry = []


while(True):
    
    # scraping the data of rank of the billionaires
    rank_tag = driver.find_elements_by_xpath("//div[@class='rank']")
    for rank in rank_tag:
        Rank.append(rank.text)
    time.sleep(1)
    
    
 
    # scraping the data  of names of the billionaires
    name_tag = driver.find_elements_by_xpath("//div[@class='personName']/div")
    for name in name_tag:
        Person_Name.append(name.text)
    time.sleep(1)
    
    
    # scraping the data of age of the billionaires
    age_tag = driver.find_elements_by_xpath("//div[@class='age']/div")
    for age in age_tag:
        Age.append(age.text)
    time.sleep(1)
    
    
    # scraping the data of citizenship of the billionaires
    cit_tag = driver.find_elements_by_xpath("//div[@class='countryOfCitizenship']")
    for cit in cit_tag:
        Citizenship.append(cit.text)
    time.sleep(1)
    
    
    # scraping the data of source of income of the billionaires
    sour_tag = driver.find_elements_by_xpath("//div[@class='source']")
    for sour in sour_tag:
        Source.append(sour.text)
    time.sleep(1)
    
    
    # scraping data of industry of the billionaires
    ind_tag = driver.find_elements_by_xpath("//div[@class='category']//div")
    for ind in ind_tag:
        Industry.append(ind.text)
    time.sleep(1)
    
    
    # scraping data of net_worth of billionaires
    net_tag = driver.find_elements_by_xpath("//div[@class='netWorth']/div")
    for net in net_tag:
        Net_worth.append(net.text)
    time.sleep(1)
    
    
    # clicking on next button
    try:
        next_button = driver.find_element_by_xpath("//button[@class='pagination-btn pagination-btn--next ']")
        next_button.click()
    except:
        break
      


# In[6]:


print(len(Rank),
len(Person_Name),
len(Net_worth),
len(Age),
len(Citizenship),
len(Source),
len(Industry))


# In[7]:


# framing Data
Billionaires = pd.DataFrame({})
Billionaires['Rank'] = Rank
Billionaires['Name'] = Person_Name
Billionaires['Net Worth'] = Net_worth
Billionaires['Age'] = Age
Billionaires['Citizenship'] = Citizenship
Billionaires['Source'] = Source
Billionaires['Industry'] = Industry
Billionaires


# In[9]:


# saving dataset in csv
Billionaires.to_csv('Forbes_Billionaires.csv')


# In[10]:


driver.close()


# In[ ]:





# # Q9 : Write a program to extract at least 500 Comments, Comment upvote and time when comment was posted from any YouTube Video.

# In[11]:


# connecting to the webdriver
driver=webdriver.Chrome(r"C:/Users/HP/Downloads/chromedriver_win32 (1)/chromedriver.exe")


# In[12]:


# opening the youtube.com
url = "https://www.youtube.com/"
driver.get(url)
time.sleep(2)


# In[16]:


# finding element for search bar
search_bar = driver.find_element_by_xpath("//div[@class='ytd-searchbox-spt']/input")
search_bar.send_keys("GOT")      # entering video name
time.sleep(2)


# In[17]:


#clicking on search button
search_btn = driver.find_element_by_id("search-icon-legacy")
search_btn.click()
time.sleep(2)


# In[18]:


# clicking on first video
video = driver.find_element_by_xpath("//yt-formatted-string[@class='style-scope ytd-video-renderer']")
video.click()


# In[19]:


# 1000 times we scroll down by 10000 in order to generate more comments
for _ in range(1000):
    driver.execute_script("window.scrollBy(0,10000)")


# In[22]:


# creating empty lists
comments = []
comment_time = []
Time = []
Likes = []
No_of_Likes = []

# scrape comments
cm = driver.find_elements_by_id("content-text")
for i in cm:
    if i.text is None:
        comments.append("--")
    else:
        comments.append(i.text)
time.sleep(4)


# scrape time when comment was posted
tm = driver.find_elements_by_xpath("//a[contains(text(),'ago')]")
for i in tm:
    Time.append(i.text)
    
for i in range(0,len(Time),2):
    comment_time.append(Time[i])
time.sleep(4)


# scrape the comment likes
like = driver.find_elements_by_xpath("//span[@class='style-scope ytd-comment-action-buttons-renderer']")
for i in like:
    Likes.append(i.text)
    
for i in range(1,len(Likes),2):
    No_of_Likes.append(Likes[i])


# In[23]:


print(len(comments),len(comment_time),len(No_of_Likes))


# In[24]:


# creating dataframe for scraped data

Youtube = pd.DataFrame({})
Youtube['Comment'] = comments[:500]
Youtube['Comment Time'] = comment_time[:500]
Youtube['Comment Upvotes'] = No_of_Likes[:500]
Youtube


# In[25]:


#saving the dataframe to csv
Youtube.to_csv("Youtube GOT Comments.csv")


# In[26]:


driver.close()


# In[ ]:





# # Q10 : Write a python program to scrape a data for all available Hostels from https://www.hostelworld.com/ in “London” location. You have to scrape hostel name, distance from city centre, ratings, total reviews, overall reviews, privates from price, dorms from price, facilities and property description.

# In[8]:


# connecting to the webdriver
driver=webdriver.Chrome(r"C:/Users/HP/Downloads/chromedriver_win32 (1)/chromedriver.exe")


# In[9]:


# getting the web page of mentioned url
url = "https://www.hostelworld.com/"
driver.get(url)
time.sleep(3)


# In[10]:


# locating the location search bar
search_bar = driver.find_element_by_id("search-input-field")

# entering London in search bar
search_bar.send_keys("London")


# In[11]:


# select London
London = driver.find_element_by_xpath("//ul[@id='predicted-search-results']//li[2]")
#clicking on button
London.click()

# do click on Let's Go button
search_btn = driver.find_element_by_id('search-button')
search_btn.click()


# In[12]:


# creating empty list & find required data
hostel_name = []
distance = []
pvt_prices = []
dorms_price = []
rating = []
reviews = []
over_all = []
facilities = []
description = []
url = []


# In[13]:


# scraping the required informations
for i in driver.find_elements_by_xpath("//div[@class='pagination-item pagination-current' or @class='pagination-item']"):
    i.click()
    time.sleep(3)
    
    
    # scraping  hostel name
    try:
        name = driver.find_elements_by_xpath("//h2[@class='title title-6']")
        for i in name:
            hostel_name.append(i.text)
    except NoSuchElementException:
        hostel_name.append('-')
        
        
    # scraping distance from city centre
    try:
        dist = driver.find_elements_by_xpath("//div[@class='subtitle body-3']//a//span[1]")
        for i in name:
            distance.append(i.text.replace('Hostel - ',''))
    except NoSuchElementException:
        distance.append('-')
        
   
    for i in driver.find_elements_by_xpath("//div[@class='prices-col']"):   
    # scraping privates from price
        try:
            pvt_price = driver.find_element_by_xpath("//a[@class='prices']//div[1]//div")
            pvt_prices.append(pvt_price.text)
        except NoSuchElementException:
            pvt_prices.append('-')
   

    for i in driver.find_elements_by_xpath("//div[@class='prices-col']"):          
    # scraping dorms from price
        try:
            dorms = driver.find_element_by_xpath("//a[@class='prices']//div[2]/div")
            dorms_price.append(dorms.text)
        except NoSuchElementException:
            dorms_price.append('-')
            
            
    # scraping facilities
    try:
        fac1 = driver.find_elements_by_xpath("//div[@class='has-wifi']")
        fac2 = driver.find_elements_by_xpath("//div[@class='has-sanitation']")
        for i in fac1:
            for j in fac2:
                facilities.append(i.text +', '+ j.text)
    except NoSuchElementException:
        facilities.append('-')
     
            
    #fetching url of each hostel
    p_url = driver.find_elements_by_xpath("//div[@class='prices-col']//a[2]")
    for i in p_url:
        url.append(i.get_attribute("href"))
        
for i in url:
    driver.get(i)
    time.sleep(3)
    

    # scraping ratings
    try:
        rat = driver.find_element_by_xpath("//div[@class='score orange big' or @class='score gray big']")
        rating.append(rat.text)
    except NoSuchElementException:
        rating.append('-')
        
        
    # scraping total review
    try:
        rws = driver.find_element_by_xpath("//div[@class='reviews']")
        reviews.append(rws.text.replace('Total Reviews',''))
    except NoSuchElementException:
        reviews.append('-')
        
        
    # fetching over all review
    try:
        overall = driver.find_element_by_xpath("//div[@class='keyword']//span")
        over_all.append(overall.text)
    except NoSuchElementException:
        over_all.append('-')
        
        
    # fetching property description
    try:
        disc = driver.find_element_by_xpath("//div[@class='content']")
        description.append(disc.text)
    except NoSuchElementException:
        over_all.append('-')
    
    # do click on show more button for description
    try:
        driver.find_element_by_xpath("//a[@class='toggle-content']").click()
        time.sleep(4)
    except NoSuchElementException:
        pass
    
               


# In[14]:


print(len(hostel_name),
len(distance),
len(pvt_prices),
len(dorms_price),
len(rating),
len(reviews),
len(over_all),
len(facilities),
len(description),
len(url))


# In[15]:


# creating DataFrame
Hostel = pd.DataFrame({})
Hostel['Hostel Name'] = hostel_name
Hostel['Distance from City Centre'] = distance
Hostel['Ratings'] = rating
Hostel['Total Reviews'] = reviews
Hostel['Overall Reviews'] = over_all
Hostel['Privates from Price'] = pvt_prices
Hostel['Dorms from Price'] = dorms_price
Hostel['Facilities'] = facilities[:74]
Hostel['Description'] = description
Hostel


# In[16]:


# saving the dataset to csv
Hostel.to_csv("London_Hostels.csv")


# In[17]:


driver.close()


# In[ ]:





# In[ ]:





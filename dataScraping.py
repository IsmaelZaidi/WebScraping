import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import geocoder

# The lists that eventually will be used for the dataframe
bedrooms = []
baths = []
sqft = []
addresses = []
housePrices = []

#Random time before opening page so that website wont think that I'm a bot (without this random time site will recognize as bot).
def pickingRandomTime():
    return random.randint(45,90)

#Function that will get all the houses of the specified url
def getHousesOfPage(pageNumber):
        # setting up the webdriver and url
        page_url = "https://www.realtor.com/realestateandhomes-search/Los-Angeles_CA/pg-" + str(pageNumber)
        s = Service('C:/Users/Ismael/Documents/chromedriver/chromedriver.exe')
        driver = webdriver.Chrome(service=s)
        driver.implicitly_wait(pickingRandomTime())
        driver.get(page_url)
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        # Searching for specific elemetns in the html
        for object in soup.findAll('li', attrs={'class': 'component_property-card'}):

                for object in soup.findAll('li', attrs={'class': 'component_property-card'}):
                    bedroom = object.find('li', attrs={'data-label': 'pc-meta-beds'})
                    bath = object.find('li', attrs={'data-label': 'pc-meta-baths'})
                    size = object.find('li', attrs={'data-label': 'pc-meta-sqft'})
                    address = object.find('div', attrs={'data-label': 'pc-address'})
                    price = object.find('span', attrs={'data-label': 'pc-price'})

                    if bedroom and bath:
                        nr_beds = bedroom.find('span', attrs={'data-label': 'meta-value'})
                        nr_baths = bath.find('span', attrs={'data-label': 'meta-value'})

                        #Converting the object to a string so that we won't have to deal with NoneTypes
                        if nr_beds is None:
                            nr_beds = "0"
                        else:
                            nr_beds = nr_beds.text
                        #Same applies as above
                        if nr_baths is None:
                            nr_beds = "0"
                        else:
                            nr_baths = nr_baths.text

                        #apparently you can have .5+ amount of beds or baths, therefor we need to remove the plus sign so we can convert it to a float
                        if("+" in nr_beds):
                            nr_beds = nr_beds[:-1]
                        #same applies here as above
                        if("+" in nr_baths):
                            nr_baths = nr_baths[:-1]

                        if nr_beds and float(nr_beds) >= 1 and nr_baths and float(nr_baths) >= 1:
                            bedrooms.append(nr_beds)
                            baths.append(nr_baths)

                            if address and address.text:
                                addresses.append(address.text)
                            else:
                                addresses.append('The address cannot be shown')

                            if size and size.text:
                                sqft.append(size.text)
                            else:
                                sqft.append('The squareFeet cannot be shown')

                            if price and price.text:
                                housePrices.append(price.text)
                            else:
                                housePrices.append('The price cannot be shown')


        #Create the csv file containing all the houses on all the pages
        dataFrame = pd.DataFrame({'Address': addresses, 'Price': housePrices, 'Beds': bedrooms, 'Baths': baths, 'Sizes': sqft})
        #Some houses are duplicates so therefor we need to remove the duplicates
        uniqueData = dataFrame.drop_duplicates()
        uniqueData.to_csv('listings.csv', mode='a', index=False, encoding='utf-8')

        driver.close()

# Function where you can specify on how many pages you want the getHouseOfPage function to run
def getAllHouses():
    for i in range(1,190,1):
        getHousesOfPage(i)

#Calling the function
getAllHouses()
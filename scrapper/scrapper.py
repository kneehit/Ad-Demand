#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 10:54:08 2018

@author: kneehit
"""
#%%
import wikipedia as wiki
from bs4 import BeautifulSoup as soup
import wikipedia as wiki
from bs4 import BeautifulSoup as soup
import numpy as np
import pandas as pd
import os
#%%
#wiki.set_lang('ru')   # else gives incorrect results Eg. for 'Самара' gave 'PFC Krylia Sovetov Samara' not city but FC
#a = wiki.page('Самара')
#a_html = a.html()

#%%
#a_soup = soup(a_html,'html.parser')
#a_pop =  a_soup.find_all(id = 'Население')[0]
##%%
## For table 
#tab = a_pop.findNext(class_ = 'standard')
## For Year
#year_row = tab.find_all(class_ = 'bright')[-1]
#year = year_row.find_all('th')[-2].text
## For population count
#pop_row = tab.find_all(align = 'center')[-1]
#pop = pop_row.find_all('td')[-2].text
#
## \xa0 is non-breaking space in Latin1 encoding
#pop_clean = pop.replace(u'\xa0',u'') 

#%%
train = pd.read_csv('train.csv')
city_counts = train['city'].value_counts() 
unique_cities = list(city_counts.index) # list of unique cities in the training data

#%%
wiki.set_lang('ru')   # else gives incorrect results Eg. for 'Самара' gave 'PFC Krylia Sovetov Samara' not city but football club

#%%
city_pop = pd.DataFrame(columns = ['city','popu_string'])
#%%
for ind in range(len(unique_cities)):
#ind = 178
    city_name = unique_cities[ind]
    try:

        page = wiki.page(city_name )  
    # If city name is ambiguous
    except wiki.DisambiguationError:
        print('Disambiguation Error: Trying {} along with term city'.format(city_name))

        try:

            page = wiki.page(city_name + ' город')  # city name + city
        # If still not found then add NANs for population string and continue
        # NAN as string and not np.NaN for data type consistency in population column
        except (wiki.DisambiguationError, wiki.PageError):     
            print('Error: Page for city {} Not Found !!!'.format(city_name))
            temp = pd.DataFrame(data = {'city':[city_name],'popu_string':['NAN']})

            city_pop = pd.concat((city_pop,temp),ignore_index = True)  
            continue
    except wiki.PageError:
        temp = pd.DataFrame(data = {'city':[city_name],'popu_string':['NAN']}) 
        
        
        city_pop = pd.concat((city_pop,temp),ignore_index = True)  
        continue
    
    print(str(ind)  + '  ' + unique_cities[ind])
    page_html = page.html()
    
    
    city_soup = soup(page_html,'html.parser')
    
    
    try:
        # Find information box (usually situated at the top left side on wikipedia page)
        infobox = city_soup.find_all(class_ = 'infobox vcard')[0]
        
        # Find the HTML element with text population (in Russian)
        pop = infobox.find_next(text = 'Население')
        
        # Find the string actually containing population figure
        popu = pop.find_next('tr').find_next('span').text
        
        temp = pd.DataFrame(data = {'city':[city_name],'popu_string':[popu]})
        
        # Concatenate temporary and main population data
        city_pop = pd.concat((city_pop,temp),ignore_index = True)
    except:
        temp = pd.DataFrame(data = {'city':[city_name],'popu_string':['NAN']}) # not np.NaN for data type consistency
        
        
        city_pop = pd.concat((city_pop,temp),ignore_index = True)
#%%
city_pop.to_csv('Population Dirty.csv')
#%%
# Example of values in population column - '↗1 468 833[2] человека (2018)'
# Split the string by '[' so that 
city_pop['popu_string'] = city_pop['popu_string'].str.split('[').str[0]
# Our values now look like '↗1 468 833'

# The space in the string is actually \xa0 which is non-breaking space in Latin1 encoding
# Some values also have the space character ' ' as well.
# Therefore we replace both of them by ''
city_pop['popu_string'] = city_pop['popu_string'].str.replace('\xa0','').str.replace(' ','')
# Now most of the values look like this '↗1468833'

# We could simpy drop the first character (arrow) but since few values in our data are different from that. Example - '707408чел.(1января2018)'
# To extract the population count we will use the regex for digits - '\d'
city_pop['popu_string'] = city_pop['popu_string'].str.extract('(\d+)')
# Finally we are left with only population count - 1468833

# Convert the string column to numeric 
city_pop['popu_string'] = pd.to_numeric(city_pop['popu_string'])

# Write csv
city_pop.to_csv('Population Clean.csv')


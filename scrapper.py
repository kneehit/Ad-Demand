#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 10:54:08 2018

@author: kneehit
"""
#%%
import wikipedia as wiki
from bs4 import BeautifulSoup as soup
#%%
wiki.set_lang('ru')   # else gives incorrect results Eg. for 'Самара' gave 'PFC Krylia Sovetov Samara' not city but FC
a = wiki.page('Самара')
a_html = a.html()

#%%
a_soup = soup(a_html,'html.parser')
a_pop =  a_soup.find_all(id = 'Население')[0]
#%%
tab = a_pop.findNext(class_ = 'standard')

year_row = tab.find_all(class_ = 'bright')[-1]
year = year_row.find_all('th')[-2].text

pop_row = tab.find_all(align = 'center')[-1]
pop = pop_row.find_all('td')[-2].text
pop_clean = pop.replace(u'\xa0',u'')
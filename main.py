#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 12:39:59 2018

@author: kneehit
"""

#%%
# Load Libraries
import numpy as np
import pandas as pd
import cv2
import os
import googletrans
import glob
import random
import matplotlib.pyplot as plt 
import pprint
import string
from collections import Counter
#%%
# Load all CSVs
periods_train = pd.read_csv('periods_train.csv',nrows = 10)
periods_test = pd.read_csv('periods_test.csv',nrows = 10)

train = pd.read_csv('train.csv',nrows = 100)
test = pd.read_csv('test.csv',nrows = 100)


train_active = pd.read_csv('train_active.csv',nrows = 100)
test_active = pd.read_csv('test_active.csv',nrows = 100)


train_images_path = 'train/data/competition_files/train_jpg/'
test_images_path = 'test/data/competition_files/test_jpg/'

train_images = glob.glob(train_images_path +'*.jpg')
test_images = glob.glob(test_images_path +'*.jpg')

#%%
# Function to visualize ad image and the related information
translator = googletrans.Translator()
def visualize_translated(num):

    item_translated = {}
    # Translate relevant columns from Russian to English
    item_translated['region'] = translator.translate(train.iloc[num,2]).text
    item_translated['city'] = translator.translate(train.iloc[num,3]).text
    item_translated['parent_cat'] = translator.translate(train.iloc[num,4]).text
    item_translated['category'] = translator.translate(train.iloc[num,5]).text
    item_translated['param_1'] = translator.translate(train.iloc[num,6]).text if not pd.isna(train.iloc[num,6]) else 'NA'
    item_translated['param_2'] = translator.translate(train.iloc[num,7]).text if not pd.isna(train.iloc[num,7]) else 'NA'
    item_translated['param_3'] = translator.translate(train.iloc[num,8]).text if not pd.isna(train.iloc[num,8]) else 'NA'
    item_translated['title']= translator.translate(train.iloc[num,9]).text
    item_translated['desc'] = translator.translate(train.iloc[num,10]).text if not pd.isna(train.iloc[num,10]) else 'NA'
    
    # pprint so that it is formatted appropriately in the output
    pprint.pprint(item_translated)
    
    # Display Image
    if not pd.isna(train.iloc[num,15]):
        image_path = train_images_path + train.iloc[num,15] + '.jpg'
        img = cv2.imread(image_path)
        cv2.imshow('Item {}'.format(num),img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print('\nImage Missing')

# Display 4 images and their translated information       
for i in range(0,4):
    num = random.randint(0,train.shape[0])
    visualize_translated(num)
#%%
city_counts = train['city'].value_counts() 
unique_cities = list(city_counts.index)

cities_translated = {}

for i in range(len(unique_cities)):
    translated_city = translator.translate(unique_cities[i]).text
    cities_translated.update({unique_cities[i]:translated_city})

# Parent category plots
    
plt.hist(train.iloc[:,17], np.arange(0.0,1.1,0.1),edgecolor = 'black',linewidth = 1.2)
plt.xticks(np.arange(0.0,1.1,0.1))

cats_and_counts = train['parent_category_name'].value_counts()

translated_cats = []
for i in list(cats_and_counts.index):
    translated_cats.append(translator.translate(i).text)



cats_and_counts.plot('bar').set_xticklabels(translated_cats)
#%%
for j in range(len(cats_and_counts)):
#    plt.subplot(2,1,j+1)
    subset = train[train['parent_category_name'] == list(cats_and_counts.index)[j]]
    
    subset_cats = subset['category_name'].value_counts()
    
    translated_subcats = []
    for i in list(subset_cats.index):
        translated_subcats.append(translator.translate(i).text)
        
    subset_cats.plot('bar').set_xticklabels(translated_subcats)
    plt.title('Parent Category: ' + translated_cats[j],fontsize = 20)
    plt.show()
 
#%%
# Read the city population scrapped from wikipedia 
pop = pd.read_csv('Population Clean.csv')
pop.columns = ['city','popu_count']
# Replace nan by average population count
pop = pop.fillna(np.round(np.mean(pop['popu_count'])))
# insert population column which is based on city names from train and pop dataset
train['population'] = train['city'].map(pop.set_index('city')['popu_count'])
test['population'] = test['city'].map(pop.set_index('city')['popu_count'])

#%%
# Percent of missing values in columns 
train.isna().sum()*100/train.shape[0]
# Param_2 and Param_3 have 43% and 57% missing values respectively.
#%%
# Replace nans by with empty string
train.loc[:,['param_1','param_2','param_3']] = train.loc[:,['param_1','param_2','param_3']].fillna('')
train.loc[:,'description'] = train.loc[:,'description'].fillna('')

# Replace nans in price column by average price of the corresponding category
train['price'] = train.loc[:,['category_name','price']].groupby('category_name').transform(lambda x: x.fillna(x.mean()))

#%%
# Combine params since param_2 and param_3 have about 50% empty strings
train['param'] = train['param_1'] + ' ' + train['param_2'] + ' ' + train['param_3']
# Remove white spaces from start and end
train['param'] = train['param'].str.strip()
# Replace double white spaces by single white space. 
train['param'] = train['param'].str.replace('  ',' ')
#%%
train['description'][random.randint(0,train.shape[0])]
# After going through many (200+) descriptions, following characters appear in the dataset 
# These should be removed/treated separately.
chars_to_replace = ['/\n','№','Б/у','\n','☎','✔','✘','☛','☚','•','«','»']
# List of punctuation marks
chars_to_replace.extend(list(string.punctuation))
# List of commonly occuring fractions
chars_to_replace.extend(['¹', '²', '³', '½', '⅓', '¼', '⅕', '⅙', '⅐', '⅛', '⅑', '⅒', '⅔', '⅖', '¾', '⅗', '⅜', '⅘', '⅚', '⅝', '⅞'])
# Numbers can occur in various forms in the item description.
chars_to_replace.extend(['⓵','⓶','⓷','⓸','⓹','⓺','⓻','⓼','⓽','⓾'])
chars_to_replace.extend(['⒈','⒉', '⒊', '⒋', '⒌', '⒍', '⒎', '⒏', '⒐','⒑'])
chars_to_replace.extend(['Ⓞ','①','②','③','④','⑤','⑥','⑦','⑧','⑨','⑩'])
chars_to_replace.extend(['⓪', '➀', '➁', '➂', '➃', '➄', '➅', '➆', '➇', '➈', '➉'])
chars_to_replace.extend(['⓿', '❶', '❷', '❸', '❹', '❺', '❻', '❼', '❽', '❾', '❿'])



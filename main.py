#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 12:39:59 2018

@author: kneehit
"""

#%%
import numpy as np
import pandas as pd
import cv2
import os
import googletrans
import glob
import random
import matplotlib.pyplot as plt 

#%%
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
def visualize_translated(num = random.randint(0,train.shape[0])):

    item_translated = {}
    item_translated['region'] = translator.translate(train.iloc[num,2]).text
    item_translated['city'] = translator.translate(train.iloc[num,3]).text
    item_translated['parent_cat'] = translator.translate(train.iloc[num,4]).text
    item_translated['category'] = translator.translate(train.iloc[num,5]).text
    item_translated['param_1'] = translator.translate(train.iloc[num,6]).text if not pd.isna(train.iloc[num,6]) else 'NA'
    item_translated['param_2'] = translator.translate(train.iloc[num,7]).text if not pd.isna(train.iloc[num,7]) else 'NA'
    item_translated['param_3'] = translator.translate(train.iloc[num,8]).text if not pd.isna(train.iloc[num,8]) else 'NA'
    item_translated['title']= translator.translate(train.iloc[num,9]).text
    item_translated['desc'] = translator.translate(train.iloc[num,10]).text
    print(item_translated)
    
    
    if not pd.isna(train.iloc[num,15]):
        image_path = train_images_path + train.iloc[num,15] + '.jpg'
        a = cv2.imread(image_path)
        cv2.imshow('',a)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print('\nImage Missing')

visualize_translated(21)
#%%
city_counts = train['city'].value_counts() 
unique_cities = list(city_counts.index)

cities_translated = {}

for i in range(len(unique_cities)):
    translated_city = translator.translate(unique_cities[i]).text
    cities_translated.update({unique_cities[i]:translated_city})

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
pop = pd.read_csv('Population Clean.csv')
pop.columns = ['city','popu_count']
# Replace nan by average population count
pop = pop.fillna(np.round(np.mean(pop['popu_count'])))
# insert population column which is based on city names from train and pop dataset
train['population'] = train['city'].map(pop.set_index('city')['popu_count'])

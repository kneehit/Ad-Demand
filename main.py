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
os.chdir('/home/kneehit/Data Science/Avito Ad Demand/Avito')
import random


#%%
periods_train = pd.read_csv('periods_train.csv',nrows = 10)
periods_test = pd.read_csv('periods_test.csv',nrows = 10)
#%%
train = pd.read_csv('train.csv',nrows = 100)
test = pd.read_csv('test.csv',nrows = 100)

#%%
train_active = pd.read_csv('train_active.csv',nrows = 100)
test_active = pd.read_csv('test_active.csv',nrows = 100)

#%%
train_images_path = 'train/data/competition_files/train_jpg/'
test_images_path = 'test/data/competition_files/test_jpg/'

train_images = glob.glob(train_images_path +'*.jpg')
test_images = glob.glob(test_images_path +'*.jpg')

#%%

def visualize_translated(num = random.randint(0,train.shape[0])):
    translator = googletrans.Translator()
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




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
translator = googletrans.Translator()
a = translator.translate('안녕하세요.')
#%%
train_images_path = 'train/data/competition_files/train_jpg/'
test_images_path = 'test/data/competition_files/test_jpg/'

train_images = glob.glob(train_images_path +'*.jpg')
test_images = glob.glob(test_images_path +'*.jpg')

#%%

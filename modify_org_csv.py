import numpy as np
import pandas as pd 
import os
import sys
import random
import glob
import math
import json
from tqdm import tqdm
import argparse
import yaml
import librosa
import itertools

from utils import \
    FSD50K, ESC50, sv_csv_dir

os.makedirs(sv_csv_dir, exist_ok=True)
os.makedirs(sv_csv_dir+'bg/', exist_ok=True)
os.makedirs(sv_csv_dir+'ev/', exist_ok=True)


## make bg csv
bg_lbls = ['rain', 'car_passing']
splits = ['dev','eval']

def add_ext(fn):
    return str(fn)+'.wav'

# 全部結合
dfs =[]
for lbl, split in itertools.product(bg_lbls, splits):
    try:
        df = pd.read_csv(f'org_audio_csv/background/fsd50k/{lbl}/{split}.csv')
        df['split'] = split
        dfs.append(df)
    except:
        print(f'No such csv file of condition: {lbl}_{split}')

df = pd.concat(dfs).reset_index(drop=True)
df['fname'] = df['fname'].apply(add_ext)

# サンプル数を測る
lens = []
for row in df.itertuples():
    fn = FSD50K+f'/FSD50K.{row.split}_audio/{row.fname}'
    s, fs = librosa.load(fn, sr=None)
    lens.append(len(s))
df['length'] = lens
df.to_csv(sv_csv_dir+'bg/fsd50k.csv')


## make ev csv
ev_lbls = [
    'thunder', 'dog', 'footsteps', 
    'chirping_birds', 'car_horn', 'church_bell',
    ]

def normalize_amp(data):
    return data/np.abs(data).max()

def detect_nonactive_section(data, th=0.1):
    filtered_amp=normalize_amp(np.convolve(np.abs(data), np.hanning(512), mode='same'))
    active = filtered_amp>np.max(filtered_amp)*th
    active_point = np.where(active == 1)[0]
    return active_point[0], active_point[-1]

# noisy 消して全結合
dfs = []
for lbl in ev_lbls:
    df = pd.read_csv(f'org_audio_csv/event/esc50/{lbl}.csv')
    df = df[df['clean']==True].drop(columns=['clean', 'noise desc'])
    dfs.append(df)
df = pd.concat(dfs).reset_index(drop=True)

sts = []
eds = []
split = []
for row in tqdm(df.itertuples()):
    fn = ESC50+f'/{row.fname}'
    s, fs = librosa.load(fn, sr=None)
    st, ed = detect_nonactive_section(s, th=0.1)
    if row.fname[0] == '5':
        sp = 'eval'
    else:
        sp = 'dev'
    sts.append(st)
    eds.append(ed)
    split.append(sp)
df['split'] = split
df['st'] = sts
df['ed'] = eds
df.to_csv(sv_csv_dir+'ev/esc50.csv')
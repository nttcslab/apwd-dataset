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
import shutil
import itertools

import scipy
from scipy.io import wavfile
import librosa

from utils import \
    FSD50K, ESC50, \
    org_audio_csv_dir, sv_csv_dir


DURATION = 10
FADE_LEN = 0.01

try:
    shutil.rmtree('source/')
except: 0

def wavwrite(fn, data, fs):
    data = np.array(np.around(data * 2**(15)), dtype = "int16")
    wavfile.write(fn, fs, data)    

def normalize_amp95(data):
    return data/np.abs(data).max() * 0.95


df = pd.read_csv('audio_csv/bg/fsd50k.csv')
for row in tqdm(df.itertuples()):
    fn = FSD50K+f'/FSD50K.{row.split}_audio/{row.fname}'
    audio, fs = librosa.load(fn, sr=None)
    rep = (DURATION*2*fs)//row.length+1
    rep_audio = np.tile(audio, rep)
    rep_audio = normalize_amp95(rep_audio)
    save_dir = f'source/{row.split}/background/{row.label}/'
    os.makedirs(save_dir, exist_ok=True)

    wavwrite(save_dir+row.fname, rep_audio, fs)

df = pd.read_csv('audio_csv/ev/esc50.csv')
for row in tqdm(df.itertuples()):
    fn = ESC50+f'/{row.fname}'
    audio, fs = librosa.load(fn, sr=None)
    fade_sample = int(FADE_LEN*fs)
    win_fadein, win_fadeout = np.split(np.hanning(fs*FADE_LEN*2), 2)
    audio = audio[row.st:row.ed]
    audio[:fade_sample] *= win_fadein
    audio[-fade_sample:] *= win_fadeout
    save_dir = f'source/{row.split}/foreground/{row.label}/'
    os.makedirs(save_dir, exist_ok=True)
    wavwrite(save_dir+row.fname, audio, fs)

## 背景音をイベント化

split_scene = itertools.product(
    ['dev', 'eval'],
    ['rain', 'car_passing']
    )

for split, label in split_scene:
    # import pdb; pdb.set_trace()
    try:
        shutil.copytree(
            f'source/{split}/background/{label}',
            f'source/{split}/foreground/{label}',
            dirs_exist_ok=True
        )
    except:
        print(f'No such file or directory: {label}_{split}')
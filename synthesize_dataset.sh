#!/bin/bash
python modify_org_csv.py
python preprocess_org_audio.py

python synthesize_audio.py -d datasets/apwd_rain_sc/dev
python synthesize_audio.py -d datasets/apwd_traffic_sc/dev

python synthesize_audio.py -d datasets/apwd_rain_sc/eval
python synthesize_audio.py -d datasets/apwd_traffic_sc/eval
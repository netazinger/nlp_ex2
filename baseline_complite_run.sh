#!/usr/bin/env bash
python train.py baseline data_training_files/heb-pos.train y
#python decode.py baseline data_files/heb-pos.test heb-pos.baseline
#python evaluate.py heb-pos.tagged data_files/heb-pos.gold baseline y
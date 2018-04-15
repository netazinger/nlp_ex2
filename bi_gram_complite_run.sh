#!/usr/bin/env bash
python train.py bi-gram data_training_files/heb-pos.train n
python decode.py bi-gram data_files/heb-pos.test heb-pos.gram heb-pos.lex
python evaluate.py heb-pos.tagged data_files/heb-pos.gold bi-gram n

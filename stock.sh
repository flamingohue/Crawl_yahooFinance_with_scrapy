#!/bin/sh
cd /home/flamingo/Documents/web_scraping/stockproject
conda deactivate
conda activate scrapyenv

scrapy crawl activestock -o flow.csv
python stock_info_organize.py
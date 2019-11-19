import gzip
import json
import re
import csv
import sqlite3
from datetime import datetime

html_pattern = re.compile('<.*?>')
connection = sqlite3.connect('interview_project.db')

def create_new_listings_table():
    c = connection.cursor()
    c.execute('''DROP TABLE IF EXISTS listings''')
    c.execute('''CREATE TABLE listings
                (body text, title text, expired date, posted date, state text, city text, onet text, soc5 text, soc2 text)''')
    connection.commit()

def remove_html_tags(text):
    clean_text = re.sub(html_pattern, '', text)
    return clean_text

def to_datetime(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d')

def insert_listing(body, title, expired, posted, state, city, onet, soc5, soc2):
    c = connection.cursor()
    c.execute('INSERT INTO listings VALUES (?,?,?,?,?,?,?,?,?)', [
        buffer(body), title, 
        expired.isoformat(), 
        posted.isoformat(), 
        state, city, 
        onet, soc5, soc2])
    connection.commit()

def process_line(line, map_onet_soc, soc_hierarchy):
    listing_json = json.loads(line)
    body = listing_json['body'].encode('utf8')
    clean_body = remove_html_tags(body)
    expired = to_datetime(listing_json['expired'])
    posted = to_datetime(listing_json['posted'])
    insert_listing(
        body = clean_body,
        title = listing_json['title'],
        expired = expired,
        posted = posted,
        state = listing_json['state'],
        city = listing_json['city'],
        onet = listing_json['onet'],
        soc5 = 'soc5',
        soc2 = 'soc2',
        )

def process_file(file_location):
    sample_f = gzip.open(file_location, 'r')
    map_onet_soc_f = open('data/map_onet_soc.csv', 'r')
    soc_hierarchy_f = open('data/soc_hierarchy.csv', 'r')

    try:
        map_onet_soc = csv.DictReader(map_onet_soc_f)
        soc_hierarchy = csv.DictReader(soc_hierarchy_f)

        process_line(sample_f.readline(), map_onet_soc, soc_hierarchy)
        # for line in sample_f:
        #     process_line(line)
    finally:
        sample_f.close()
        map_onet_soc_f.close()
        soc_hierarchy_f.close()
        
try:
    create_new_listings_table()
    process_file('data/sample.gz')
finally:
    connection.close()
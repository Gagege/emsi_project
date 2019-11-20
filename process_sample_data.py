import gzip
import json
import re
import csv
import sqlite3
from datetime import datetime

# There are some broken html tags and javascript in the sample.
# I did some research and decided it wouldn't be the best use of my time to try to remove every bit of broken html and code.
# So I'm simply removing all the actual html tags.
html_pattern = re.compile('<.*?>')
html_removed_count = 0
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
    # I would usually put a try/except here but the dates in the sample data are all nice a clean
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
    try:
        listing_json = json.loads(line)
        body = listing_json['body'].encode('utf8')
        clean_body = remove_html_tags(body)
        if body != clean_body:
            global html_removed_count
            html_removed_count += 1
        expired = to_datetime(listing_json['expired'])
        posted = to_datetime(listing_json['posted'])
        soc5 = map_onet_soc[listing_json['onet']]
        
        # some soc5 codes are not in the soc_hierarchy file
        try:
            soc2 = soc_hierarchy[soc5]
        except KeyError:
            soc2 = None

        insert_listing(
            body = clean_body,
            title = listing_json['title'],
            expired = expired,
            posted = posted,
            state = listing_json['state'],
            city = listing_json['city'],
            onet = listing_json['onet'],
            soc5 = soc5,
            soc2 = soc2,
            )
    except KeyError:
        print('Unable to parse this listing:')
        print(listing_json)

def map_onet_soc_csv_to_dict(file_location):
    with open(file_location, 'r') as f:
        mapping = {}
        for row in csv.DictReader(f):
            mapping[row['onet']] = row['soc5']
        return mapping

def soc_hierarchy_to_dict(file_location):
    with open(file_location, 'r') as f:
        mapping = {}
        for row in csv.DictReader(f):
            mapping[row['child']] = row['parent']
        return mapping

def process_file(file_location):
    with gzip.open(file_location, 'r') as sample_f:
        map_onet_soc = map_onet_soc_csv_to_dict('data/map_onet_soc.csv')
        soc_hierarchy = soc_hierarchy_to_dict('data/soc_hierarchy.csv')
        for line in sample_f:
            process_line(line, map_onet_soc, soc_hierarchy)
        
try:
    create_new_listings_table()
    process_file('data/sample.gz')
    print('Removed html tags from this many listings:', html_removed_count)
finally:
    connection.close()
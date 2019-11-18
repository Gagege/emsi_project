import gzip
import json
import re
import sqlite3

html_pattern = re.compile('<.*?>')
connection = sqlite3.connect('interview_project.db')

def create_new_listings_table():
    c = connection.cursor()
    c.execute('''DROP TABLE IF EXISTS listings''')
    c.execute('''CREATE TABLE listings
                (body text, title text, expired text, posted text, state text, city text, onet text, soc5 text, soc2 text)''')
    connection.commit()

def remove_html_tags(text):
    clean_text = re.sub(html_pattern, '', text)
    return clean_text

def insert_listing(body, title):
    c = connection.cursor()
    c.execute('INSERT INTO listings VALUES (?,?,?,?,?,?,?,?,?)', [
        buffer(body),
        buffer(title),
        'expired',
        'posted',
        'state',
        'city', 
        'onet', 'soc5', 'soc2'])
    connection.commit()

def process_line(line):
    listing_json = json.loads(line)
    body = listing_json['body'].encode('utf8')
    clean_body = remove_html_tags(body)
    insert_listing(
        body = clean_body,
        title = listing_json['title']
        )

def process_file(file_location):
    with gzip.open(file_location, 'r') as fileIn:
        for line in fileIn:
            process_line(line)

create_new_listings_table()
process_file('data/sample.gz')
connection.close()
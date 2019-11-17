import gzip
import json
import re

html_pattern = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

def remove_html_tags(text):
    clean_text = re.sub(html_pattern, '', text)
    return clean_text

with gzip.open('data/sample.gz', 'r') as fileIn:
    num = 0
    for line in fileIn:
        listing = json.loads(line)
        body = listing['body'].encode('utf8')
        clean_body = remove_html_tags(body)
        print(clean_body)
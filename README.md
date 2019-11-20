# Gage Herrmann's EMSI Project

## Requirements
- Python 2.7
- Sample data folder from https://github.com/economicmodeling/data_engineer_technical_project

## Getting Started
The simplest way to run the project is to clone the sample data to a sibling folder and run:

```bash
python process_sample_data.py ../data_engineer_technical_project/sample.gz ../data_engineer_technical_project/map_onet_soc.csv ../data_engineer_technical_project/soc_hierarchy.csv
```

This will begin processing the listings from sample.gz. When it is finished there will be a sqlite database called ```interview_project.db``` in the root folder.

## Summary Output
- The count of documents with HTML tags removed will be output to the terminal
- To get the count of soc2 listings, run ```sql_scripts/count_soc2.sql``` against ```interview_project.db```
- To get the count of listings active on February 1 2017, run ```sql_scripts/active_on_2017_02_01.sql``` against ```interview_project.db```

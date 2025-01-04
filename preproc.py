import os
import pandas as pd
import re
from rake_nltk import Rake
import nltk
nltk.download('stopwords')
nltk.download('punkt')
import mysql.connector

sql_user = input("enter mysql username: ")
sql_pass = input("enter mysql password: ")

conn = mysql.connector.connect(
    host='localhost',
    user=sql_user,
    password=sql_pass
)


df = pd.read_csv('./reddit_tech_data.csv')

def extract_data(text):
    data = {}

    username_match = re.search(r'u/(\w+)', text)
    if username_match:
        data['username'] = "@user"

    subreddit_match = re.search(r'r/(\w+)', text)
    if subreddit_match:
        data['subreddit'] = subreddit_match.group(1)

    url_match = re.search(r'(https?://[^\s]+)', text)
    if url_match:
        data['url'] = url_match.group(1)

    upvotes_match = re.search(r'(?:Upvote|points)[\s\n]+(\d+)', text, re.DOTALL)
    if upvotes_match:
        data['upvotes'] = int(upvotes_match.group(1))
    else:
      data['upvotes'] = 0

    comments_match = re.search(r'(\d+)\scomments', text)
    if comments_match:
        data['comments'] = int(comments_match.group(1))
    else:
      data['comments'] = 0

    timestamp_match = re.search(r'(\d+)\s*([a-zA-Z]+\.?)\s*ago', text)
    if timestamp_match:
        amount, unit = timestamp_match.groups()
        data['timestamp'] = f"{amount} {unit} ago"

    return data

df['extracted_data'] = df['shreddit-post'].apply(extract_data)

extracted_df = pd.DataFrame(df['extracted_data'].tolist())

titles = pd.DataFrame(df['faceplate-screen-reader-content'])

result_df = pd.merge(titles, extracted_df, left_index=True, right_index=True)

result_df.rename(columns={'faceplate-screen-reader-content': 'content'}, inplace=True)


def extract_keywords(text):
    r = Rake()
    r.extract_keywords_from_text(text)
    keywords = r.get_ranked_phrases()
    return keywords

result_df['keywords'] = result_df['content'].apply(extract_keywords)
result_df = result_df.fillna('')
cursor = conn.cursor()
cursor.execute('''
    use reddit_tech;
'''
)
for index, row in result_df.iterrows():
    keywords_str = ', '.join(row['keywords'])
    
    insert_data = (row['content'], row['username'], row['subreddit'], row['url'],
                   row['upvotes'], row['comments'], row['timestamp'], keywords_str)

    insert_query = """
    INSERT INTO posts (content, username, subreddit, url, upvotes, comments, timestamp, keywords)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(insert_query, insert_data)

select_query = "SELECT * FROM posts;"

verify = pd.read_sql_query(select_query, conn)

verify.to_csv('output_data.csv', index=False)


conn.commit()
conn.close()

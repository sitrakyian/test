import re
import pandas as pd
from textblob import TextBlob

def classify_bio(bio):
    # Define a list of job titles
    job_titles = ['software developer', 'software engineer', 'programmer', 'data scientist', 'data analyst', 'marketing manager', 'sales manager']

    # Analyze the bio to extract the job title
    blob = TextBlob(bio).lower()
    job_title = None
    for word in blob.noun_phrases:
        if word in [job_title.lower() for job_title in job_titles]:
            job_title = word
            print(word)
            break

    return job_title if job_title else 'Unknown'

# Read the CSV file
df = pd.read_csv('result.csv')

# Fill missing values in the 'bio' column with an empty string
df['bio'] = df['bio'].fillna('')

# Classify the job titles
df['job_title'] = df['bio'].apply(classify_bio)

# Print the classified job titles
print(df[['profileName', 'job_title']])
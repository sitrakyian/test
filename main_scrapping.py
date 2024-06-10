import pandas as pd
import string
from textblob import TextBlob

# Define a function to extract the job title from a string
def classify_bio(lines):
    # Define a list of job titles
    job_titles = ['software developer', 'software engineer', 'programmer', 'data scientist', 'data analyst', 'marketing manager', 'sales manager']

    # Analyze each line to extract the job title
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Remove punctuation marks and special characters from the line
        line = line.translate(str.maketrans('', '', string.punctuation))

        # Extract the job title from the line
        blob = TextBlob(line)
        job_title = None
        for word in blob.noun_phrases:
            if word.lower() in [job_title.lower() for job_title in job_titles]:
                job_title = word
                break

        if job_title:
            return job_title

    return 'Unknown'

# Define a function to extract the job title from a row in the dataframe
def extract_job_title(row):
    # Check if the 'bio' column is a string
    if isinstance(row['bio'], str):
        # Split the 'bio' column into multiple lines
        lines = row['bio'].splitlines()

        # Extract the job title from the lines
        job_title = classify_bio(lines)

        # Return the job title
        return job_title
    else:
        # Return a default value if the 'bio' column is not a string
        return 'Unknown'

# Load the data from a CSV file
df = pd.read_csv('result.csv')

# Apply the 'extract_job_title' function to each row in the dataframe
df['job_title'] = df.apply(extract_job_title, axis=1)

# Print the first 10 rows of the dataframe
print(df.head(10))
import requests
from bs4 import BeautifulSoup
import re
from textblob import TextBlob

# Set up the headers and cookies
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'
}

# Set up the Instagram account URL
instagram_url = 'https://www.instagram.com/villaclapotis/'

# Send a GET request to the Instagram account page
response = requests.get(instagram_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the list of followers
    followers = soup.find_all('a', {'class': 'FPmhX notranslate _0imsa'})

    # Initialize a dictionary to store the classified followers
    classified_followers = {}

    # Loop through each follower
    for follower in followers:
        # Extract the follower's username
        username = follower.text.strip()

        # Send a GET request to the follower's profile page
        follower_url = f'https://www.instagram.com/{username}/'
        follower_response = requests.get(follower_url, headers=headers)

        # Check if the request was successful
        if follower_response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            follower_soup = BeautifulSoup(follower_response.content, 'html.parser')

            # Extract the follower's bio
            bio = follower_soup.find('div', {'class': 'PQo_M'}).text.strip()

            # Analyze the bio to extract the job title
            blob = TextBlob(bio)
            job_title = None
            for word in blob.noun_phrases:
                if 'developer' in word.lower() or 'engineer' in word.lower() or 'programmer' in word.lower():
                    job_title = word
                    break

            # Classify the follower based on the job title
            if job_title:
                if job_title not in classified_followers:
                    classified_followers[job_title] = []
                classified_followers[job_title].append(username)

    # Print the classified followers
    for job_title, followers in classified_followers.items():
        print(f'{job_title}: {followers}')
    

else:
    print(f'Error: {response.status_code}')

print(response.status_code)
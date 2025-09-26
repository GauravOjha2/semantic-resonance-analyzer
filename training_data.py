import pandas as pd
import praw
from dotenv import load_dotenv
import os
import sys

# --- 1. SECURELY LOAD API CREDENTIALS ---
# This function loads variables from a file named '.env' in your project folder.
# This keeps your secret keys out of the code and safe from GitHub.
print("Loading API credentials from .env file...")
load_dotenv()

# We retrieve the credentials from the environment variables.
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# This is a critical safety check. If the keys are not found, the script will stop
# with a helpful error message.
if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, USER_AGENT]):
    print("\n🔴 FATAL ERROR: Reddit API credentials not found in .env file.")
    print("Please create a .env file in your project folder with your credentials:")
    print("REDDIT_CLIENT_ID='Your_Client_ID'")
    print("REDDIT_CLIENT_SECRET='Your_Client_Secret'")
    print("REDDIT_USER_AGENT='A_Descriptive_User_Agent_by_u/your_username'")
    sys.exit(1) # This stops the script from running with an error.

# --- 2. INITIALIZE REDDIT API CONNECTION ---
try:
    print("Connecting to Reddit API...")
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT
    )
    # The following line checks if the connection is read-only and valid.
    _ = reddit.user.me() 
    print("✅ Successfully connected to Reddit API.")
except Exception as e:
    print(f"\n🔴 FATAL ERROR: Could not connect to Reddit API. Please check your credentials.\nDetails: {e}")
    sys.exit(1)

# --- 3. DATA FETCHING FUNCTIONS ---
def fetch_user_comments(username: str, limit: int = 150):
    """Fetches the most recent comments for a given Reddit user."""
    print(f"  -> Fetching up to {limit} comments for u/{username}...")
    try:
        user = reddit.redditor(username)
        comments = [
            {"text": comment.body, "created_utc": comment.created_utc, "subreddit": str(comment.subreddit)}
            for comment in user.comments.new(limit=limit)
        ]
        return pd.DataFrame(comments)
    except Exception as e:
        print(f"     Could not fetch comments for {username}. Error: {e}")
        return pd.DataFrame() # Return an empty DataFrame on error

def fetch_user_posts(username: str, limit: int = 50):
    """Fetches the most recent submissions (posts) for a given Reddit user."""
    print(f"  -> Fetching up to {limit} posts for u/{username}...")
    try:
        user = reddit.redditor(username)
        posts = [
            {"text": submission.title + " " + (submission.selftext or ""), "created_utc": submission.created_utc, "subreddit": str(submission.subreddit)}
            for submission in user.submissions.new(limit=limit)
        ]
        return pd.DataFrame(posts)
    except Exception as e:
        print(f"     Could not fetch posts for {username}. Error: {e}")
        return pd.DataFrame() # Return an empty DataFrame on error

# --- 4. MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    # Define the two users we want to analyze
    user_a = "mistersavage"
    user_b = "J_Ken_Alt"

    print(f"\n--- Starting Data Scraping for {user_a} ---")
    df_a_comments = fetch_user_comments(user_a)
    df_a_posts = fetch_user_posts(user_a)
    
    print(f"\n--- Starting Data Scraping for {user_b} ---")
    df_b_comments = fetch_user_comments(user_b)
    df_b_posts = fetch_user_posts(user_b)

    # Combine the comments and posts into a single DataFrame for each user
    df_a = pd.concat([df_a_comments, df_a_posts], ignore_index=True)
    df_b = pd.concat([df_b_comments, df_b_posts], ignore_index=True)

    # Save the final data to CSV files
    df_a.to_csv(f"{user_a}_reddit.csv", index=False)
    df_b.to_csv(f"{user_b}_reddit.csv", index=False)

    print("\n----------------------------------------------------")
    print("✅ SCRAPING COMPLETE!")
    print(f"Saved {len(df_a)} total entries for {user_a} to '{user_a}_reddit.csv'")
    print(f"Saved {len(df_b)} total entries for {user_b} to '{user_b}_reddit.csv'")
    print("----------------------------------------------------")

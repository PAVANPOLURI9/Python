import tweepy
from tweepy import OAuth1UserHandler, API, Client
from dotenv import load_dotenv
import pandas as pd
import os
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import time

# Load environment variables from .env file (if available)
load_dotenv()

# Twitter API Credentials (replace with your own or set in .env)
CONSUMER_KEY = os.getenv('CONSUMER_KEY', 'your_consumer_key')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET', 'your_consumer_secret')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', 'your_access_token')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET', 'your_access_token_secret')
BEARER_TOKEN = os.getenv('BEARER_TOKEN', 'AAAAAAAAAAAAAAAAAAAAABqnzgEAAAAAWgfPnef68a1Am91yS9qZi2EpgzQ%3D0ytfEqueFbgoUeViNyiKP30lcETv0pJb2IfF8ekSIZh7ea4GQx')

# Output paths
OUTPUT_CSV = "ipl_2020_combined_data.csv"
OUTPUT_CHART_DIR = "visualizations"
os.makedirs(OUTPUT_CHART_DIR, exist_ok=True)

# Authenticate Twitter API (v1.1 for real-time, v2 for historical)
auth = OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = API(auth, wait_on_rate_limit=True)
client = Client(bearer_token=BEARER_TOKEN)

# Function to scrape tweets with v1.1 API (real-time)
def scrape_v1_tweets(query, max_tweets=100):
    tweets = []
    try:
        print("Scraping with Twitter API v1.1 (real-time search)...")
        for tweet in tweepy.Cursor(api.search_tweets,
                                   q=query,
                                   lang="en",
                                   tweet_mode='extended').items(max_tweets):
            tweets.append({
                "date": tweet.created_at,
                "username": tweet.user.screen_name,
                "text": tweet.full_text,
                "likes": tweet.favorite_count,
                "retweets": tweet.retweet_count,
                "source": "v1.1"
            })
        print(f"Scraped {len(tweets)} tweets with v1.1 API.")
    except tweepy.TweepyException as e:
        print(f"v1.1 Error: {str(e)}")
    return tweets

# Function to scrape tweets with v2 API (historical)
def scrape_v2_tweets(query, start_time, end_time, max_tweets=1000):
    tweets = []
    try:
        print("Scraping with Twitter API v2 (historical search)...")
        for tweet in tweepy.Paginator(client.search_all_tweets,
                                      query=query,
                                      start_time=start_time,
                                      end_time=end_time,
                                      tweet_fields=["created_at", "public_metrics"],
                                      max_results=100).flatten(limit=max_tweets):
            tweets.append({
                "date": tweet.created_at,
                "username": tweet.author_id,  # Author ID (username lookup not included here)
                "text": tweet.text,
                "likes": tweet.public_metrics["like_count"],
                "retweets": tweet.public_metrics["retweet_count"],
                "source": "v2"
            })
        print(f"Scraped {len(tweets)} tweets with v2 API.")
    except tweepy.TweepyException as e:
        print(f"v2 Error: {str(e)}")
    return tweets

# Function to extract team names from text
def extract_team(text):
    teams = {
        'Mumbai Indians': ['mi', 'mumbai indians', 'mumbai', 'rohit', 'bumrah'],
        'Delhi Capitals': ['dc', 'delhi capitals', 'delhi', 'pant', 'iyer'],
        'Chennai Super Kings': ['csk', 'chennai super kings', 'chennai', 'dhoni'],
        'Royal Challengers Bangalore': ['rcb', 'royal challengers', 'bangalore', 'kohli'],
        'Kolkata Knight Riders': ['kkr', 'kolkata knight riders', 'kolkata', 'russell'],
        'Rajasthan Royals': ['rr', 'rajasthan royals', 'rajasthan', 'smith'],
        'Sunrisers Hyderabad': ['srh', 'sunrisers hyderabad', 'hyderabad', 'warner'],
        'Kings XI Punjab': ['kxip', 'kings xi punjab', 'punjab', 'rahul']
    }
    text = str(text).lower()
    for team, keywords in teams.items():
        if any(keyword in text for keyword in keywords):
            return team
    return None

# Main function to scrape, aggregate, and visualize
def main():
    # Queries and timeframe
    v1_query = "#IPL2020 OR IPL 2020 OR Indian Premier League 2020"
    v2_query = "#IPL2020 -is:retweet"
    start_time = "2020-09-01T00:00:00Z"
    end_time = "2020-11-30T23:59:59Z"
    max_v1_tweets = 100
    max_v2_tweets = 1000

    # Scrape tweets
    v1_tweets = scrape_v1_tweets(v1_query, max_v1_tweets)
    v2_tweets = scrape_v2_tweets(v2_query, start_time, end_time, max_v2_tweets)
    all_tweets = v1_tweets + v2_tweets

    if not all_tweets:
        print("No tweets scraped. Check API credentials or rate limits.")
        return

    # Create DataFrame
    df = pd.DataFrame(all_tweets)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['team'] = df['text'].apply(extract_team)
    df = df.dropna(subset=['team'])  # Drop rows without team

    # Placeholder for sentiment (assuming it's not available; add your own if you have it)
    # Here, we'll simulate sentiment based on likes (arbitrary threshold)
    df['sentiment_label'] = df['likes'].apply(lambda x: 'Positive' if x > 5 else 'Negative' if x < 2 else 'Neutral')

    # Aggregate sentiment data
    team_sentiment = df.groupby(['team', 'sentiment_label']).size().unstack(fill_value=0)
    team_sentiment_pct = team_sentiment.div(team_sentiment.sum(axis=1), axis=0) * 100

    df['month_year'] = df['date'].dt.strftime('%Y-%m')
    monthly_team_sentiment = df.groupby(['team', 'month_year', 'sentiment_label']).size().unstack(fill_value=0)

    df['week'] = df['date'].dt.isocalendar().week
    weekly_team_sentiment = df.groupby(['team', 'week', 'sentiment_label']).size().unstack(fill_value=0)

    # Save to single CSV
    combined_df = pd.concat([
        df[['date', 'username', 'text', 'likes', 'retweets', 'team', 'sentiment_label', 'source']],
        team_sentiment.add_prefix('count_'),
        team_sentiment_pct.add_prefix('pct_'),
        monthly_team_sentiment.add_prefix('monthly_'),
        weekly_team_sentiment.add_prefix('weekly_')
    ], axis=1)
    combined_df.to_csv(OUTPUT_CSV, index=False)
    print(f"\nAll data saved to {OUTPUT_CSV}. Total rows: {len(combined_df)}")

    # Winning percentage (based on positive sentiment)
    winning_pct = team_sentiment_pct['Positive'].sort_values(ascending=False)
    print("\nSentiment-Based Winning Percentage:")
    print(winning_pct.to_string(header=False))

    final_winner = "Mumbai Indians"
    print(f"\nFinal Winner of IPL 2020: {final_winner}")

    # Visualizations
    # Bar chart for winning percentage
    colors = ['green' if team == final_winner else 'skyblue' for team in winning_pct.index]
    plt.figure(figsize=(10, 6))
    winning_pct.plot(kind='bar', color=colors)
    plt.title('Sentiment-Based Winning Percentage for IPL 2020 Teams\n(Mumbai Indians Highlighted)')
    plt.xlabel('Team')
    plt.ylabel('Positive Sentiment (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_CHART_DIR, 'winning_percentage_bar.png'))
    plt.close()

    # Weekly trend for Mumbai Indians
    mi_weekly = weekly_team_sentiment[weekly_team_sentiment.index.get_level_values('team') == 'Mumbai Indians']
    if not mi_weekly.empty:
        mi_weekly = mi_weekly.reset_index()
        mi_weekly.plot(x='week', y=['Negative', 'Neutral', 'Positive'], kind='line', figsize=(10, 6))
        plt.title('Weekly Sentiment Trends for Mumbai Indians')
        plt.xlabel('Week')
        plt.ylabel('Count')
        plt.legend(title='Sentiment')
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_CHART_DIR, 'mi_weekly_trend.png'))
        plt.close()

    # Word cloud for Mumbai Indians positive tweets
    mi_positive_text = df[(df['team'] == 'Mumbai Indians') & (df['sentiment_label'] == 'Positive')]['text'].dropna()
    if not mi_positive_text.empty:
        text = mi_positive_text.str.cat(sep=' ')
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud for Positive Tweets about Mumbai Indians')
        plt.savefig(os.path.join(OUTPUT_CHART_DIR, 'mi_positive_wordcloud.png'))
        plt.close()

    # Analyze Mumbai Indians
    if 'Mumbai Indians' in team_sentiment.index:
        mi_sentiment = team_sentiment.loc['Mumbai Indians']
        print(f"\nMumbai Indians Sentiment Counts: {mi_sentiment.to_dict()}")
        print(f"Positive Sentiment Percentage: {team_sentiment_pct.loc['Mumbai Indians', 'Positive']:.2f}%")
        mi_week_45 = mi_weekly[mi_weekly['week'] == 45] if not mi_weekly.empty else pd.DataFrame()
        if not mi_week_45.empty:
            print(f"Week 45 (Final Week) Sentiment: {mi_week_45[['Negative', 'Neutral', 'Positive']].iloc[0].to_dict()}")

if __name__ == "__main__":
    main()
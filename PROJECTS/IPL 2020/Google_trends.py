from pytrends.request import TrendReq
import pandas as pd
import time
from pytrends import exceptions

# Initialize pytrends without retries parameter
pytrends = TrendReq(hl='en-US', tz=360)

# List of IPL 2020 teams
teams = [
    "Mumbai Indians", "Chennai Super Kings", "Delhi Capitals", 
    "Kings XI Punjab", "Royal Challengers Bangalore", "Sunrisers Hyderabad",
    "Rajasthan Royals", "Kolkata Knight Riders"
]

# Set timeframe for IPL 2020 (Sep 1 - Nov 30, 2020)
timeframe = "2020-09-01 2020-11-30"

# Function to fetch trends with manual retry logic
def fetch_trends(keywords, max_retries=5):
    for attempt in range(max_retries):
        try:
            pytrends.build_payload(kw_list=keywords, timeframe=timeframe, geo="IN")
            interest_over_time = pytrends.interest_over_time()
            if not interest_over_time.empty:
                return interest_over_time.drop(columns=['isPartial'], errors='ignore')
            return None
        except exceptions.TooManyRequestsError:
            print(f"Rate limit hit for {keywords}. Waiting {10 * (attempt + 1)} seconds...")
            time.sleep(10 * (attempt + 1))  # Exponential backoff
        except Exception as e:
            print(f"Error fetching {keywords}: {str(e)}")
            return None
    print(f"Failed to fetch {keywords} after {max_retries} attempts.")
    return None

# Batch teams (up to 5 per request)
batches = [teams[i:i+5] for i in range(0, len(teams), 5)]
dataframes = []

for batch in batches:
    print(f"Fetching trends for: {batch}")
    df = fetch_trends(batch)
    if df is not None:
        dataframes.append(df)
    time.sleep(10)  # Base delay between batches

# Combine data into one DataFrame
if dataframes:
    combined_data = pd.concat(dataframes, axis=1)
    # Save to CSV
    combined_data.to_csv("ipl_2020_google_trends.csv")
    print("Google Trends data saved to ipl_2020_google_trends.csv")
    # Preview
    print(combined_data.head())
else:
    print("No data collected due to persistent errors.")
    combined_data = pd.DataFrame()  # Define empty DataFrame to avoid NameError

# Optional: Plot trends
import matplotlib.pyplot as plt
if not combined_data.empty:
    combined_data.plot(figsize=(12, 6))
    plt.title("IPL 2020 Team Search Interest on Google Trends")
    plt.xlabel("Date")
    plt.ylabel("Search Interest (0-100)")
    plt.legend(title="Teams")
    plt.show()
else:
    print("No data to plot.")
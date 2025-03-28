import pandas as pd
import re
from datetime import datetime
import os

# Step 1: Load the CSV file
# Replace 'ipl_2020_matches.csv' with the path to your CSV file
df = pd.read_csv("C:\AI\Python\IPL 2020\ipl2020_commentary.csv")
print(f"Initial number of rows: {len(df)}")
print(df.columns)

# Step 2: Initial Cleaning
# Remove duplicates
df = df.drop_duplicates(subset=["match_url"])
print(f"Number of rows after removing duplicates: {len(df)}")

# Handle missing values
df = df.dropna(subset=["match_url", "match_title"])
df["commentary"] = df["commentary"].fillna("No commentary available")

# Standardize column names
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Step 3: Extract Match Dates
def extract_date(subhdr):
    match = re.search(r"Date & Time: (\w{3} \d{1,2}),", subhdr)
    if match:
        date_str = match.group(1) + ", 2020"  # Append year (IPL 2020)
        return datetime.strptime(date_str, "%b %d, %Y").strftime("%Y-%m-%d")
    return None

df["match_date"] = df["match_subhdr"].apply(extract_date)
df = df.dropna(subset=["match_date"])

# Step 4: Extract Teams and Result
df["team1"] = df["match_title"].str.extract(r"^(.*?) vs")[0]
df["team2"] = df["match_title"].str.extract(r"vs (.*?),")[0]
df["winner"] = df["match_status"].str.extract(r"^(.*?) won")[0]
df["margin"] = df["match_status"].str.extract(r"won by (.*)$")[0]

# Handle tied matches
df.loc[df["match_status"].str.contains("tied"), "winner"] = df["match_status"].str.extract(r"\((.*?) won")[0]
df.loc[df["match_status"].str.contains("tied"), "margin"] = "Super Over"

# Step 5: Clean and Split Commentary
def extract_commentary_sections(commentary):
    quotes = []
    ball_by_ball = []
    stats = []
    summaries = []

    lines = commentary.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r".*?\|.*?:", line):
            quotes.append(line)
        elif re.match(r"^(?:Ball \d+:)?\w+ to \w+", line):
            ball_by_ball.append(line)
        elif re.match(r"^(Stats|Highest|Most|Tied matches)", line):
            stats.append(line)
        elif re.match(r"^\d{2}:\d{2} Local Time", line):
            summaries.append(line)

    return {
        "quotes": "\n".join(quotes),
        "ball_by_ball": "\n".join(ball_by_ball),
        "stats": "\n".join(stats),
        "summaries": "\n".join(summaries)
    }

# Apply the function to split commentary
commentary_sections = df["commentary"].apply(extract_commentary_sections)
df["quotes"] = commentary_sections.apply(lambda x: x["quotes"])
df["ball_by_ball"] = commentary_sections.apply(lambda x: x["ball_by_ball"])
df["stats"] = commentary_sections.apply(lambda x: x["stats"])
df["summaries"] = commentary_sections.apply(lambda x: x["summaries"])

# Drop the original commentary column
df = df.drop(columns=["commentary"])

# Remove unwanted phrases
unwanted_phrases = ["Cricbuzz Video", "Cricbuzz LIVE", "Cricbuzz Live"]
for col in ["quotes", "ball_by_ball", "stats", "summaries"]:
    for phrase in unwanted_phrases:
        df[col] = df[col].str.replace(phrase, "", regex=False)

# Normalize text
text_columns = ["quotes", "ball_by_ball", "stats", "summaries"]
for col in text_columns:
    df[col] = df[col].str.lower().str.strip()
    df[col] = df[col].str.replace(r"\s+", " ", regex=True)
    df[col] = df[col].str.replace(r"[^\w\s]", "", regex=True)

# Step 6: Extract Quotes, Stats, and Ball-by-Ball Data into Separate DataFrames
# Quotes
quotes_list = []
for idx, row in df.iterrows():
    match_url = row["match_url"]
    match_date = row["match_date"]
    quotes = row["quotes"].split("\n")
    for quote in quotes:
        if quote:
            speaker = quote.split(" ")[0]  # Simplified; improve with regex if needed
            quotes_list.append({
                "match_url": match_url,
                "match_date": match_date,
                "speaker": speaker,
                "quote": quote
            })
df_quotes = pd.DataFrame(quotes_list)

# Stats
stats_list = []
for idx, row in df.iterrows():
    match_url = row["match_url"]
    stats = row["stats"].split("\n")
    for stat in stats:
        if stat:
            stats_list.append({
                "match_url": match_url,
                "stat": stat
            })
df_stats = pd.DataFrame(stats_list)

# Ball-by-Ball
ball_by_ball_list = []
for idx, row in df.iterrows():
    match_url = row["match_url"]
    balls = row["ball_by_ball"].split("\n")
    for ball in balls:
        if ball:
            bowler = ball.split(" to ")[0].strip()
            batsman = ball.split(" to ")[1].split(",")[0].strip()
            action = ball.split(",")[1].strip() if "," in ball else "no action"
            ball_by_ball_list.append({
                "match_url": match_url,
                "bowler": bowler,
                "batsman": batsman,
                "action": action
            })
df_ball_by_ball = pd.DataFrame(ball_by_ball_list)

# Step 7: Final Cleaning and Validation
# Drop irrelevant columns
df = df.drop(columns=["match_subhdr"])

# Standardize team names
team_mapping = {
    "mumbai indians": "MI",
    "chennai super kings": "CSK",
    "delhi capitals": "DC",
    "punjab kings": "PBKS",
    "sunrisers hyderabad": "SRH",
    "royal challengers bangalore": "RCB",
    "rajasthan royals": "RR",
    "kings xi punjab": "PBKS",
}
for col in ["team1", "team2", "winner"]:
    df[col] = df[col].str.lower().map(team_mapping).fillna(df[col])

# Validate dates
df["match_date"] = pd.to_datetime(df["match_date"])
df = df[(df["match_date"] >= "2020-09-19") & (df["match_date"] <= "2020-11-10")]

# Remove rows with no winner
df = df.dropna(subset=["winner"])

# Step 8: Save the Cleaned Data
output_dir = "cleaned_ipl_data"
os.makedirs(output_dir, exist_ok=True)

df.to_csv(os.path.join(output_dir, "cleaned_ipl_2020_matches.csv"), index=False)
df_quotes.to_csv(os.path.join(output_dir, "ipl_2020_quotes.csv"), index=False)
df_stats.to_csv(os.path.join(output_dir, "ipl_2020_stats.csv"), index=False)
df_ball_by_ball.to_csv(os.path.join(output_dir, "ipl_2020_ball_by_ball.csv"), index=False)

print("Cleaned data saved successfully in the following files:")
print("- cleaned_ipl_2020_matches.csv")
print("- ipl_2020_quotes.csv")
print("- ipl_2020_stats.csv")
print("- ipl_2020_ball_by_ball.csv")

# Display a preview of the cleaned data
print("\nPreview of Cleaned Matches Data:")
print(df[["match_url", "match_title", "match_date", "team1", "team2", "winner", "margin"]].head())

print("\nPreview of Quotes Data:")
print(df_quotes.head())

print("\nPreview of Stats Data:")
print(df_stats.head())

print("\nPreview of Ball-by-Ball Data:")
print(df_ball_by_ball.head())
import pandas as pd

# Step 1: Load the CSV file
# Replace 'ipl2020_matches.csv' with the path to your actual CSV file
file_path = 'C:\AI\Python\IPL 2020\ipl_2020_matches.csv'  # Update this with your file path
df = pd.read_csv(file_path)

# Step 2: Clean the Date Column
# Remove the day name (e.g., "Sat,") and standardize the format
df['date'] = df['date'].str.replace(r'^(Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s*', '', regex=True)  # Remove day name
df['date'] = df['date'].str.strip()  # Remove extra spaces

# Fill missing dates with the previous row's date
df['date'] = df['date'].replace('', pd.NA).ffill()

# Convert to datetime (assuming format like "19 Sep '20")
df['date'] = pd.to_datetime(df['date'], format="%d %b '%y")
df['date'] = df['date'].dt.strftime('%Y-%m-%d')  # Format as YYYY-MM-DD

# Step 3: Standardize Team Names in winner and loser columns
# Replace "Kings XI" with "KXIP" and ensure consistency
df['winner'] = df['winner'].replace('Kings XI', 'KXIP')
df['loser'] = df['loser'].replace('Kings XI', 'KXIP')

# Ensure all team names are uppercase for consistency
df['winner'] = df['winner'].str.upper()
df['loser'] = df['loser'].str.upper()

# Step 4: Extract Match Stage and Clean Match Column
# Create a new 'stage' column based on the 'match' column
def extract_stage(match):
    if 'Qualifier 1' in match:
        return 'Qualifier 1'
    elif 'Qualifier 2' in match:
        return 'Qualifier 2'
    elif 'Eliminator' in match:
        return 'Eliminator'
    elif 'Final' in match:
        return 'Final'
    else:
        return 'League'

df['stage'] = df['match'].apply(extract_stage)

# Clean the 'match' column: Remove "(N)" and keep only the match description
df['match'] = df['match'].str.replace(r'\s*\(N\)', '', regex=True)  # Remove "(N)"
df['match'] = df['match'].str.strip()

# Step 5: Standardize Place Names
df['place'] = df['place'].str.replace(' \(DICS\)', '', regex=True)  # Remove "(DICS)" from Dubai
df['place'] = df['place'].str.strip()

# Step 6: Handle Ties
# Ties are already marked as "Tie" in winner and loser columns, so we'll leave them as is

# Step 7: Final Cleanup
# Remove any extra spaces in all columns
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Ensure all string columns are uppercase for consistency
df['match'] = df['match'].str.upper()
df['place'] = df['place'].str.upper()
df['stage'] = df['stage'].str.upper()

# Step 8: Save the Cleaned Data to a New CSV
output_file = 'cleaned_ipl2020_matches.csv'
df.to_csv(output_file, index=False)
print(f"Cleaned data saved to: {output_file}")

# Step 9: Display the First Few Rows of the Cleaned Data
print("\nFirst few rows of the cleaned data:")
print(df.head())

# Step 10: Confirm the Winner of IPL 2020
final_match = df[df['stage'] == 'FINAL']
if not final_match.empty:
    winner = final_match['winner'].iloc[0]
    print(f"\nThe winner of IPL 2020 is: {winner}")
else:
    print("\nFinal match not found in the data.")
import pandas as pd

# Step 1: Load the CSV file
# Replace 'points_table.csv' with the path to your actual CSV file
file_path = 'C:\AI\Python\IPL 2020\ipl_2020_points_table.csv'  # Update this with your file path
df = pd.read_csv(file_path)

# Step 2: Standardize Team Names
# Replace "PBKS" with "KXIP" to match IPL 2020 naming
df['Team'] = df['Team'].replace('PBKS', 'KXIP')

# Convert all team names to uppercase for consistency
df['Team'] = df['Team'].str.upper()

# Step 3: Clean Recent Form
# Ensure Recent Form contains only "W" and "L" and is uppercase
df['Recent Form'] = df['Recent Form'].str.upper()
# Validate that it only contains "W" and "L"
df['Recent Form'] = df['Recent Form'].apply(lambda x: x if all(c in ['W', 'L'] for c in x) else None)

# Step 4: Handle Numerical Columns
# Convert Position, Played, Won, Lost, No Result, Points to integers
numeric_cols = ['Position', 'Played', 'Won', 'Lost', 'No Result', 'Points']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce', downcast='integer')

# Convert NRR to float
df['NRR'] = pd.to_numeric(df['NRR'], errors='coerce')

# Step 5: Split For and Against Columns into Runs and Overs
# Split 'For' into 'Runs For' and 'Overs For'
df[['Runs For', 'Overs For']] = df['For'].str.split('/', expand=True)
df['Runs For'] = pd.to_numeric(df['Runs For'], errors='coerce', downcast='integer')
df['Overs For'] = pd.to_numeric(df['Overs For'], errors='coerce')

# Split 'Against' into 'Runs Against' and 'Overs Against'
df[['Runs Against', 'Overs Against']] = df['Against'].str.split('/', expand=True)
df['Runs Against'] = pd.to_numeric(df['Runs Against'], errors='coerce', downcast='integer')
df['Overs Against'] = pd.to_numeric(df['Overs Against'], errors='coerce')

# Drop the original 'For' and 'Against' columns if no longer needed
df = df.drop(columns=['For', 'Against'])

# Step 6: General Cleanup
# Remove any extra spaces in all columns
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Step 7: Save the Cleaned Data to a New CSV
output_file = 'cleaned_ipl2020_points_table.csv'
df.to_csv(output_file, index=False)
print(f"Cleaned data saved to: {output_file}")

# Step 8: Display the Cleaned Data
print("\nCleaned points table data:")
print(df)

# Step 9: Optional Validation
# Verify that the Position column has no duplicates
if df['Position'].duplicated().any():
    print("\nWarning: Duplicate positions found in the data.")
else:
    print("\nNo duplicate positions found.")

# Verify that Played = Won + Lost + No Result for each team
df['Calculated Played'] = df['Won'] + df['Lost'] + df['No Result']
if (df['Played'] == df['Calculated Played']).all():
    print("Validation: Played matches equal the sum of Won, Lost, and No Result for all teams.")
else:
    print("Validation Warning: Played matches do not equal the sum of Won, Lost, and No Result for some teams.")
    print(df[df['Played'] != df['Calculated Played']][['Team', 'Played', 'Won', 'Lost', 'No Result']])

# Drop the temporary 'Calculated Played' column
df = df.drop(columns=['Calculated Played'])
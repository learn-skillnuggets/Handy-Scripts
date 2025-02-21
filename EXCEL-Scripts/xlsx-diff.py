import pandas as pd

# Load the Excel files into DataFrames
asset_df = pd.read_excel('Asset-amended.xlsx', engine='openpyxl')
contact_df = pd.read_excel('Contact.xlsx', engine='openpyxl')

# Print column names for debugging
print("Asset-amended.xlsx columns:", asset_df.columns)
print("Contact.xlsx columns:", contact_df.columns)

# Ensure the columns are treated as strings for comparison
asset_df['AccountId'] = asset_df['AccountId'].astype(str)
contact_df['AccountId'] = contact_df['AccountId'].astype(str)

# Convert Email column to string, handling NaN values
contact_df['Email'] = contact_df['Email'].fillna('').astype(str)

# Create a dictionary from Contact.xlsx with AccountId as key and list of Emails as value
contact_dict = contact_df.groupby('AccountId')['Email'].apply(lambda x: ';'.join(filter(None, x))).to_dict()

# Function to map values from contact_dict to Asset-amended.xlsx
def map_values(row):
    return contact_dict.get(row['AccountId'], None)

# Apply the function to the Asset-amended DataFrame
asset_df['Email Address'] = asset_df.apply(map_values, axis=1)

# Save the updated DataFrame to a new Excel file with a fixed name
output_filename = 'Asset-amended_updated.xlsx'
asset_df.to_excel(output_filename, index=False, engine='openpyxl')

print(f'Data has been updated and saved to {output_filename}')

import pandas as pd

# Load the voter dataset
input_file = "dataset/voters.csv"
output_file = "dataset/cleaned_voters.csv"

voters = pd.read_csv(input_file)

print("===== BEFORE PREPROCESSING =====")
print("Number of records:", len(voters))
print("\nMissing values:")
print(voters.isnull().sum())

# Remove completely duplicated rows
voters = voters.drop_duplicates()

# Clean text columns
text_columns = ["name", "gender", "address", "constituency", "voting_status"]

for column in text_columns:
    voters[column] = voters[column].astype(str).str.strip().str.lower()

# Standardize date format
voters["date_of_birth"] = pd.to_datetime(
    voters["date_of_birth"],
    errors="coerce"
).dt.strftime("%Y-%m-%d")

# Remove records with missing essential values
essential_columns = [
    "voter_id",
    "name",
    "date_of_birth",
    "address",
    "constituency"
]

voters = voters.dropna(subset=essential_columns)

# Save cleaned dataset
voters.to_csv(output_file, index=False)

print("\n===== AFTER PREPROCESSING =====")
print("Number of records:", len(voters))

print("\nCleaned sample:")
print(voters.head())

print("\nCleaned dataset saved as:")
print(output_file)
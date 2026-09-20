import pandas as pd

# Load cleaned voter data
voters = pd.read_csv("dataset/cleaned_voters.csv")

print("===== ALREADY VOTED DETECTION =====")

found = False

for i in range(len(voters)):

    status = str(voters.iloc[i]["voting_status"]).strip().lower()

    if status == "yes":
        found = True

        print("\nAlready Voted Record Found")
        print("Voter ID:", voters.iloc[i]["voter_id"])
        print("Name:", voters.iloc[i]["name"])
        print("Constituency:", voters.iloc[i]["constituency"])
        print("Voting Status:", voters.iloc[i]["voting_status"])

if not found:
    print("No already-voted records found.")
import pandas as pd
from difflib import SequenceMatcher

# Load cleaned voter data
voters = pd.read_csv("dataset/cleaned_voters.csv")

def similarity(a, b):
    return SequenceMatcher(None, str(a), str(b)).ratio()

print("===== DUPLICATE DETECTION =====")

found = False

for i in range(len(voters)):
    for j in range(i + 1, len(voters)):

        name_score = similarity(
            voters.iloc[i]["name"],
            voters.iloc[j]["name"]
        )

        address_score = similarity(
            voters.iloc[i]["address"],
            voters.iloc[j]["address"]
        )

        phone_match = (
            voters.iloc[i]["phone"] == voters.iloc[j]["phone"]
        )

        dob_match = (
            voters.iloc[i]["date_of_birth"]
            == voters.iloc[j]["date_of_birth"]
        )

        # Suspicious if name is similar and other details match
        if name_score >= 0.70 and (
            phone_match or (dob_match and address_score >= 0.70)
        ):
            found = True

            print("\nSuspicious Similar Records")
            print("Voter 1:", voters.iloc[i]["voter_id"],
                  "-", voters.iloc[i]["name"])
            print("Voter 2:", voters.iloc[j]["voter_id"],
                  "-", voters.iloc[j]["name"])

            print("Name Similarity:", round(name_score, 2))
            print("Address Similarity:", round(address_score, 2))
            print("Phone Match:", phone_match)
            print("Date of Birth Match:", dob_match)

if not found:
    print("No suspicious duplicate records found.")
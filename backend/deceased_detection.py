import pandas as pd

# Load datasets
voters = pd.read_csv("dataset/cleaned_voters.csv")
death_registry = pd.read_csv("dataset/death_registry.csv")

print("===== DECEASED VOTER DETECTION =====")

found = False

for i in range(len(voters)):
    for j in range(len(death_registry)):

        name_match = (
            voters.iloc[i]["name"].lower()
            == death_registry.iloc[j]["name"].lower()
        )

        dob_match = (
            voters.iloc[i]["date_of_birth"]
            == death_registry.iloc[j]["date_of_birth"]
        )

        address_match = (
            voters.iloc[i]["address"].lower()
            == death_registry.iloc[j]["address"].lower()
        )

        # Match voter with death registry
        if name_match and dob_match and address_match:
            found = True

            print("\nDeceased Voter Match Found")
            print("Voter ID:", voters.iloc[i]["voter_id"])
            print("Name:", voters.iloc[i]["name"])
            print("Date of Birth:", voters.iloc[i]["date_of_birth"])
            print("Address:", voters.iloc[i]["address"])
            print("Date of Death:", death_registry.iloc[j]["date_of_death"])

if not found:
    print("No deceased voter matches found.")
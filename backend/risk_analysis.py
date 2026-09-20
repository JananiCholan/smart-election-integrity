import pandas as pd
from difflib import SequenceMatcher

# Load cleaned voter data
voters = pd.read_csv("dataset/cleaned_voters.csv")

# Load death registry
death_registry = pd.read_csv("dataset/death_registry.csv")


def similarity(a, b):
    return SequenceMatcher(None, str(a), str(b)).ratio()


print("===== ELECTION FRAUD RISK INDEX =====")

for i in range(len(voters)):

    voter = voters.iloc[i]

    duplicate = False
    deceased = False
    already_voted = False

    # Check already voted
    if str(voter["voting_status"]).lower() == "yes":
        already_voted = True

    # Check deceased
    for j in range(len(death_registry)):
        if (
            str(voter["name"]).lower()
            == str(death_registry.iloc[j]["name"]).lower()
            and voter["date_of_birth"]
            == death_registry.iloc[j]["date_of_birth"]
            and str(voter["address"]).lower()
            == str(death_registry.iloc[j]["address"]).lower()
        ):
            deceased = True
            break

    # Check duplicate/similar record
    for j in range(len(voters)):

        if i == j:
            continue

        other = voters.iloc[j]

        name_score = similarity(
            voter["name"],
            other["name"]
        )

        address_score = similarity(
            voter["address"],
            other["address"]
        )

        phone_match = voter["phone"] == other["phone"]

        dob_match = (
            voter["date_of_birth"]
            == other["date_of_birth"]
        )

        if name_score >= 0.70 and (
            phone_match or
            (dob_match and address_score >= 0.70)
        ):
            duplicate = True
            break

    # Calculate EFRI score
    score = 0

    if duplicate:
        score += 40

    if already_voted:
        score += 30

    if deceased:
        score += 30

    # Determine risk level
    if score <= 30:
        risk = "LOW RISK"
    elif score <= 60:
        risk = "MEDIUM RISK"
    else:
        risk = "HIGH RISK"

    # Display result only for suspicious records
    if score > 0:
        print("\n--------------------------------")
        print("Voter ID:", voter["voter_id"])
        print("Name:", voter["name"])
        print("EFRI Score:", score)
        print("Risk Level:", risk)

        print("Duplicate Evidence:", duplicate)
        print("Already Voted:", already_voted)
        print("Deceased Match:", deceased)
import pandas as pd
from difflib import SequenceMatcher


def similarity(a, b):
    return SequenceMatcher(None, str(a), str(b)).ratio()


def generate_risk_report():

    voters = pd.read_csv("dataset/cleaned_voters.csv")
    death_registry = pd.read_csv("dataset/death_registry.csv")

    report = []

    for i in range(len(voters)):

        voter = voters.iloc[i]

        duplicate = False
        deceased = False
        already_voted = False

        # Already voted check
        if str(voter["voting_status"]).strip().lower() == "yes":
            already_voted = True

        # Deceased check
        for j in range(len(death_registry)):

            name_match = (
                str(voter["name"]).strip().lower()
                == str(death_registry.iloc[j]["name"]).strip().lower()
            )

            dob_match = (
                str(voter["date_of_birth"])
                == str(death_registry.iloc[j]["date_of_birth"])
            )

            address_match = (
                str(voter["address"]).strip().lower()
                == str(death_registry.iloc[j]["address"]).strip().lower()
            )

            if name_match and dob_match and address_match:
                deceased = True
                break

        # Duplicate check
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

            phone_match = (
                voter["phone"] == other["phone"]
            )

            dob_match = (
                voter["date_of_birth"]
                == other["date_of_birth"]
            )

            if name_score >= 0.70 and (
                phone_match
                or (dob_match and address_score >= 0.70)
            ):
                duplicate = True
                break

        # EFRI score
        score = 0

        if duplicate:
            score += 40

        if already_voted:
            score += 30

        if deceased:
            score += 30

        # Risk level
        if score <= 30:
            risk = "Low Risk"
        elif score <= 60:
            risk = "Medium Risk"
        else:
            risk = "High Risk"

        # Reason
        reasons = []

        if duplicate:
            reasons.append("Duplicate evidence")

        if deceased:
            reasons.append("Deceased registry match")

        if already_voted:
            reasons.append("Already voted")

        if not reasons:
            reasons.append("No suspicious evidence")

        report.append({
            "voter_id": voter["voter_id"],
            "name": voter["name"],
            "constituency": voter["constituency"],
            "EFRI_score": score,
            "risk_level": risk,
            "duplicate_evidence": duplicate,
            "deceased_match": deceased,
            "already_voted": already_voted,
            "reason": ", ".join(reasons)
        })

    return report
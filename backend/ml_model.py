import pandas as pd
from difflib import SequenceMatcher
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib

# Load datasets
voters = pd.read_csv("dataset/cleaned_voters.csv")
death_registry = pd.read_csv("dataset/death_registry.csv")

# Make sure date formats match
voters["date_of_birth"] = pd.to_datetime(
    voters["date_of_birth"]
).dt.strftime("%Y-%m-%d")

death_registry["date_of_birth"] = pd.to_datetime(
    death_registry["date_of_birth"]
).dt.strftime("%Y-%m-%d")


def similarity(a, b):
    return SequenceMatcher(None, str(a), str(b)).ratio()


# Create features
voters["duplicate_evidence"] = 0
voters["deceased_match"] = 0
voters["already_voted"] = 0


# -------------------------------
# Already Voted
# -------------------------------
for i in range(len(voters)):

    if str(voters.iloc[i]["voting_status"]).strip().lower() == "yes":
        voters.loc[i, "already_voted"] = 1


# -------------------------------
# Deceased Detection
# -------------------------------
for i in range(len(voters)):

    for j in range(len(death_registry)):

        voter_name = str(voters.iloc[i]["name"]).strip().lower()
        death_name = str(death_registry.iloc[j]["name"]).strip().lower()

        voter_dob = str(voters.iloc[i]["date_of_birth"])
        death_dob = str(death_registry.iloc[j]["date_of_birth"])

        voter_address = str(voters.iloc[i]["address"]).strip().lower()
        death_address = str(death_registry.iloc[j]["address"]).strip().lower()

        if (
            voter_name == death_name
            and voter_dob == death_dob
            and voter_address == death_address
        ):
            voters.loc[i, "deceased_match"] = 1
            break


# -------------------------------
# Duplicate Detection
# -------------------------------
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
            voters.iloc[i]["phone"]
            == voters.iloc[j]["phone"]
        )

        dob_match = (
            voters.iloc[i]["date_of_birth"]
            == voters.iloc[j]["date_of_birth"]
        )

        if name_score >= 0.70 and (
            phone_match
            or (dob_match and address_score >= 0.70)
        ):
            voters.loc[i, "duplicate_evidence"] = 1
            voters.loc[j, "duplicate_evidence"] = 1


# -------------------------------
# EFRI
# -------------------------------
voters["EFRI_score"] = (
    voters["duplicate_evidence"] * 40
    + voters["already_voted"] * 30
    + voters["deceased_match"] * 30
)


def classify_risk(score):

    if score <= 30:
        return "Low Risk"

    elif score <= 60:
        return "Medium Risk"

    else:
        return "High Risk"


voters["risk_level"] = voters["EFRI_score"].apply(classify_risk)


print("===== ML FEATURE DATA =====")

print(
    voters[
        [
            "voter_id",
            "duplicate_evidence",
            "already_voted",
            "deceased_match",
            "EFRI_score",
            "risk_level"
        ]
    ]
)


# -------------------------------
# Decision Tree
# -------------------------------
X = voters[
    [
        "duplicate_evidence",
        "already_voted",
        "deceased_match"
    ]
]

y = voters["risk_level"]

model = DecisionTreeClassifier(random_state=42)

model.fit(X, y)
joblib.dump(model, "models/decision_tree.pkl")
print("Model saved successfully!")


print("\n===== DECISION TREE MODEL =====")
print("Model trained successfully!")

print("\nTraining Records:", len(voters))

print("\nRisk Distribution:")
print(voters["risk_level"].value_counts())

print("\nSample Predictions:")

predictions = model.predict(X)

for i in range(len(voters)):

    if voters.iloc[i]["EFRI_score"] > 0:

        print(
            voters.iloc[i]["voter_id"],
            "→",
            predictions[i]
        )
print("\n===== MODEL EVALUATION =====")

accuracy = accuracy_score(y, predictions)
precision = precision_score(y, predictions, average="weighted", zero_division=0)
recall = recall_score(y, predictions, average="weighted", zero_division=0)
f1 = f1_score(y, predictions, average="weighted", zero_division=0)

print("Accuracy:", round(accuracy, 2))
print("Precision:", round(precision, 2))
print("Recall:", round(recall, 2))
print("F1-Score:", round(f1, 2))

print("\nConfusion Matrix:")
print(confusion_matrix(y, predictions))
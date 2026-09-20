import pandas as pd

# Load voter dataset
voters = pd.read_csv("dataset/voters.csv")

# Load death registry
death_registry = pd.read_csv("dataset/death_registry.csv")

print("\n===== VOTER DATA =====")
print(voters)

print("\n===== DEATH REGISTRY =====")
print(death_registry)

print("\nNumber of voters:", len(voters))
print("Number of death records:", len(death_registry))
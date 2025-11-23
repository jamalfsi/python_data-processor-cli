import pandas as pd
import sys

if len(sys.argv) < 3:
    print("Usage: python my_cli.py show FILENAME")
    sys.exit()

action = sys.argv[1]
filename = sys.argv[2]

data = pd.read_csv(filename)


if action == "show":
    print(data.head())
elif action == "clean":
    data = data.dropna()
    print(data)
    data.to_csv("cleaned_"+filename, index=False)
    print("Saved cleaned_"+filename)
elif action == "stats":
    print(data.describe())
else:
    print("Unknown action:", action)

import pandas as pd  # Tell Python we will use pandas (helps with data)

filename = input("Enter the CSV filename: ")  # Ask the user for a file name

# Read the file and save it as 'data'
data = pd.read_csv(filename)

# Say how big the data is
print("Rows:", data.shape[0])
print("Columns:", data.shape[1])

print("Rows before cleaning:", len(data))
print("Missing values in each column:")
print(data.isnull().sum())

# Remove rows that have missing data
data = data.dropna()

print("Rows after cleaning:", len(data))

new_filename = "cleaned_" + filename
data.to_csv(new_filename, index=False)
print("Cleaned data saved to", new_filename)

print("Statistics for your data:")
print(data.describe())

col = input("Which column to filter? (type it): ")
num = float(input("Keep rows where value in this column is greater than: "))
filtered = data[data[col] > num]

print("Filtered rows:")
print(filtered)

col = input("Which column do you want to count? ")
counts = data[col].value_counts()
print("How many times each value appears:")
print(counts)

# Show the first 3 rows
print("Here are a few lines from your data:")
print(data.head(3))

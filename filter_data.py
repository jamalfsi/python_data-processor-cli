import pandas as pd  # Step 1. Import pandas so we can work with tables

data = pd.read_csv('sample_sales.csv')  # Step 2. Read the data from a CSV file

# Step 3. Filter: Only keep rows where the 'Sales' column is more than 500
filtered = data[data['Sales'] > 500]   # This makes a new table with only rows that match

print(filtered)      # Step 4. Show the filtered table
print("Number of rows after filtering:", len(filtered))  # Print how many rows we have now

# Step 2. Group by 'Region', and find average sales for each region
mean_by_region = data.groupby('Region')['Sales'].mean()  # This finds average sales per region

print("Avg sales per region is ", mean_by_region)   # Step 3. Print results

total_by_region = data.groupby('Region')['Sales'].sum()
print("Total sales per region is ",total_by_region)

count_by_region = data.groupby('Region').size()
print("Count per region is ",count_by_region)

import csv

# Read the CSV file
with open('output.csv', 'r', newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    header = next(csv_reader)  # Read the header row
    data = list(csv_reader)    # Read the remaining rows into a list

# Sort the data based on the risk/reward ratio (column index 12)
sorted_data = sorted(data[1:], key=lambda row: float(row[10]) if row[10] != 'Abstand' else float('inf'))

# Write the sorted data to a new CSV file
with open('sorted_output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(header)   # Write the header row
    csv_writer.writerows(sorted_data)   # Write the sorted rows

print('Sorted data written to sorted_output.csv')

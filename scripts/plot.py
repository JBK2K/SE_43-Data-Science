import matplotlib.pyplot as plt
import csv

# Read data from CSV file
abstand = []
hebel = []
risk_reward = []
wkn = []

with open('output.csv', 'r', newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        try:
            abstand.append(float(row[11]))      # Convert to float
            hebel.append(float(row[7]))         # Convert to float
            risk_reward.append(float(row[12]))  # Convert to float
            wkn.append(row[0])                  # Assuming 'WKN' is at index 0
        except ValueError:
            print("Error converting to float. Skipping row.")
            pass

# Print data types of abstand and hebel lists
print("Data types:")
print("Abstand:", type(abstand[0]))
print("Hebel:", type(hebel[0]))

# Plot
plt.figure(figsize=(10, 6))
scatter = plt.scatter(abstand, hebel, c=risk_reward, cmap='viridis', marker='o')

# Annotate points with WKN
for i, txt in enumerate(wkn):
    plt.annotate(txt, (abstand[i], hebel[i]), xytext=(5, -5), textcoords='offset points')

# Set labels and title
plt.xlabel('Distance in % to Strike Price')
plt.ylabel('Leverage x')
plt.title('Distance / Hebel for Derivatives (Color Encoded by Risk-Reward Ratio)')

# Set axis limits based on minimum and maximum values
plt.xlim(min(abstand), max(abstand))
plt.ylim(min(hebel), max(hebel))

# Add colorbar
plt.colorbar(scatter, label='Risk-Reward Ratio')

# Show plot
plt.grid(True)
plt.show()

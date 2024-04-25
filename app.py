import subprocess
import os

# Function to ask user whether to delete existing CSV files
def ask_delete_csv():
    response = input("Do you want to delete existing CSV files? (yes/no): ").lower()
    return response == 'yes'

# Main function to run the script
def main():
    # Ask user whether to delete existing CSV files
    delete_csv = ask_delete_csv()
    
    # If user wants to delete existing CSV files, delete them
    if delete_csv:
        csv_files = ["output.csv", "sorted_output.csv"]
        for file in csv_files:
            if os.path.exists(file):
                os.remove(file)
        print("Existing CSV files deleted.")
    else:
        print("Existing CSV files kept.")

    # Run scraper.py
    subprocess.run(["python3", "scripts/scraper.py"], check=True)

    # After scraper.py finishes, run sort.py and plot.py
    subprocess.run(["python3", "scripts/sort.py"])
    subprocess.run(["python3", "scripts/plot.py"])

# Run the main function
if __name__ == "__main__":
    main()

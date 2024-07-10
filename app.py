import subprocess
import os
import questionary

# Function to ask user whether to delete existing CSV files
def ask_delete_csv():
    response = questionary.confirm("Do you want to delete existing CSV files?").ask()
    return response

# Function to ask user whether to plot
def ask_plot():
    response = questionary.confirm("Do you want to plot the existing data?").ask()
    return response

def check_csv_has_data(csv_files):
    for file in csv_files:
        if os.path.exists(file):
            with open(file, "r") as f:
                if len(f.readlines()) > 1:
                    return True
    return False


# Main function to run the script
def main():
    # Ask user whether to plot existing data
    plot_data = ask_plot()
    if plot_data:
        # Check if CSV files have data
        if check_csv_has_data(["output.csv"]):
            # Run plot.py
            subprocess.run(["python3", "scripts/plot.py"])
        else:
            print("No data found in CSV files. Skipping plotting.")
            return
    
    # If user doesn't want to plot or if CSV files have no data, ask whether to delete existing CSV files
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

    # After scraper.py finishes, run sort.py
    subprocess.run(["python3", "scripts/sort.py"])
    subprocess.run(["python3", "scripts/plot.py"])

# Run the main function
if __name__ == "__main__":
    main()
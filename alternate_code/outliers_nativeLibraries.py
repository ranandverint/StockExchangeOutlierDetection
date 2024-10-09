import os
import csv
import random
import argparse
from datetime import datetime

# Function 1: Get 30 consecutive data points starting from a random timestamp
def get_random_30_data_points(file_path: str):
    try:
        # Read the CSV file manually
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            data = []
            
            for row in reader:
                # Parse date format and ensure valid data structure
                stock_id, timestamp, price = row[0], row[1], float(row[2])
                data.append({
                    "Stock-ID": stock_id,
                    "Timestamp": datetime.strptime(timestamp, "%d-%m-%Y"),
                    "Price": price
                })
            
            if len(data) < 30:
                raise ValueError(f"File {file_path} contains fewer than 30 data points.")
            
            # Randomly select 30 consecutive data points
            max_start = len(data) - 30
            random_start = random.randint(0, max_start)
            selected_data = data[random_start:random_start + 30]
            
            return selected_data
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return []

# Function 2: Detect outliers based on standard deviation
def detect_outliers(data):
    try:
        # Calculate the mean and standard deviation
        prices = [item['Price'] for item in data]
        mean_price = sum(prices) / len(prices)
        variance = sum((x - mean_price) ** 2 for x in prices) / len(prices)
        std_dev = variance ** 0.5

        # Outlier thresholds
        lower_threshold = mean_price - (2 * std_dev)
        upper_threshold = mean_price + (2 * std_dev)

        outliers = []
        for item in data:
            price = item['Price']
            deviation = price - mean_price
            percent_deviation = (deviation / mean_price) * 100

            if price < lower_threshold or price > upper_threshold:
                outliers.append({
                    "Stock-ID": item['Stock-ID'],
                    "Timestamp": item['Timestamp'].strftime("%d-%m-%Y"),
                    "Price": price,
                    "Mean": mean_price,
                    "Deviation": deviation,
                    "Percent_Deviation": percent_deviation,
                    "Threshold_Exceeded": "Above" if price > upper_threshold else "Below"
                })

        return outliers
    except Exception as e:
        print(f"Error detecting outliers: {e}")
        return []

# Function to save outliers to a CSV file
def save_outliers_to_csv(outliers, output_file):
    try:
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write headers
            writer.writerow(["Stock-ID", "Timestamp", "Price", "Mean", "Deviation", "Percent_Deviation", "Threshold_Exceeded"])

            # Write each outlier row
            for outlier in outliers:
                writer.writerow([
                    outlier["Stock-ID"], 
                    outlier["Timestamp"], 
                    outlier["Price"], 
                    outlier["Mean"], 
                    outlier["Deviation"], 
                    outlier["Percent_Deviation"], 
                    outlier["Threshold_Exceeded"]
                ])
        
        print(f"Outliers saved to {output_file}")
    except Exception as e:
        print(f"Error saving outliers to file {output_file}: {e}")

# Main processing function
def process_files(stock_exchange_folder: str, num_files: int):
    files = [f for f in os.listdir(stock_exchange_folder) if f.endswith('.csv')]
    files_to_process = files[:min(num_files, len(files))]

    if not files_to_process:
        print(f"No files to process in {stock_exchange_folder}")
        return

    for file in files_to_process:
        file_path = os.path.join(stock_exchange_folder, file)
        stock_id = file.split('.')[0]

        # Get random 30 data points
        data = get_random_30_data_points(file_path)
        if not data:
            continue

        # Detect outliers
        outliers = detect_outliers(data)
        if outliers:
            # Save outliers to CSV
            output_file = f"{stock_id}_outliers.csv"
            save_outliers_to_csv(outliers, output_file)
        else:
            print(f"No outliers found in {file}")

# Set up argument parsing
def parse_args():
    parser = argparse.ArgumentParser(description="Process stock exchange data for outliers.")
    parser.add_argument('stock_exchange_folder', type=str, help="Path to the stock exchange data folder")
    parser.add_argument('num_files', type=int, help="Number of files to process")
    return parser.parse_args()

# Usage
if __name__ == "__main__":
    args = parse_args()
    process_files(args.stock_exchange_folder, args.num_files)
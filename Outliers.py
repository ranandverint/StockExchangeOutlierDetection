import pandas as pd
import numpy as np
import os
import random
import argparse

# Function 1: Get 30 consecutive data points starting from a random timestamp
def get_random_30_data_points(file_path: str) -> pd.DataFrame:
    try:
        # Adjusting column names for the provided data format: Stock-ID, Timestamp, Price
        data = pd.read_csv(file_path, header=None, names=["Stock-ID", "Timestamp", "Price"], parse_dates=['Timestamp'], dayfirst=True)
        
        if len(data) < 30:
            raise ValueError(f"File {file_path} contains fewer than 30 data points.")
        
        # Ensure a random start timestamp that allows selecting 30 consecutive data points
        max_start = len(data) - 30
        random_start = random.randint(0, max_start)
        selected_data = data.iloc[random_start:random_start + 30].copy()

        return selected_data
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return pd.DataFrame()

# Function 2: Detect outliers based on standard deviation
def detect_outliers(data: pd.DataFrame, stock_id: str) -> pd.DataFrame:
    try:
        mean_price = data['Price'].mean()
        std_dev = data['Price'].std()

        # Define the outlier threshold (2 standard deviations beyond the mean)
        lower_threshold = mean_price - (2 * std_dev)
        upper_threshold = mean_price + (2 * std_dev)

        # Find outliers
        data['Mean'] = mean_price
        data['Deviation'] = data['Price'] - mean_price
        data['Percent_Deviation'] = (data['Deviation'] / mean_price) * 100
        outliers = data[(data['Price'] < lower_threshold) | (data['Price'] > upper_threshold)]

        # Add additional columns for clarity
        outliers['Threshold_Exceeded'] = outliers.apply(
            lambda row: "Above" if row['Price'] > upper_threshold else "Below", axis=1
        )

        # Format the Timestamp back to 'dd-mm-yyyy' before returning
        outliers['Timestamp'] = outliers['Timestamp'].dt.strftime('%d-%m-%Y')

        return outliers
    except Exception as e:
        print(f"Error detecting outliers: {e}")
        return pd.DataFrame()

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
        if data.empty:
            continue

        # Detect outliers
        outliers = detect_outliers(data, stock_id)
        if not outliers.empty:
            # Save outliers to CSV
            output_file = f"output_data/{stock_id}_outliers.csv"
            outliers.to_csv(output_file, index=False)
            print(f"Outliers saved to {output_file}")
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

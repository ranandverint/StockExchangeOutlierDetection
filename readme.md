# Stock Exchange Outlier Detection

This project processes stock exchange data to detect outliers based on stock prices. It uses a CSV file format for input and output and identifies outliers as data points that exceed 2 standard deviations from the mean of 30 consecutive data points, sampled randomly from the input.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [How to Run](#how-to-run)
4. [Docker based implementation](#docker-based-implementation)
5. [Assumptions](#assumptions)
6. [Error Handling](#error-handling)
7. [Additional Information](#additional-information)

## Prerequisites

To run this project, you need to have Python installed. The code has been tested with:
- **Python 3.9**

You also need to install the following Python libraries:
- **pandas**: `2.2.3`
- **numpy**: `2.0.2`

Ensure you have a terminal or command-line interface available to execute the script.

## Setup

Follow these steps to set up the environment and install necessary dependencies:

### 1. Clone the Repository or Download the Code
You can download the code as a ZIP file or clone it using:
```bash
git clone <repository-url>
```

### 2. Set Up a Virtual Environment (Optional but Recommended)

Create a virtual environment to isolate dependencies:
```bash
python3 -m venv env
source env/bin/activate   # On Windows, use `env\Scripts\activate`
```

### 3. Install Required Libraries
You need to install `pandas` and `numpy` to run the code. You can install these using the `requirements.txt` file or manually.

#### Installing using `requirements.txt`
If provided, run:
```bash
pip install -r requirements.txt
```

#### Installing Manually
You can install the required libraries by running:
```bash
pip install pandas==2.2.3 numpy==2.0.2
```

Verify the installation by running:
```bash
pip list
```

## How to Run

### Step 1: Organize Data Files

Ensure your input files are placed inside a folder. The input files should be CSV files containing stock price data, formatted as follows:

| Stock-ID | Timestamp    | Price    |
|----------|--------------|----------|
| FLTR     | 01-09-2023   | 16340.00 |
| FLTR     | 02-09-2023   | 16258.30 |
| ...      | ...          | ...      |

- **Stock-ID**: The stock ticker symbol.
- **Timestamp**: The date in `dd-mm-yyyy` format.
- **Price**: The stock price value.

### Step 2: Running the Script

This script takes 2 parameters as arguments. To execute the script, run the following command from the terminal:
```bash
python3 outliers.py <path_to_data_folder> <number_of_files_to_process>
```

Where:
- `<path_to_data_folder>`: The path to the folder containing your CSV stock files.
- `<number_of_files_to_process>`: Number of files you want to process (typically `1` or `2`).

### Example
```bash
python3 outliers.py ./stock_price_data_files/LSE/ 2
```

### Output:
For each processed CSV file, an output file will be generated in the `output_data\` directory, named as `<stock-id>_outliers.csv`. The output file will contain the following columns:

| Stock-ID | Timestamp    | Price    | Mean   | Deviation | Percent_Deviation | Threshold_Exceeded |
|----------|--------------|----------|--------|-----------|-------------------|--------------------|
| FLTR     | 03-09-2023   | 16274.56 | 16340  | -65.44    | -0.4%             | Below              |

- **Timestamp** in the output will be in `dd-mm-yyyy` format, matching the input format.


## Docker based implementation
The same script can be implemented using docker containers too. This helps in creating a container during runtime, execute the script inside the container & produce results & then the container is terminated.
I have added a `dockerfile` to achieve the same.

### How to run?
- Build the custom image:
  ```bash
  docker build -t stock-exchange-outlier-detection .
  ```
- Run the container:
  ```bash
  docker run -v $(pwd)/stock_price_data_files/NYSE:/app/input_data -v $(pwd)/output_data:/app/output_data stock-exchange-outlier-detection 
  ```
  Note: Replace the `NYSE` with the stock-id that you want to detect outlier from. Here `-v` flag will mount persistent volume to the container & inturn, it will be able to read the input data as well as write the output data to your local volume & the data won't be lost after the container is terminated.

### Additional work
I have compiled an image and uploaded on dockerhub (as mentioned in the challenge document).
Use the below command to pull my docker image to your local machine and execute the script:

- Step 1: Pull the docker image:
  ```bash
  docker pull ranand5855/outlier-detection:v1.0
  ```
- Step 2: Run the container:
  ```bash
  docker run -v $(pwd)/stock_price_data_files/<stock-id>:/app/input_data -v $(pwd)/output_data:/app/output_data ranand5855/outlier-detection:v1.0
  ```
  Replace the `<stock-id>` with the stock id of your interest, here it can be one of these:
  - LSE
  - NASDAQ
  - NYSE

## Assumptions

- The input zip file has been extracted & the content renamed to make it simpler and added to the root of this repository.
- Multiple types of representation of the same code has been implemented, you can find other versions of this code in the directory `alternate_code\`
  - Version of code with inline arguments
  - Version of code using native python libraries (without using pandas & numpy)
 
- The input CSV files are well-formed with three columns: `Stock-ID`, `Timestamp`, and `Price`.
- The `Timestamp` is provided in the format `dd-mm-yyyy`.
- If a file contains fewer than 30 data points, it will raise an error and skip processing for that file.
- The number of files to process is capped by the number of available files in the folder. If fewer files are available than requested, it processes the available files.

## Error Handling

The application is designed to handle a variety of errors:
- **Empty or Missing Files**: If a file is empty or missing, it will skip that file and continue with the next one.
- **Invalid CSV Format**: The program assumes the CSV format is valid; any file with incorrect formatting will be skipped, and an error message will be displayed.
- **Insufficient Data Points**: If a file contains fewer than 30 data points, it will raise a `ValueError` and skip the file.
- **File Not Found**: If the specified directory or file is not found, it will handle this gracefully with a printed error message.

## Additional Information

- **Performance**: The script is optimized for processing multiple files with minimal memory overhead. However, it processes one file at a time.
- **Scalability**: The script can easily be extended to handle additional stock exchanges by modifying the input and the number of files to process.
- I have taken help from AI to generate this README & then edited on top of it.

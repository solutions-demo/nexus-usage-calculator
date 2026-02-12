# nexus-usage-calculator
Calculate data transfer based on logs

This Python script extracts request data from your Nexus logs and generates a summary as a CSV file.  The script provides the information noted below, where the data is cited by name:
- File name
- Total bytes sent
- Total bytes received
- GET bytes sent
- POST bytes sent
- PUT bytes sent
- DELETE bytes sent
- Total Duration

The results are summarized as gigabytes (GB).

## What this script processes
- **Parses log files**: Processes `.log` files in the specified directory.
- **Calculates total bytes sent**: For each log file, the script calculates the total bytes sent based on the log entries.
- **Generates CSV output**: The script writes the total bytes sent for each file and the total bytes sent across all files to a CSV file.
- **Customizable log format**: The regex pattern can be adjusted to accommodate different log formats.
- **Progress Tracking**: Displays progress bars for both file processing and line-by-line processing using `tqdm`

## Prerequisites
- Python 3.x installed. If not, download it from [here](https://www.python.org/downloads/).
- Recommended: use a python virtual environment.
- Required Python libraries:
    - `re` (for regex matching)
    - `csv` (for writing to CSV)
    - `os` (for directory file handling)
    - `math` (for data conversions)
    - `datetime` (for timestamp handling)
    - `tqdm` (for displaying progress bars) — Install via `pip install tqdm`
    - See also: requirements.txt
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Place your `.log` files in a directory (e.g., `logs_directory`).
2. Edit the script to point to the correct input directory if you wish to specify a different directory or output file:
    - Set the variable `input_directory` to the path where your `.log` files are stored.
    - Set the variable `output_csv_file` to the desired name and location for the CSV output.
3. Run the script:

```bash
   python3 usagecalc.py
```

## Log Format

The output contains the following:

```
%clientHost %l %user [%date] "%requestURL" %statusCode %bytesSent %bytesReceived %elapsedTime "%header{User-Agent}"
```


## Example CSV Output:

The output looks like the following:

```
File,Total Bytes Sent,Total Bytes Received,GET Bytes Sent,POST Bytes Sent,PUT Bytes Sent,DELETE Bytes Sent,Total Duration
sample-request.log,0,20971,0,0,0,0,0d/1hr/0m/0s
sample-request2.log,3712,77,0,3712,0,0,0d/0hr/0m/0s

Total Bytes Sent Across All Files (Bytes),3712,21048,0,3712,0,0,5d/1hr/4m/0s
Total Bytes Sent Across All Files (GBs),1 GB,1 GB,0 GB,1 GB,0 GB,0 GB,5d/1hr/4m/0s
```

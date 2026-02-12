import re
import csv
import os
import math
from datetime import datetime
from tqdm import tqdm

# Adjusted log format regex pattern (added bytesReceived)
log_pattern = re.compile(
    r'^(?P<clientHost>\S+) '              # clientHost (IP or hostname)
    r'- (?P<user>\S+) '                   # user (could be '-' or actual username)
    r'\[(?P<date>[^]]+)\] '               # date in [day/month/year:hour:minute:second timezone] format
    r'"(?P<requestMethod>\S+) '           # HTTP request method (GET, POST, PUT, DELETE, etc.)
    r'(?P<requestURL>[^"]+)" '            # request URL
    r'(?P<statusCode>\d{3}) '             # status code (3 digits)
    r'(?P<bytesSent>\d+|-) '              # bytes sent (can be '-')
    r'(?P<bytesReceived>\d+|-) '          # bytes received (can be '-')
    r'(?P<elapsedTime>\d+|-) '            # elapsed time (can be '-')
    r'"(?P<userAgent>[^"]+)" '            # User-Agent (in quotes)
    r'\[(?P<threadID>[^\]]+)\]'           # Thread ID in square brackets
)

# Input directory and output file path
input_directory = 'logs_directory'
output_csv_file = 'output.csv'

# Ensure directory exists
if not os.path.exists(input_directory):
    print(f"Error: Directory '{input_directory}' does not exist.")
    exit(1)

# Initialize total accumulators
total_bytes_sent = 0
total_bytes_received = 0
method_totals = {"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0}
timestamps = []
all_data = []

# Get a list of log files
log_files = [f for f in os.listdir(input_directory) if f.endswith('.log')]

# Progress bar for files
for filename in tqdm(log_files, desc="Processing files", unit="file"):
    file_total_bytes_sent = 0
    file_total_bytes_received = 0
    file_method_totals = {"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0}
    file_timestamps = []

    with open(os.path.join(input_directory, filename), 'r') as infile:
        # Progress bar for lines in the current file
        for line in tqdm(infile, desc=f"Processing {filename}", unit="line", leave=False):
            match = log_pattern.match(line)
            if match:
                data = match.groupdict()

                # Convert values, handling `-`
                bytes_sent = int(data['bytesSent']) if data['bytesSent'] != '-' else 0
                bytes_received = int(data['bytesReceived']) if data['bytesReceived'] != '-' else 0
                elapsed_time = int(data['elapsedTime']) if data['elapsedTime'] != '-' else 0

                request_method = data['requestMethod']
                timestamp_str = data['date']

                # Convert timestamp to datetime object
                timestamp = datetime.strptime(timestamp_str.split()[0], "%d/%b/%Y:%H:%M:%S")
                file_timestamps.append(timestamp)

                # Accumulate bytes
                file_total_bytes_sent += bytes_sent
                file_total_bytes_received += bytes_received
                if request_method in file_method_totals:
                    file_method_totals[request_method] += bytes_sent

    # Calculate duration (in seconds)
    file_duration_seconds = (max(file_timestamps) - min(file_timestamps)).total_seconds() if file_timestamps else 0

    # Convert duration in seconds to readable format
    def format_duration(seconds):
        days = int(seconds // (24 * 3600))
        hours = int((seconds % (24 * 3600)) // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{days}d/{hours}hr/{minutes}m/{seconds}s"

    file_duration = format_duration(file_duration_seconds)

    # Store file data for later writing
    all_data.append([filename, file_total_bytes_sent, file_total_bytes_received, file_method_totals["GET"],
                     file_method_totals["POST"], file_method_totals["PUT"], file_method_totals["DELETE"], file_duration])

    # Update total values
    total_bytes_sent += file_total_bytes_sent
    total_bytes_received += file_total_bytes_received
    for method in method_totals:
        method_totals[method] += file_method_totals[method]
    timestamps.extend(file_timestamps)

# Calculate overall duration (in seconds) for all logs
total_duration_seconds = (max(timestamps) - min(timestamps)).total_seconds() if timestamps else 0
total_duration = format_duration(total_duration_seconds)

# Write data to CSV
with open(output_csv_file, 'w', newline='') as outfile:
    csv_writer = csv.writer(outfile)

    # Write headers
    csv_writer.writerow(["File", "Total Bytes Sent", "Total Bytes Received", "GET Bytes Sent", "POST Bytes Sent", "PUT Bytes Sent", "DELETE Bytes Sent", "Total Duration"])

    # Write all collected data
    csv_writer.writerows(all_data)

    # Write total summary
    csv_writer.writerow([])
    csv_writer.writerow(["Total Bytes Sent Across All Files (Bytes)", total_bytes_sent, total_bytes_received, method_totals["GET"], method_totals["POST"], method_totals["PUT"], method_totals["DELETE"], total_duration])
    csv_writer.writerow(["Total Bytes Sent Across All Files (GBs)",
                         f"{math.ceil(total_bytes_sent / (1024**3))} GB",
                         f"{math.ceil(total_bytes_received / (1024**3))} GB",
                         f"{math.ceil(method_totals['GET'] / (1024**3))} GB",
                         f"{math.ceil(method_totals['POST'] / (1024**3))} GB",
                         f"{math.ceil(method_totals['PUT'] / (1024**3))} GB",
                         f"{math.ceil(method_totals['DELETE'] / (1024**3))} GB",
                         total_duration])

print("Log analysis completed. Output saved to CSV successfully!")

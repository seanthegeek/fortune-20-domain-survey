#!/usr/bin/env python3

import datetime
import os
import subprocess
import csv

combined_result_rows = []

date = datetime.datetime.today().strftime('%Y-%m-%d')
results_dir = os.path.join("results", date)
os.makedirs(results_dir, exist_ok=True)
domain_lists = [f for f in os.listdir("domains") if
                os.path.isfile(os.path.join("domains", f)) and
                f.endswith(".txt")]
for filename in sorted(domain_lists):
    input_path = os.path.join("domains", filename)
    with open(input_path) as input_file:
        sorted_lines = sorted(list(set(input_file.readlines())))
    with open(input_path, "w") as input_file:
        input_file.writelines(sorted_lines)
    symbol = filename.rstrip("-domains.txt")
    symbol_dir = os.path.join(results_dir, symbol)
    os.makedirs(symbol_dir, exist_ok=True)
    print(f"Checking {symbol}...")
    output_filename = os.path.join(symbol_dir, f"{date}_{symbol}_checkdmarc")
    subprocess.run(["checkdmarc", "--skip-tls", "-t", "5", input_path,
                   "-o", f"{output_filename}.csv", f"{output_filename}.json"])
    with (open(f"{output_filename}.csv")) as results_csv:
        reader = csv.DictReader(results_csv)
        csv_fields = reader.fieldnames
        for row in reader:
            combined_result_rows.append(row)
combined_result_rows = sorted(combined_result_rows, key= lambda x: x["domain"])
combined_filename = f"{date}_fortune-20-combined_checkdmarc.csv"
with open(os.path.join(results_dir, combined_filename), "w") as combined_csv_file:
    writer = csv.DictWriter(combined_csv_file, csv_fields)
    writer.writeheader()
    writer.writerows(combined_result_rows)

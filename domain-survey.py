#!/usr/bin/env python3

import datetime
import os
import subprocess
import csv
import json

from checkdmarc import get_base_domain

combined_result_rows = []
combined_stats = dict(dnssec=dict(true=0, false=0),
                             valid_spf_record=dict(true=0, false=0),
                             dmarc_policy=(dict(missing_or_invalid=0,
                                                       none=0,
                                                       quarantine=0,
                                                       reject=0)),
                                                       mx=dict(no_mx=0),
                                                       dmarc_rua=dict(
                                                           no_rua=0
                                                       ))

date = datetime.datetime.utcnow().strftime('%Y-%m-%d')
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
    subprocess.run(["checkdmarc", "--skip-tls", input_path,
                   "-o", f"{output_filename}.csv", f"{output_filename}.json",
                    "-t", "10", "-n", "1.1.1.1", "1.0.0.1"])
    with (open(f"{output_filename}.csv")) as results_csv:
        reader = csv.DictReader(results_csv)
        csv_fields = list(reader.fieldnames)
        csv_fields.insert(1, "owner")
        for row in reader:
            row["owner"] = symbol
            combined_result_rows.append(row)
            combined_stats["dnssec"][row["dnssec"].lower()] += 1
            combined_stats["valid_spf_record"][row["spf_valid"].lower()] += 1
            if row["dmarc_p"] == "":
                combined_stats["dmarc_policy"]["missing_or_invalid"] += 1
            else:
                combined_stats["dmarc_policy"][row["dmarc_p"]] += 1
            if row["mx"] == "":
                combined_stats["mx"]["no_mx"] += 1
            else:
                mx = get_base_domain(row["mx"].split("|")[0].split(" ")[-1])
                if mx in combined_stats["mx"]:
                    combined_stats["mx"][mx] += 1
                else:
                    combined_stats["mx"][mx] = 1
            if row["dmarc_rua"] == "":
                combined_stats["dmarc_rua"]["no_rua"] += 1
            else:
                rua_addresses = row["dmarc_rua"].split("|")
                rua_domains = list(set(map(lambda x: get_base_domain(
                    x.split("@")[-1].lower()), rua_addresses)))
                for domain in rua_domains:
                    if domain not in combined_stats["dmarc_rua"]:
                        combined_stats["dmarc_rua"][domain] = 1
                    else:
                        combined_stats["dmarc_rua"][domain] += 1
combined_stats["dnssec"] = dict(sorted(combined_stats["dnssec"].items(), 
                                       key=lambda x: x[1], reverse=True))
combined_stats["valid_spf_record"] = dict(sorted(
    combined_stats["valid_spf_record"].items(), key=lambda x: x[1],
    reverse=True))
combined_stats["mx"] = dict(sorted(combined_stats["mx"].items(),
                               key=lambda x: x[1], reverse=True))
combined_stats["dmarc_policy"] = dict(sorted(
    combined_stats["dmarc_policy"].items(),
    key=lambda x: x[1], reverse=True))
combined_stats["dmarc_rua"] = dict(sorted(combined_stats["dmarc_rua"].items(),
                               key=lambda x: x[1], reverse=True))
combined_result_rows = sorted(combined_result_rows, key=lambda x: x["domain"])
combined_filename = f"{date}_fortune-20-aggregate_checkdmarc"
combined_results_path = os.path.join(results_dir, combined_filename)
with open(f"{combined_results_path}.csv", "w") as combined_csv_file:
    writer = csv.DictWriter(combined_csv_file, csv_fields)
    writer.writeheader()
    writer.writerows(combined_result_rows)
with open(f"{combined_results_path}_stats.json", "w") as combined_stats_file:
    combined_stats_file.write(json.dumps(combined_stats, indent=2))
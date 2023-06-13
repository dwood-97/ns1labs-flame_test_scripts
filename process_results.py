import os
import json

def process_results(tests_directory):
    avg_recv_values = []

    for root, dirs, files in os.walk(tests_directory):
        for filename in files:
            if filename == "flame_results.json":
                file_path = os.path.join(root, filename)
                with open(file_path, "r") as file:
                    results = json.load(file)
                    avg_recv_values.extend(results["avg_recv"])

    if avg_recv_values:
        average = sum(avg_recv_values) / len(avg_recv_values)
    else:
        average = 0.0

    output_file = os.path.join(tests_directory, "avg_recv_results.txt")
    with open(output_file, "w") as file:
        file.write(f"Average of all data: {average}\n")
        file.write("\n")
        for i, avg_recv in enumerate(avg_recv_values, start=1):
            file.write(f"{i}) {avg_recv}\n")

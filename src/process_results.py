import os
import json

def process_results(tests_directory, num_tests, l_value, Q_value, command):
    avg_recv_values = []
    for root, dirs, files in os.walk(tests_directory):
        for filename in files:
            if filename == "flame_results.json":
                file_path = os.path.join(root, filename)
                with open(file_path, "r") as file:
                    results = json.load(file)
                    avg_recv = results.get("avg_recv")
                    if isinstance(avg_recv, list) and len(avg_recv) > 0:
                        test_average = sum(avg_recv) / len(avg_recv)
                        avg_recv_values.append(test_average)

    if avg_recv_values:
        overall_average = sum(avg_recv_values) / len(avg_recv_values)
    else:
        overall_average = 0.0

    print(f"\nAverage of all data: {overall_average}")
    print ("----------------------------------------------------------------")

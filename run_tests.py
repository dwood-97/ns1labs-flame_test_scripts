import os
import json
from datetime import datetime
from constants import BASE_DIRECTORY, PATTERN

def run_tests(num_tests):
    # Prompt the user for the -l and -Q values
    l_value = input("Please enter the maximum duration (in seconds) for traffic generation. Enter 0 for unlimited duration: ")
    Q_value = input("Please enter the maximum queries per second (QPS) for traffic generation. Enter 0 for no rate limit: ")

    current_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    tests_directory = os.path.join(BASE_DIRECTORY, "test_results", current_date)
    os.makedirs(tests_directory)

    results = {"avg_send": [], "avg_recv": []}

    for i in range(1, num_tests + 1):
        test_directory = os.path.join(tests_directory, str(i))
        os.makedirs(test_directory)
        os.chdir(test_directory)

        # Use the user-provided values in the command
        command = f"docker run ns1labs/flame -l {l_value} -Q {Q_value} 10.244.160.173"
        output = os.popen(command).read()

        with open("flame_output.txt", "w") as output_file:
            output_file.write(output)

        for line in output.splitlines():
            match = PATTERN.search(line)
            if match:
                results["avg_send"].append(int(match.group(1)))
                results["avg_recv"].append(int(match.group(2)))

        with open("flame_results.json", "w") as results_file:
            results_file.write(json.dumps(results, indent=4))

    return tests_directory

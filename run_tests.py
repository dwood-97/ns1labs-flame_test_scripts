import os
import json
import time
from datetime import datetime
from constants import BASE_DIRECTORY, PATTERN
from rich.progress import Progress

def run_tests(num_tests):
    l_value = input("Please enter the maximum duration (in seconds) for traffic generation (default is 10): ") or "10"
    Q_value = input("Please enter the maximum queries per second (QPS) for traffic generation (default is 20000): ") or "20000"

    total_time_sec = num_tests * int(l_value)
    total_time_sec += round(total_time_sec * 0.2)  # Add 20% buffer time

    total_time_min = total_time_sec // 60
    remaining_sec = total_time_sec % 60

    total_time_str = f"{total_time_min} minute{'s' if total_time_min != 1 else ''}"
    if remaining_sec > 0:
        total_time_str += f" {remaining_sec} second{'s' if remaining_sec != 1 else ''}"

    print(f"Running {num_tests} tests. This will take approximately {total_time_str}. Please wait...")

    current_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    tests_directory = os.path.join(BASE_DIRECTORY, "test_results", current_date)
    os.makedirs(tests_directory)

    results = {"avg_send": [], "avg_recv": []}
    command = None  # Initialize the command variable

    start_time = time.time()  # Start timer

    with Progress() as progress:
        task1 = progress.add_task("[cyan]Working...", total=num_tests)

        for i in range(1, num_tests + 1):
            test_directory = os.path.join(tests_directory, str(i))
            os.makedirs(test_directory)
            os.chdir(test_directory)

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
            
            progress.update(task1, advance=1)

    end_time = time.time()  # End timer

    # Calculate actual total time
    actual_total_time_sec = end_time - start_time

    # Convert total time to hours, minutes, and seconds
    actual_total_time_hour = actual_total_time_sec // 3600
    actual_total_time_min = (actual_total_time_sec % 3600) // 60
    remaining_sec = round(actual_total_time_sec % 60, 2)

    time_str = ""
    if actual_total_time_hour > 0:
        time_str += f"{actual_total_time_hour} hours "
    if actual_total_time_min > 0:
        time_str += f"{actual_total_time_min} minutes "
    if remaining_sec > 0:
        time_str += f"{remaining_sec} seconds"

    print(f"The tests took a total of {time_str} to complete.")

    return tests_directory, l_value, Q_value, command

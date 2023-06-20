import os
import json
import time
import argparse
import configparser
import ipaddress
from datetime import datetime
from constants import BASE_DIRECTORY, PATTERN
from rich.progress import Progress


def validate_num(num_str):
    return num_str.isdigit() and int(num_str) > 0


def validate_ip(ip_str):
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False


def run_tests(num_tests):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--MaxDuration",
        type=int,
        help="Maximum duration (in seconds) for traffic generation.",
    )
    parser.add_argument(
        "--MaxQPS",
        type=int,
        help="Maximum queries per second (QPS) for traffic generation.",
    )
    parser.add_argument(
        "--IPAddress",
        type=str,
        help="IP address that you would like to send queries to.",
    )
    args = parser.parse_args()
    config = configparser.ConfigParser()

    config_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "..", "config", "config.ini"
    )
    if not os.path.exists(config_path):
        print(
            "Warning: config.ini not found. Using default settings and/or command line arguments."
        )
    else:
        try:
            config.read(config_path)
        except configparser.Error as e:
            print(
                f"Warning: Failed to parse config.ini: {e}. Using default settings and/or command line arguments."
            )

    l_value = args.MaxDuration or config.get("Required", "MaxDuration")
    Q_value = args.MaxQPS or config.get("Required", "MaxQPS")
    ip_address = args.IPAddress or config.get("Required", "IPAddress")
    optional_flags = {
        key: config.get("Optional", key) for key in config.options("Optional")
    }

    if not validate_ip(ip_address):
        print(
            "The provided IP address is not valid. Please provide a valid IP address."
        )
        return

    total_time_sec = num_tests * int(l_value)
    total_time_sec += round(total_time_sec * 0.3)  # Add 30% buffer time

    total_time_min = total_time_sec // 60
    remaining_sec = total_time_sec % 60

    total_time_str = f"{total_time_min} minute{'s' if total_time_min != 1 else ''}"
    if remaining_sec > 0:
        total_time_str += f" {remaining_sec} second{'s' if remaining_sec != 1 else ''}"

    print ("\n----------------------------------------------------------------")
    print(
        f"Running {num_tests} tests. This will take approximately {total_time_str}. Please wait...\n"
    )

    current_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    tests_directory = os.path.join(BASE_DIRECTORY, "../data/test_results", current_date)
    os.makedirs(tests_directory, exist_ok=True)

    results = {"avg_send": [], "avg_recv": []}
    command = None  # Initialize the command variable

    start_time = time.time()  # Start timer

    with Progress() as progress:
        task1 = progress.add_task("[cyan]Working...", total=num_tests)

        for i in range(1, num_tests + 1):
            test_directory = os.path.join(tests_directory, str(i))
            os.makedirs(test_directory, exist_ok=True)
            os.chdir(test_directory)

            command = f"docker run ns1labs/flame -l {l_value} -Q {Q_value} {ip_address}"
            output = os.popen(command).read()

            for flag, value in optional_flags.items():
                if value:
                    command += f" -{flag} {value}"

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


if __name__ == "__main__":
    run_tests(6)  # default number of tests

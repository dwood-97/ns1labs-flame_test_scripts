# Flame Test Scripts

This repository contains a set of Python scripts to conduct and analyze DNS stress tests using the Flamethrower tool. These scripts are designed to interact with the Flamethrower tool packaged as a Docker image (ns1labs/flame). The key scripts in the repository include main.py, run_tests.py, process_results.py, and constants.py.

## Getting Started

### Prerequisites

    - Python 3.7 or higher
    - Docker
    - Access to a functioning DNS server for testing

### Installation

    1. Clone the repository to your local machine using git clone.
    2. Navigate into the cloned directory with cd ns1labs-flame_test_scripts.
    3. Install required Python packages using pip install -r requirements.txt.

## Usage

To begin the testing process, run the main script with python src/main.py. By default, the script will ask for the number of tests you wish to perform.

The script will then perform the indicated number of tests. By default, each test has a maximum duration of 10 seconds and a maximum number of queries per second (QPS) of 20,000. The tests are conducted against an IP address which is either set in config.ini or entered when prompted.

These default parameters can be overridden using a config.ini file or by providing command-line arguments.

## Configuration File

The config.ini file allows you to specify your preferred settings for maximum duration, maximum QPS, and IP address. The file should be structured as follows:

```init
[Required]
IPAddress = <Your Desired IP>
MaxDuration = 10
MaxQPS = 20000

[Optional]
# Populate as per your requirements. If left blank, default values will be used.
BIND_IP = 
QCOUNT = 
TCOUNT = 
PORT = 
DELAY_MS = 
RECORD = 
QTYPE = 
FILE = 
LIMIT_SECS = 
TIMEOUT = 
FAMILY = 
PROTOCOL = 
HTTPMETHOD = 
QPS = 
GENERATOR = 
VERBOSITY = 
CLASS = 
qps_flow = 
targets = 
dnssec = false
RANDOMIZE = false
```

The script will use these values unless they are overridden by command-line arguments.

## Command-Line Arguments

To override the settings in the configuration file or the default values, provide command-line arguments with the following syntax:

```init
python src/run_tests.py --MaxDuration 15 --MaxQPS 25000 --IPAddress 192.168.1.1
```

## Result Processing

The process_results.py script processes the results of the tests and writes a summary to a file named avg_recv_results.txt. This file is stored in the directory created for that particular testing session within the /data/test_results folder.

The summary includes:

    - Number of tests run
    - Maximum duration
    - Maximum QPS
    - Command used to run the tests
    - Average of all received queries across tests

For each individual test, the average received queries are also reported.

Lastly, the script process_test_results_directory.py generates a grand average of all tests performed, recorded in total_test_averages.txt.

This suite of scripts provides a comprehensive tool for conducting and analyzing DNS stress tests.
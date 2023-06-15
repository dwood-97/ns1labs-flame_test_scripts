```
# Flame Test Scripts

This repository contains a set of Python scripts for running and analyzing DNS stress tests using the Flamethrower tool (packaged as `ns1labs/flame` Docker image). The main scripts in this repository are `main.py`, `run_tests.py`, `process_results.py`, and `constants.py`.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Docker
- Access to a running DNS server that can be tested

### Installation

1. Clone the repository to your local machine using `git clone`.
2. Navigate into the directory using `cd ns1labs-flame_test_scripts`.

## Usage

Run the main script using `python main.py`. By default, it will prompt for the number of tests to run. The script will then run the specified number of tests, each with a default maximum duration of 10 seconds and a default maximum queries per second (QPS) of 20,000. The tests are run against a default IP address of 10.244.160.173.

To customize these values, you can either use a `config.ini` file or provide command-line arguments.

### Configuration File

You can use a `config.ini` file to set your preferences for the maximum duration, maximum QPS, and IP address. The file should be structured as follows:

```ini
[Settings]
MaxDuration = 10
MaxQPS = 20000
IPAddress = 10.244.160.173
```

The script will use these values unless overridden by command-line arguments.

### Command-Line Arguments

You can also provide command-line arguments to override the settings in the configuration file or the default values. Use the following syntax:

```shell
python run_tests.py --MaxDuration 15 --MaxQPS 25000 --IPAddress 192.168.1.1
```

### Result Processing

The `process_results.py` script processes the results of the tests and writes a summary to a file named `avg_recv_results.txt`. This includes the number of tests, the maximum duration, the maximum QPS, the command used to run the tests, and the average number of received queries. It also includes a list of the average number of received queries from each test.

This is a basic `README.md` file and should cover most of the information users need to understand and use your scripts. You might want to add more details depending on your specific needs, such as information about the repository's structure, how to contribute, license information, etc.
```

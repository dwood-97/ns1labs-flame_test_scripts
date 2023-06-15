from run_tests import run_tests, validate_num
from process_results import process_results


def validate_input(prompt, default_value, validation_func):
    while True:
        value = input(prompt) or default_value
        if validation_func(value):
            return int(value)
        else:
            print("Invalid input. Please try again.")


def main():
    num_tests = validate_input(
        "Please enter the desired number of tests to perform (default is 6): ",
        "6",
        validate_num,
    )
    tests_directory, l_value, Q_value, command = run_tests(num_tests)
    process_results(tests_directory, num_tests, l_value, Q_value, command)


if __name__ == "__main__":
    main()

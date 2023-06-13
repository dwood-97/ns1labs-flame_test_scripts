from run_tests import run_tests
from process_results import process_results

num_tests = int(input("Please enter the desired number of tests to perform: "))
tests_directory = run_tests(num_tests)
process_results(tests_directory)

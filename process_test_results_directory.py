import os

def calculate_total_average():
    test_results_directory = "/home/operations/ns1labs-flame_test_scripts/test_results"
    total_values = []

    # Iterate over all directories in test_results
    for test_directory in os.listdir(test_results_directory):
        avg_recv_results_file = os.path.join(test_results_directory, test_directory, "avg_recv_results.txt")
        
        # Check if avg_recv_results.txt file exists
        if os.path.exists(avg_recv_results_file):
            with open(avg_recv_results_file, "r") as file:
                lines = file.readlines()
                
                # The first line of the file contains the average
                # "Average of all data: {average}\n"
                average_line = lines[0]
                # Split the line on ": " and take the second part, then remove the newline character and convert to float
                average = float(average_line.split(": ")[1].strip())
                total_values.append(average)

    # Calculate the total average
    if total_values:
        total_average = sum(total_values) / len(total_values)
    else:
        total_average = 0.0

    # Write or update total_test_averages.txt with the new average
    total_averages_file = os.path.join(test_results_directory, "total_test_averages.txt")
    with open(total_averages_file, "w") as file:
        file.write(f"Total average of all tests: {total_average}\n")

# Call the function
calculate_total_average()

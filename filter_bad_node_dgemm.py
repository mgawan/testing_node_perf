import os
import re
import sys

# Define the threshold for Best performance
threshold = 19000 * 0.93  # 7% less than 1363787

# Function to extract all Best performance values from a file
def extract_triad_performance(file_path):
    triad_values = []
    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("Best"):
                # Extract the performance value (Gflop/s)
                match = re.search(r"Best\s+\(\d+\)\s+([\d.]+)\s+([\d.]+)", line)
                if match:
                    triad_values.append(float(match.group(2)))
    return triad_values

# Check if the input directory is provided
if len(sys.argv) != 2:
    print("Usage: python test_script.py <input_directory>")
    sys.exit(1)

# Directory containing the output files
output_dir = sys.argv[1]

# Iterate over all files in the directory
low_performance_nodes = []
for file_name in os.listdir(output_dir):
    if file_name.endswith("_.out"):  # Process only files ending with "_.out"
        node_id = file_name.split("_")[0]  # Extract node ID from file name
        file_path = os.path.join(output_dir, file_name)
        triad_performance_values = extract_triad_performance(file_path)

        if triad_performance_values:
            print(f"Node: {node_id}, Best Performances: {', '.join(f'{v:.2f}' for v in triad_performance_values)} Gflop/s")
            if any(value < threshold for value in triad_performance_values):
                low_performance_nodes.append((node_id, triad_performance_values))

# Report nodes with low Best performance
if low_performance_nodes:
    print("Nodes with at least one Best performance value below 93% of 1363787:")
    for node_id, performances in low_performance_nodes:
        print(f"Node: {node_id}, Best Performances: {', '.join(f'{v:.2f}' for v in performances)} Gflop/s")
else:
    print("All nodes meet the Best performance threshold.")

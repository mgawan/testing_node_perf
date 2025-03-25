import os
import re
import sys

# Define the threshold for Triad performance
threshold = 1363787 * 1.0  # 7% less than 1363787

# Function to extract Triad performance from a file
def extract_triad_performance(file_path):
    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("Triad"):
                # Extract the performance value (MBytes/sec)
                match = re.search(r"Triad\s+([\d.]+)", line)
                if match:
                    return float(match.group(1))
    return None

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
        triad_performance = extract_triad_performance(file_path)
        
        if triad_performance is not None:
            if triad_performance < threshold:
                low_performance_nodes.append((node_id, triad_performance))

# Report nodes with low Triad performance
if low_performance_nodes:
    print("Nodes with Triad performance below 93% of 1363787:")
    for node_id, performance in low_performance_nodes:
        print(f"Node: {node_id}, Triad Performance: {performance:.2f} MBytes/sec")
else:
    print("All nodes meet the Triad performance threshold.")
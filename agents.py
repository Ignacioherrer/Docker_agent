# agents.py

# Importing the necessary libraries
import os
import csv
import anthropic
from prompts import *

# Set up the Anthropic API key
if not os.getenv("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = input("Please enter your Anthropic API key: ") # Prompt the user to enter API key

# Create the Anthropic client
client = anthropic.Anthropic()
sonnet = "claude-3-5-sonnet-20240620"

# Function to read the CSV file from the User
def read_csv(file_path):
    data = []
    with open(file_path, "r", newline="") as csvfile: # Open the CSV fie in read mode
        csv_reader = csv.reader(csvfile) # Create a CSV reader object
        for row in csv_reader:
            data.append(row)  # Add each row to the data list
        return data
    
# Function to save the generated data to a new CSV file
def save_to_csv(data, output_file, headers=None):
    mode = "w" if headers else "a" # Set the file mode: "w" (write) if headers are provided, else "a"
    with open(output_file, mode, newline="") as f:
        writer = csv.writer(f)  # Create a CSV writer object
        if headers:
            writer.writerow(headers)  # Write the headers if provided 
        for row in csv.reader(data.splitlines()):  # Split the data string into rows and iterate
            writer.writerow(row)

# Create the Analyzer Agent 
def analyzer_agent(sample_data):
    message = client.messages.create(
        model=sonnet,
        max_tokens=400,  # Limit the response to 400 tokens
        temperature=0.1,  # Set a low temperature for more focuse, deterministic output
        system=ANALYZER_SYSTEM_PROMPT,  # Use the predefined system prompt for the analyzer
        messages=[
            {
                "role": "user",
                "content": ANALYZER_USER_PROMPT.format(sample_data=sample_data)
                # Format the user prompt with the provided sample data 
            }
        ]
    )
    return message.content[0].text  # Return the text content of the first message

# Create the Generator Agent
def generator_agent(analysis_result, sample_data, num_rows=30):
    message = client.messages.create(
        model=sonnet,
        max_tokens=1500,  # Allow for a longer response (1500 tokens)
        temperature=1,   # Set a high temperature for more creative, diverse output 
        system=GENERATOR_SYSTEM_PROMPT,
        message=[
            {
                "role": "user",
                "content": GENERATOR_USER_PROMPT.format(
                    num_rows=num_rows,
                    analysis_result=analysis_result,
                    sample_data=sample_data
                )
                # Format the user prompt with the number of rows to generate
                # The analysis result, and the sample data
            }
        ]
    )
    return message.content[0].text

# Main execution flow

# Get input from the user
file_path = input("\nEnter the name of your CSV file: ")
file_path = os.path.join("/app/data", file_path)
desired_rows = int(input("Enter the number of rows you want in the new dataset: "))

# Read the sample data from the input CSV file
sample_data = read_csv(file_path)
sample_data_str = "\n".join([",".join(row) for row in sample_data])  # Converts 2D list to a single string 

print("\nLaunching team of Agents...")
# Analyze the sample data using the Analyzer Agent
analysis_result = analyzer_agent(sample_data_str)
print("\n#### Analyzer Agent output: ####\n")
print(analysis_result)
print("\n--------------------------------------------\n\nGenerating new data...")

# Set up the output file
output_file = "/app/data/new_dataset.csv"
headers = sample_data[0]
# Create the output file with headers
save_to_csv("", output_file, headers)

batch_size = 30  # Number of rows to generate in each batch 
generated_rows = 0  # Counter to keep track of how many rows have been generated

# Generate data in batches until we reach the desired number of rows
while generated_rows < desired_rows:
    # Calculate how many rows to generate in this batch
    rows_to_generate = min(batch_size, desired_rows - generated_rows)
    # Generate a batch of data using the Generator agent 
    generated_data = generator_agent(analysis_result, sample_data_str, rows_to_generate)
    # Append the generate data to the output file
    save_to_csv(generated_data, output_file)
    # Update the count of generated rows
    generated_rows += rows_to_generate
    # Print progress update
    print(f"Generated {generated_rows} rows out of {desired_rows}")

# Inform the user that the process is complete
print(f"\nGenerated data has been saved to {output_file}")
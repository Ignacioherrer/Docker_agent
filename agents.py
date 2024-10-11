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
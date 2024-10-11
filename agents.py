# agents.py

# Importing the necessary libraries
import os
import csv
import anthropic

# Set up the Anthropic API key
if not os.getenv("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = input("Please enter your Anthropic API key: ") # Prompt the user to enter API key

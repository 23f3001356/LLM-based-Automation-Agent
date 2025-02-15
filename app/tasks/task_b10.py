import csv
import json
import os

def execute_task_b10(input_csv, output_json, filter_column, filter_value):
    """
    Filters rows in a CSV file based on a column value and writes the result to a JSON file.
    Args:
        input_csv (str): Path to the input CSV file.
        output_json (str): Path where filtered data will be saved as JSON.
        filter_column (str): The column name to filter by.
        filter_value (str): The value to match in the specified column.
    Returns:
        str: Success or error message.
    """
    try:
        # Check if input CSV file exists
        if not os.path.exists(input_csv):
            return f"Error: Input CSV file '{input_csv}' does not exist."

        filtered_data = []

        # Read CSV and filter rows based on the condition
        with open(input_csv, "r") as csvfile:
            reader = csv.DictReader(csvfile)

            # Check if the specified filter column exists
            if filter_column not in reader.fieldnames:
                return f"Error: Column '{filter_column}' not found in the CSV file. Available columns are: {', '.join(reader.fieldnames)}."

            for row in reader:
                # Perform case-insensitive matching
                if str(row.get(filter_column, "")).strip().lower() == str(filter_value).strip().lower():
                    filtered_data.append(row)

        # Check if any rows matched the filter condition
        if not filtered_data:
            return f"Warning: No rows matched the condition '{filter_column} = {filter_value}'."

        # Write filtered data to JSON file
        with open(output_json, "w") as jsonfile:
            json.dump(filtered_data, jsonfile, indent=4)

        return f"Task B10 completed successfully. Filtered data saved to {output_json}."
    
    except FileNotFoundError:
        return f"Error: File '{input_csv}' not found."
    except PermissionError:
        return f"Error: Permission denied while accessing files."
    except Exception as e:
        return f"Error executing Task B10: {str(e)}"
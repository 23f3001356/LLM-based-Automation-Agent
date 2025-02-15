import sqlite3
import csv

def execute_task_b5(db_path, query, output_file):
    """
    Runs a SQL query on an SQLite database and writes the result to a file.
    Args:
        db_path (str): Path to the SQLite database file.
        query (str): SQL query to execute.
        output_file (str): File path where query results will be saved.
    Returns:
        str: Success or error message.
    """
    try:
        conn = sqlite3.connect(db_path)
        
        cursor = conn.cursor()
        cursor.execute(query)
        
        results = cursor.fetchall()
        
        conn.close()

        # Write results to CSV
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(results)

        return f"Task B5 completed successfully. Results saved to {output_file}."
    except Exception as e:
        return f"Error executing Task B5: {str(e)}"
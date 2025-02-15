import sqlite3

def execute_task_a10(metal):
    """
    Calculates total sales for a specified ticket type (e.g., Gold, Silver, Bronze)
    and writes it to a corresponding output file.
    """
    import sqlite3

    db_file = "/data/ticket-sales.db"
    output_file = f"/data/ticket-sales-{metal.lower()}.txt"

    try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Use COALESCE to handle NULL values and parameterized query for safety
        query = "SELECT SUM(COALESCE(units, 0) * COALESCE(price, 0)) FROM tickets WHERE LOWER(type) = ?"
        cursor.execute(query, (metal.lower(),))
        
        total_sales = cursor.fetchone()[0]
        conn.close()

        # Handle case where no matching rows are found
        if total_sales is None:
            total_sales = 0

        # Write total sales to output file
        with open(output_file, 'w') as f:
            f.write(str(total_sales))

        return f"Task A10 completed successfully. Total sales for '{metal}': {total_sales}."
    except Exception as e:
        return f"Error executing Task A10: {str(e)}"
from datetime import datetime
from dateutil.parser import parse

def execute_task_a3(n):
    """
    Counts the number of Wednesdays in /data/dates.txt and writes the count to /data/dates-wednesdays.txt.
    Returns:
        str: Success or error message.
    """
    input_file = "/data/dates.txt"
    output_file = "/data/dates-wednesdays.txt"

    # List of known date formats
    known_formats = [
        "%d-%b-%Y",           # e.g., '27-May-2003'
        "%Y/%m/%d %H:%M:%S",  # e.g., '2019/08/16 03:19:25'
        "%Y/%m/%d",           # e.g., '2020/01/01'
        "%Y-%m-%d",           # e.g., '2025-02-12'
        "%b %d, %Y",          # e.g., 'Sep 22, 2000'
        "%d-%b-%y"            # e.g., '05-Jan-05'
    ]

    def parse_date(date_str):
        """
        Tries to parse a date string using known formats or falls back to dateutil.parser.parse().
        """
        for fmt in known_formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue
        # Fallback to dateutil.parser.parse() for unknown formats
        try:
            return parse(date_str.strip())
        except Exception as e:
            raise ValueError(f"Date '{date_str.strip()}' does not match any known formats or fallback parsing failed.")

    try:
        with open(input_file, 'r') as f:
            dates = f.readlines()

        # Count Wednesdays
        wednesday_count = sum(1 for date in dates if parse_date(date).weekday() == n)

        with open(output_file, 'w') as f:
            f.write(str(wednesday_count))

        return f"Task A3 completed successfully. Number of Wednesdays: {wednesday_count}."
    except Exception as e:
        return f"Error executing Task A3: {str(e)}"

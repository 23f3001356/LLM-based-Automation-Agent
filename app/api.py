from flask import Flask, request, jsonify
import os
import re
from app.tasks import (
    # Phase A tasks
    execute_task_a1,
    execute_task_a2,
    execute_task_a3,
    execute_task_a4,
    execute_task_a5,
    execute_task_a6,
    execute_task_a7,
    execute_task_a8,
    execute_task_a9,
    execute_task_a10,

    # Phase B tasks
    execute_task_b3,
    execute_task_b4,
    execute_task_b5,
    execute_task_b6,
    execute_task_b7,
    execute_task_b8,
    execute_task_b9,
    execute_task_b10
)

app = Flask(__name__)

# Days of the week for dynamic matching
DAYS_OF_WEEK = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

@app.route('/run', methods=['POST'])
def run_task():
    """
    Executes a plain-English task by parsing the task description and calling the appropriate function.
    """
    task_description = request.args.get('task')

    if not task_description:
        return jsonify({"error": "Task description is required"}), 400

    try:
        # Security validation (except for Task A6)
        if "markdown" not in task_description.lower():
            validate_task_security(task_description)

        # Extract email address dynamically from task description
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', task_description)
        user_email = email_match.group(0) if email_match else None

        # Handle Task A1: Install UV and run datagen.py
        if "install uv" in task_description.lower() or "datagen.py" in task_description.lower() or "script" in task_description.lower() or  "'uv'" in task_description.lower():
            if not user_email:
                return jsonify({"error": "No email address found in the task description"}), 400
            result = execute_task_a1(user_email)

        # Handle dynamic day-based tasks (e.g., count Wednesdays)
        elif any(day in task_description.lower() for day in DAYS_OF_WEEK):
            day_to_index = {day: idx for idx, day in enumerate(DAYS_OF_WEEK)}
            n = None
            for day in DAYS_OF_WEEK:
                if day in task_description.lower():
                    n = day_to_index[day]
                    result = execute_task_a3(n)
                    break

        # Handle other tasks (unchanged logic)
        elif "format" in task_description.lower() and "prettier" in task_description.lower():
            result = execute_task_a2()
        elif "sort contacts" in task_description.lower() or "contacts.json" in task_description.lower() or "array" in task_description.lower():
            result = execute_task_a4()
        elif "logs-recent.txt" in task_description.lower() or "recent logs" in task_description.lower() or "recent" in task_description.lower():
            result = execute_task_a5()
        elif "markdown" in task_description.lower() or "index.json" in task_description.lower() or "occurrance" in task_description.lower():
            result = execute_task_a6()
        elif "email sender" in task_description.lower() or "email.txt" in task_description.lower() or "address" in task_description.lower() or "email" in task_description.lower():
            result = execute_task_a7()
        elif "credit card number" in task_description.lower() or "credit-card.png" in task_description.lower() or "credit" in task_description.lower() or "debit" in task_description.lower() or "card" in task_description.lower():
            result = execute_task_a8()
        elif "similar comments" in task_description.lower() or "comments.txt" in task_description.lower() or "similar" in task_description.lower() or "comments" in task_description.lower():
            result = execute_task_a9()
        elif "gold ticket sales" in task_description.lower() or "ticket-sales.db" in task_description.lower() or "gold" in task_description.lower() or "bronze" in task_description.lower() or "silver" in task_description.lower() or "unit" in task_description.lower() or "type" in task_description.lower() or "price" in task_description.lower():
            if any(metal in task_description.lower() for metal in ["gold", "bronze", "silver"]):
                if "gold" in task_description.lower():
                    metal = "gold"
                elif "bronze" in task_description.lower():
                    metal = "bronze"
                elif "silver" in task_description.lower():
                    metal = "silver"
                    
            result = execute_task_a10(metal)

        # Phase B Tasks

        elif "fetch data from api" in task_description.lower() or "api data save" in task_description.lower() or "api" in task_description.lower() or "save" in task_description.lower():
            # Extract API URL from the task description
            api_url_match = re.search(r'https?://[^\s]+', task_description)
            api_url = api_url_match.group(0) if api_url_match else request.args.get('api_url', 'https://jsonplaceholder.typicode.com/posts')
            output_file = "/data/api_output.json"
            result = execute_task_b3(api_url, output_file)
    
        elif "clone git repo" in task_description.lower() or "commit" in task_description.lower() or "clone" in task_description.lower():
            # Extract GitHub repository URL from the task description
            repo_url_match = re.search(r'https?://[^\s]+', task_description)
            repo_url = repo_url_match.group(0) if repo_url_match else 'https://github.com/example/repo.git'
            commit_message = request.args.get('commit_message', 'Automated Commit')
            result = execute_task_b4(repo_url, commit_message)
    
        elif "run sql query" in task_description.lower() or "sqlite" in task_description.lower() or "duckdb" in task_description.lower() or "sql" in task_description.lower():
            # Extract SQL query from the task description
            query_match = re.search(r'(?i)(SELECT|INSERT|UPDATE|DELETE).*;', task_description)
            query = query_match.group(0) if query_match else request.args.get('query', 'SELECT * FROM table_name')
            db_path = "/data/database.db"
            output_file = "/data/sql_query_output.txt"
            result = execute_task_b5(db_path, query, output_file)
    
        elif "scrape website" in task_description.lower() or "extract website data" in task_description.lower() or "scrape" in task_description.lower() or "website" in task_description.lower():
            # Extract website URL from the task description
            url_match = re.search(r'https?://[^\s]+', task_description)
            url = url_match.group(0) if url_match else request.args.get('url', 'https://example.com')
            output_file = "/data/website_data.txt"
            result = execute_task_b6(url, output_file)
    
        elif "compress" in task_description.lower() or "resize" in task_description.lower():
            # Extract image size from the task description if specified
            size_match = re.search(r'(\d+)\s*x\s*(\d+)', task_description)
            size = tuple(map(int, size_match.groups())) if size_match else (100, 100)
            image_path = "/data/image.png"
            output_path = "/data/image_resized.png"
            result = execute_task_b7(image_path, output_path, size)
    
        elif "transcribe" in task_description.lower() or "mp3" in task_description.lower() or "audio" in task_description.lower():
            # Extract audio file path (if specified) from the description
            audio_path_match = re.search(r'/[^\s]+\.mp3', task_description)
            audio_path = audio_path_match.group(0) if audio_path_match else "/data/audio.mp3"
            output_file = "/data/transcription.txt"
            result = execute_task_b8(audio_path, output_file)
    
        elif "convert" in task_description.lower() or "html" in task_description.lower():
            # Extract markdown file path (if specified) from the description
            input_file_match = re.search(r'/[^\s]+\.md', task_description)
            input_file = input_file_match.group(0) if input_file_match else "/data/document.md"
            output_file = "/data/document.html"
            result = execute_task_b9(input_file, output_file)
    
        elif ("csv" in task_description.lower()) or ("json" in task_description.lower() or "filter" in task_description.lower()):
            # Extract CSV filter parameters from the description
            filter_column_match = re.search(r'filter column:\s*(\w+)', task_description.lower())
            filter_value_match = re.search(r'filter value:\s*([\w\s]+)', task_description.lower())
        
            filter_column = filter_column_match.group(1) if filter_column_match else request.args.get('filter_column', 'status')
            filter_value = filter_value_match.group(1).strip() if filter_value_match else request.args.get('filter_value', 'approved')
        
            input_csv = "/data/input.csv"
            output_json = "/data/output.json"
            result = execute_task_b10(input_csv, output_json, filter_column, filter_value)

        else:
            return jsonify({"error": f"No handler found for the given task: {task_description}"}), 400

        return jsonify({"message": result}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500



def validate_task_security(task_description):
    """
    Enforces security constraints:
    - Data outside /data cannot be accessed.
    - Data cannot be deleted.
    """
    if ".." in task_description or "/etc/" in task_description or "/var/" in task_description:
        raise ValueError("Access to paths outside /data is not allowed.")

    if ("delete" in task_description.lower()) or ("remove" in task_description.lower()):
        raise ValueError("Deletion of data is not allowed.")


@app.route('/read', methods=['GET'])
def read_file():
    file_path = request.args.get('path')

    if not os.path.exists(file_path):
        return jsonify({"error": f"File {file_path} does not exist"}), 404

    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return content, 200
    except Exception as e:
        return jsonify({"error": f"Error reading file {file_path}: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
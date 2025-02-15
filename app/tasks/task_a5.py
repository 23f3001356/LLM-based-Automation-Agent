import os

def execute_task_a5():
    """
    Extracts the first line of the 10 most recent .log files in /data/logs/ and writes them to /data/logs-recent.txt.
    Returns:
        str: Success or error message.
    """
    log_dir = "/data/logs/"
    output_file = "/data/logs-recent.txt"

    try:
        log_files = [os.path.join(log_dir, f) for f in os.listdir(log_dir) if f.endswith('.log')]
        log_files.sort(key=os.path.getmtime, reverse=True)  # Sort by modification time
        
        recent_logs = []
        for log_file in log_files[:10]:
            with open(log_file, 'r') as f:
                first_line = f.readline().strip()
                recent_logs.append(first_line)
        
        with open(output_file, 'w') as f:
            f.write("\n".join(recent_logs))
        
        return "Task A5 completed successfully."
    except Exception as e:
        return f"Error executing Task A5: {str(e)}"
import subprocess

def execute_task_a1(user_email):
    """
    Installs `uv` if not already installed and runs the datagen.py script.
    Args:
        user_email (str): The email to be passed as an argument to datagen.py.
    Returns:
        str: Success or error message.
    """
    try:
        # Install `uv` if not already installed
        subprocess.run(["pip", "install", "uv"], check=True)
        
        # Download the datagen.py script
        script_url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
        subprocess.run(["curl", "-O", script_url], check=True)
        
        # Run the script with the user's email
        subprocess.run(["python3", "datagen.py", user_email], check=True)
        
        return f"Task A1 completed successfully for {user_email}."
    except subprocess.CalledProcessError as e:
        return f"Error executing Task A1: {str(e)}"
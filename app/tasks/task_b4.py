import subprocess
import os
import shutil

def execute_task_b4(repo_url, commit_message):
    """
    Clones a git repository and makes a commit.
    Args:
        repo_url (str): The URL of the git repository to clone.
        commit_message (str): The commit message for the change.
    Returns:
        str: Success or error message.
    """
    try:
        repo_dir = "/data/repo"

        # Clean up if directory already exists
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)

        # Clone the repository
        subprocess.run(["git", "clone", repo_url, repo_dir], check=True)

        # Make a dummy change (e.g., add a README file)
        readme_path = os.path.join(repo_dir, "README.md")
        with open(readme_path, 'w') as f:
            f.write("# Automated Commit\n")

        # Stage and commit the change
        subprocess.run(["git", "-C", repo_dir, "add", "."], check=True)
        subprocess.run(["git", "-C", repo_dir, "commit", "-m", commit_message], check=True)

        return "Task B4 completed successfully. Changes committed."
    except Exception as e:
        return f"Error executing Task B4: {str(e)}"
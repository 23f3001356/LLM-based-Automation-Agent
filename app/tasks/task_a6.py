import os
import json
import glob

def execute_task_a6():
    """
    Creates an index of Markdown files in /data/docs/, mapping filenames to H1 titles.
    Returns:
        str: Success or error message.
    """
    docs_dir = "/data/docs/"
    output_file = "/data/docs/index.json"

    try:
        # Use glob to retrieve all .md files recursively
        md_files = glob.glob(os.path.join(docs_dir, "**", "*.md"), recursive=True)

        # Initialize an empty dictionary for the index
        index = {}

        for md_file in md_files:
            try:

                # Validate that the file path is inside /data/docs/
                if not os.path.abspath(md_file).startswith(os.path.abspath(docs_dir)):
                    raise ValueError(f"Access to {md_file} is not allowed.")

                # Compute the relative path of the file
                relative_path = os.path.relpath(md_file, docs_dir)

                # Open the file and extract the first H1 title
                with open(md_file, "r", encoding="utf-8") as file:
                    for line in file:
                        if line.startswith("# "):  # H1 title
                            title = line[2:].strip()  # Remove '# ' and strip whitespace
                            index[relative_path] = title
                            break  # Stop after finding the first H1

            except Exception as e:
                print(f"Error processing file {md_file}: {str(e)}")
                continue  # Skip this file if there's an error

        # Write the index to /data/docs/index.json
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=4)

        return "Task A6 completed successfully."
    except Exception as e:
        return f"Error executing Task A6: {str(e)}"
import markdown

def execute_task_b9(input_file, output_file):
    """
    Converts a Markdown file to HTML and saves it to a new file.
    Args:
        input_file (str): Path to the Markdown (.md) file.
        output_file (str): Path where the generated HTML will be saved.
    Returns:
        str: Success or error message.
    """
    try:
        # Read the Markdown content from the input file
        with open(input_file, "r") as f:
            markdown_content = f.read()
        
        # Convert Markdown to HTML
        html_content = markdown.markdown(markdown_content)

        # Save the HTML content to the output file
        with open(output_file, "w") as f:
            f.write(html_content)

        return f"Task B9 completed successfully. HTML saved to {output_file}."
    
    except FileNotFoundError:
        return "Error executing Task B9: Input file not found."
    except Exception as e:
        return f"Error executing Task B9: {str(e)}"
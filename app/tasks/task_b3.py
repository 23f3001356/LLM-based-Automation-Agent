import requests

def execute_task_b3(api_url, output_file):
    """
    Fetches data from an API and saves it to a file.
    Args:
        api_url (str): The URL of the API to fetch data from.
        output_file (str): The file path where the data will be saved.
    Returns:
        str: Success or error message.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()

        # Save JSON response if applicable
        with open(output_file, 'w') as f:
            if response.headers.get('Content-Type') == 'application/json':
                f.write(response.text)
            else:
                f.write(response.content.decode('utf-8'))

        return f"Task B3 completed successfully. Data saved to {output_file}."
    except Exception as e:
        return f"Error executing Task B3: {str(e)}"
from bs4 import BeautifulSoup
import requests

def execute_task_b6(url, output_file, element="body"):
    """
    Scrapes data from a website and saves it to a file.
    Args:
        url (str): The URL of the website to scrape.
        output_file (str): File path where scraped data will be saved.
        element (str): HTML element/tag to extract (default is "body").
    Returns:
        str: Success or error message.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract specified elements
        extracted_data = soup.find_all(element)
        
        with open(output_file, 'w') as f:
            for tag in extracted_data:
                f.write(tag.get_text(strip=True) + "\n")

        return f"Task B6 completed successfully. Data saved to {output_file}."
    except Exception as e:
        return f"Error executing Task B6: {str(e)}"
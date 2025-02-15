import os
import requests

def execute_task_a7():
    """
    Extracts the sender's email address from /data/email.txt using GPT-4o-Mini via AI Proxy.
    """
    input_file = "/data/email.txt"
    output_file = "/data/email-sender.txt"

    # Retrieve AI Proxy token from environment variable
    proxy_token = os.getenv("AIPROXY_TOKEN")
    if not proxy_token:
        raise ValueError("AI Proxy token not found! Set it as an environment variable.")

    # Define the AI Proxy endpoint for chat completions
    proxy_endpoint = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

    try:
        # Read email content
        with open(input_file, 'r', encoding='utf-8') as f:
            email_content = f.read()

        # Prepare request payload
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are an assistant that extracts email addresses."},
                {"role": "user", "content": f"Extract only the sender's email address from this email:\n\n{email_content}"}
            ]
        }

        # Set headers with Bearer token authorization
        headers = {
            "Authorization": f"Bearer {proxy_token}",
            "Content-Type": "application/json"
        }

        # Send request to GPT-4o-Mini via AI Proxy
        response = requests.post(proxy_endpoint, headers=headers, json=payload)

        if response.status_code != 200:
            return f"Error: Failed to communicate with GPT-4o-Mini API. Status code: {response.status_code}, Response: {response.text}"

        # Extract sender's email address from response
        response_data = response.json()
        sender_email = response_data['choices'][0]['message']['content'].strip()

        # Write only the extracted email address to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(sender_email)

        return f"Task A7 completed successfully. Sender's email: {sender_email}"

    except Exception as e:
        return f"Error executing Task A7: {str(e)}"
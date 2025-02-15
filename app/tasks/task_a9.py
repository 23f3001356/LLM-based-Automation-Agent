import os
import requests
from scipy.spatial.distance import cosine

def execute_task_a9():
    """
    Finds the most similar pair of comments in /data/comments.txt using embeddings 
    and writes them to /data/comments-similar.txt.
    """
    input_file = "/data/comments.txt"
    output_file = "/data/comments-similar.txt"

    # Retrieve AI Proxy token from environment variable
    proxy_token = os.getenv("AIPROXY_TOKEN")
    if not proxy_token:
        raise ValueError("AI Proxy token not found! Set it as an environment variable.")

    # Define the AI Proxy endpoint for embeddings
    proxy_endpoint = "https://aiproxy.sanand.workers.dev/openai/v1/embeddings"

    try:
        # Read all comments from input file
        if not os.path.exists(input_file):
            return f"Error: Input file not found: {input_file}"

        with open(input_file, 'r', encoding='utf-8') as f:
            comments = [line.strip() for line in f.readlines()]

        if len(comments) < 2:
            return "Error: Not enough comments to find similar pairs."

        # Generate embeddings for each comment
        embeddings = []
        headers = {
            "Authorization": f"Bearer {proxy_token}",
            "Content-Type": "application/json"
        }

        for comment in comments:
            payload = {
                "model": "text-embedding-3-small",
                "input": [comment]  # Input must be a list of strings
            }

            response = requests.post(proxy_endpoint, headers=headers, json=payload)

            # Debugging information for response
            if response.status_code == 401:
                return f"Error: Unauthorized (401). Check your API token."
            elif response.status_code != 200:
                return f"Error: Failed to get embedding for comment. Status code: {response.status_code}, Response: {response.text}"

            # Extract embedding from response
            response_data = response.json()
            embedding = response_data.get('data', [{}])[0].get('embedding')
            if embedding is None:
                return f"Error: 'data' field missing in response. Response: {response.text}"

            embeddings.append(embedding)

        # Find most similar pair of comments using cosine similarity
        max_similarity = float('-inf')
        most_similar_pair = ("", "")

        for i in range(len(comments)):
            for j in range(i + 1, len(comments)):
                similarity = 1 - cosine(embeddings[i], embeddings[j])
                if similarity > max_similarity:
                    max_similarity = similarity
                    most_similar_pair = (comments[i], comments[j])

        # Write most similar pair to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(most_similar_pair))

        return "\n".join(most_similar_pair)

    except Exception as e:
        return f"Error executing Task A9: {str(e)}"

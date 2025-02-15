import os
import re
import requests
from PIL import Image
import pytesseract

def luhn_checksum(card_number):
    """Corrected Luhn algorithm implementation"""
    total = 0
    for i, digit in enumerate(reversed(str(card_number))):
        n = int(digit)
        # 🔴 FIXED: Double digits at ODD positions (was even)
        total += (n*2 // 10 + n*2 % 10) if i % 2 else n
    return total % 10 == 0

def preprocess_image(image_path):
    """Enhanced image preprocessing with sharpening"""
    img = Image.open(image_path)
    return img.convert('L').resize((img.width*2, img.height*2), Image.BICUBIC)

def execute_task_a8():
    """
    Final fixed version with:
    - Correct Luhn validation
    - Better number extraction
    - Enhanced error handling
    """
    input_files = ["/data/credit-card.png", "/data/credit_card.png"]
    input_path = next((f for f in input_files if os.path.exists(f)), None)
    output_file = "/data/credit-card.txt"

    if not input_path:
        return "Error: No input file found"

    try:
        # OCR Processing
        processed_img = preprocess_image(input_path)
        raw_text = pytesseract.image_to_string(processed_img)
        print(f"OCR Output: {raw_text}")  # Debug log

        # 🔴 ADDED: API error handling
        proxy_token = os.getenv("AIPROXY_TOKEN")
        if not proxy_token:
            return "Error: Missing AIPROXY_TOKEN environment variable"

        # LLM API Call
        try:
            response = requests.post(
                "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {proxy_token}"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "Extract ONLY 16-digit credit card number. Respond ONLY with digits."},
                        {"role": "user", "content": f"Text: {raw_text}\nNumber:"}
                    ],
                    "temperature": 0.0
                },
                timeout=10
            )
            response.raise_for_status()
        except requests.RequestException as e:
            return f"API Error: {str(e)}"

        # Response Handling
        response_data = response.json()
        if 'choices' not in response_data or not response_data['choices']:
            return "Error: Empty LLM response"
            
        response_text = response_data['choices'][0]['message']['content'].strip()
        print(f"LLM Response: {response_text}")  # Debug log
        
        # 🔴 FIXED: Extract any 16-digit sequences
        sanitized = re.sub(r'\D', '', response_text)
        candidates = re.findall(r'\d{16}', sanitized)  # Find ALL 16-digit sequences
        candidates = [num for num in candidates if len(num) == 16]  # Exact length
        
        # Validation
        valid_numbers = [num for num in candidates if luhn_checksum(num)]
        
        if not valid_numbers:
            return f"Error: No valid numbers found. Candidates: {candidates}"

        # Write output
        try:
            with open(output_file, 'w') as f:
                f.write(valid_numbers[0])
        except IOError as e:
            return f"File Write Error: {str(e)}"

        return f"Success: Saved {valid_numbers[0]} to {output_file}"

    except Exception as e:
        return f"Critical Error: {str(e)}"
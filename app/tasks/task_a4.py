import json

def execute_task_a4():
    """
    Sorts contacts in /data/contacts.json by last_name, then first_name, and writes to /data/contacts-sorted.json.
    Returns:
        str: Success or error message.
    """
    input_file = "/data/contacts.json"
    output_file = "/data/contacts-sorted.json"

    try:
        with open(input_file, 'r') as f:
            contacts = json.load(f)
        
        sorted_contacts = sorted(contacts, key=lambda x: (x['last_name'], x['first_name']))
        
        with open(output_file, 'w') as f:
            json.dump(sorted_contacts, f, indent=4)
        
        return "Task A4 completed successfully."
    except Exception as e:
        return f"Error executing Task A4: {str(e)}"
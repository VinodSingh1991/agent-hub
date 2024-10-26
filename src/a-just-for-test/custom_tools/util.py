import json
import re

def convert_markdown_to_json(markdown_str):
    # Use regex to extract the JSON content between triple backticks
    json_match = re.search(r'```json\n(.*?)\n```', markdown_str, re.DOTALL)
    
    if json_match:
        json_str = json_match.group(1)  # Extract JSON part
        
        try:
            # Convert the JSON string to a Python dictionary
            json_data = json.loads(json_str)
            return json_data
        except json.JSONDecodeError as e:
            return markdown_str
    else:
        return markdown_str

# Example usage
markdown_data = '''```json
{"status": "success", "response_type": "table", "total_no_of_leads": 1, "acid_columns": ["LeadID", "CampaignID", "FirstName", "LastName", "MiddleName", "Phone", "Email", "Address", "City", "State", "PinCode", "Country", "ProductId", "AccountId", "RatingId", "CreatedOn", "CreatedBy", "ActivityId", "Amount"], "acid_rows": [{"LeadID": 1, "CampaignID": 101, "FirstName": "John", "LastName": "Doe", "MiddleName": "A", "Phone": "1234567890", "Email": "john.doe@example.com", "Address": "123 Main St", "City": "New York", "State": "NY", "PinCode": "10001", "Country": "USA", "ProductId": 201, "AccountId": 301, "RatingId": 5, "CreatedOn": "2023-10-01 10:30:00", "CreatedBy": "admin", "ActivityId": 1001, "Amount": 150.75}], "acid_update_message_of_ai": "Here is The List of Complete Leads"}
```'''

json_output = convert_markdown_to_json(markdown_data)
print(json_output)

import openpyxl
import json

input_file = 'Wazuh Logs.xlsx'  
output_file = 'dataset.jsonl'

workbook = openpyxl.load_workbook(input_file)
sheet = workbook.active

with open(output_file, 'w') as jsonlfile:
    for row in sheet.iter_rows(min_row=2, max_col=2, values_only=True):  
        prompt = row[0].strip() if row[0] else ""
        completion = row[1].strip() if row[1] else ""
 
        # Create chat-formatted data
        chat_data = {
            "messages": [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": completion}
            ]
        }
        jsonlfile.write(json.dumps(chat_data) + '\n')

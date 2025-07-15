# Airtable CSV Manager

This class works with Airtable to fetch data and save it as a CSV file.

## Setup Instructions

### 1. Get Your Airtable API Key
1. Log in to your Airtable account.
2. Go to your account settings.
3. Generate an API key.

### 2. Find Your Base ID and Table Name
1. Open your Airtable base.
2. The Base ID can be found in the URL: `https://airtable.com/{BASE_ID}`.
3. Use the name of the table you want to fetch data from.

### 3. Usage Example

```python
from airtable_csv import AirtableCSVManager

# Initialize the manager
manager = AirtableCSVManager(
    base_id="your-base-id",  # Found in the URL of your Airtable base
    table_name="Table1",  # Name of the specific table
    api_key="your-api-key"  # Your Airtable API key
)

# Update CSV from Airtable
result = manager.update_csv_from_airtable()
print(result)

# Read the CSV data
csv_data = manager.read_csv()
print(csv_data)

# Convert to JSON format
json_data = manager.convert_csv_to_json()
print(json_data)
```

### 4. Required Dependencies
Make sure to install the required packages:
```bash
pip install -r requirements.txt
```
# instagram-to-s3-script

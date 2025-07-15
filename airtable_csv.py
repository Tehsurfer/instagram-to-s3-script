import os
import csv
import io
import json
from pyairtable import Table




class AirtableCSVManager:
    def __init__(self, base_id, table_name, api_key):
        self.base_id = base_id
        self.table_name = table_name
        self.api_key = api_key
        self.csv_path = "data/nutrition-school-scrape.csv"
        self.table = Table(self.api_key, self.base_id, self.table_name)

    def fetch_data_from_airtable(self):
        # Fetch all records from Airtable using pyairtable
        records = self.table.all()
        return records

    def update_csv_from_airtable(self):
        try:
            records = self.fetch_data_from_airtable()
            if not records:
                return None


            # Extract all unique headers from all records
            all_fieldnames = set()
            rows = []
            for record in records:
                fields = record["fields"]
                all_fieldnames.update(fields.keys())
                rows.append(fields)
            headers = list(all_fieldnames)

            # Create CSV content
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=headers, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(rows)

            csv_data = output.getvalue()
            output.close()

            # Save to file
            with open(self.csv_path, "w", encoding="utf-8") as f:
                f.write(csv_data)

            return "Successfully updated CSV from Airtable. Access it at /data/.csv"
        except Exception as e:
            return f"Error updating CSV from Airtable: {str(e)}"

    def read_csv(self):
        # Read and return the raw CSV data from the file
        if not os.path.exists(self.csv_path):
            return None
        with open(self.csv_path, "r", encoding="utf-8") as f:
            return f.read()

    def convert_csv_to_json(self):
        # Read the CSV file and convert to JSON
        if not os.path.exists(self.csv_path):
            return None
        result = []
        with open(self.csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                result.append(row)
        return result

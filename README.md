
# instagram-to-s3-script

This project provides tools to fetch data from Airtable, save it as a CSV, and update image and video URLs in the CSV to point to Amazon S3 permalinks.

## Features
- Fetch Airtable data and save as CSV
- Upload images and videos to S3 and update CSV URLs
- Easily configurable with environment variables

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Tehsurfer/instagram-to-s3-script.git
cd instagram-to-s3-script
```

### 2. Set Up Environment Variables
Create a `.env.local` or `.env` file in the project root with the following:
```
BASE_ID=your_airtable_base_id
TABLE_NAME=your_airtable_table_name
API_KEY=your_airtable_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=ap-southeast-2
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Fetch Airtable Data and Save as CSV
```python
from airtable_csv import AirtableCSVManager

manager = AirtableCSVManager(
    base_id="your-base-id",
    table_name="your-table-name",
    api_key="your-api-key"
)
result = manager.update_csv_from_airtable()
print(result)
```

### Update Image URLs in CSV to S3 Permalinks
```python
from url_mod import URLModifier

csv_path = "data/nutrition-school-scrape.csv"
bucket_name = "instagram-files-permalink"
url_modifier = URLModifier(csv_path, bucket_name)
url_modifier.update_image_urls()
```

### Update Video URLs in CSV to S3 Permalinks
```python
url_modifier.update_video_urls()
```

## Notes
- The updated CSVs will be saved as `*-updated.csv` and `*-video-updated.csv` in the `data/` directory.
- Make sure your AWS S3 bucket policy allows uploads and public reads as needed.
- The project uses `.env.local` or `.env` for configuration. Do not commit these files.

## License
MIT

#url-modifier - steps through nutrition-school-scrape.csv and 
# updates the imageUrl column to point to the S3 bucket for permalinks

import os
import csv
from dotenv import load_dotenv
from s3_manager import S3Manager

class URLModifier:
    def __init__(self, csv_path, bucket_name):
        self.csv_path = csv_path
        self.new_csv_path = csv_path.replace('.csv', '-updated.csv')
        self.bucket_name = bucket_name
        self.s3_manager = S3Manager(bucket_name)
        load_dotenv()

    def update_image_urls(self):
        with open(self.csv_path, "r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            rows = list(reader)
            fieldnames = reader.fieldnames

        for row in rows:
            image_url = row.get("imgUrl")
            if image_url:
                try:
                    s3_url = self.s3_manager.upload_image_from_url(image_url)
                    print(f"Updated {image_url} to {s3_url}")
                    row["imgUrl"] = s3_url
                except Exception as e:
                    print(f"Failed to upload {image_url}: {e}")

        with open(self.new_csv_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Updated image URLs in {self.new_csv_path} to point to S3 bucket {self.bucket_name}")

    def update_video_urls(self):
        with open(self.csv_path, "r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            rows = list(reader)
            fieldnames = reader.fieldnames

        for row in rows:
            video_url = row.get("videoUrl")
            if video_url:
                try:
                    s3_url = self.s3_manager.upload_video_from_url(video_url)
                    print(f"Updated {video_url} to {s3_url}")
                    row["videoUrl"] = s3_url
                except Exception as e:
                    print(f"Failed to upload {video_url}: {e}")

        new_video_csv_path = self.csv_path.replace('-updated.csv', '-all-updated.csv')
        with open(new_video_csv_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Updated video URLs in {new_video_csv_path} to point to S3 bucket {self.bucket_name}")

if __name__ == "__main__":
    csv_path = "data/nutrition-school-scrape-updated.csv"
    bucket_name = "instagram-files-permalink"

    url_modifier = URLModifier(csv_path, bucket_name)
    #url_modifier.update_image_urls() # I did these one at a time
    url_modifier.update_video_urls()
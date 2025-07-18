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
        self.max_total_uploads_in_bytes = 5 * 1024 * 1024 * 1024  # 5 GB
        self.current_total_uploads_in_bytes = 0
        self.file_number = 1
        load_dotenv()

    def set_csv_source(self, csv_path):
        """Set the CSV source file path."""
        self.csv_path = csv_path
        self.new_csv_path = csv_path.replace('.csv', '-updated.csv')
        print(f"CSV source set to: {self.csv_path}")

    def set_max_total_uploads_in_bytes(self, max_bytes):
        """Set the maximum total uploads size in bytes."""
        self.max_total_uploads_in_bytes = max_bytes
        print(f"Max total uploads size set to: {self.max_total_uploads_in_bytes} bytes")

    def set_s3_folder(self, folder_name):
        """Set the S3 folder path for uploads."""
        self.s3_manager.set_folder(folder_name)
        print(f"S3 folder set to: {self.s3_manager.folder}")

    def update_urls_for_column(self, column_name, content_type, update_file_path=None):

        if not update_file_path:
            print(f"No update file path provided, modifying original CSV: {self.new_csv_path}")
            update_file_path = self.new_csv_path

        with open(self.csv_path, "r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            rows = list(reader)
            fieldnames = reader.fieldnames

        try:
            for i, row in enumerate(rows):
                if self.current_total_uploads_in_bytes >= self.max_total_uploads_in_bytes:
                    print("Reached maximum total uploads size. Stopping updates.")
                    break
                url = row.get(column_name)
                if url:
                    try:
                        result = self.s3_manager.upload_file_from_url(url, content_type, self.file_number)
                        print(f"Updated {url} to {result['permalink']}")
                        row[column_name] = result['permalink']
                        self.current_total_uploads_in_bytes += result['file_size'] or 0
                        self.file_number += 1
                    except Exception as e:
                        print(f"Failed to upload {url}: {e}")
                        # Continue processing other rows
                        continue
        except KeyboardInterrupt:
            print(f"\nProcess interrupted by user. Saving progress...")
        except Exception as e:
            print(f"Unexpected error occurred: {e}. Saving progress...")
        finally:
            # Always save progress, even if interrupted
            with open(self.new_csv_path, "w", newline="", encoding="utf-8") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            print(f"Progress saved to {self.new_csv_path}. Processed updates point to S3 bucket {self.bucket_name}")

if __name__ == "__main__":
    csv_path = "data/nutrition-school-scrape-updated.csv"
    bucket_name = "instagram-files-permalink"
    folder_name = "nutrition-school-scrape/"

    
    url_modifier = URLModifier(csv_path, bucket_name)
    url_modifier.set_s3_folder(folder_name)
    url_modifier.set_max_total_uploads_in_bytes(10 * 1024 * 1024 * 1024)  # Set to 10 GB for testing

    url_modifier.update_urls_for_column("imgUrl", "image/jpeg", update_file_path="data/nutrition-school-scrape-img-updated.csv")
    url_modifier.set_csv_source("data/nutrition-school-scrape-all.csv")
    url_modifier.update_urls_for_column("videoUrl", "video/mp4", update_file_path="data/nutrition-school-scrape-all-updated.csv")
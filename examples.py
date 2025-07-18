from s3_manager import S3Manager
from airtable_csv import AirtableCSVManager
from dotenv import load_dotenv
import os

bucket_name = 'instagram-files-permalink'

test_image = "https://scontent-cdg4-3.cdninstagram.com/v/t51.2885-15/517242755_18519186250052586_837350672080328910_n.jpg?stp=dst-jpg_e35_p1080x1080_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6IkNBUk9VU0VMX0lURU0uaW1hZ2VfdXJsZ2VuLjE0NDB4MTgwMC5zZHIuZjgyNzg3LmRlZmF1bHRfaW1hZ2UifQ&_nc_ht=scontent-cdg4-3.cdninstagram.com&_nc_cat=106&_nc_oc=Q6cZ2QEJI5KPcWj9nR7sIT4XPZ1fXmOO_K3B1JwTvSpjLLh-wd-RCM6CHVI6vehXX44OCUY&_nc_ohc=OBOZS-pfv7YQ7kNvwGDVZoR&_nc_gid=N2UOuyw34wCn7mV-IofyDQ&edm=ACWDqb8BAAAA&ccb=7-5&ig_cache_key=MzY3Mjk0MDk5MDkwMTUzODQ1Ng%3D%3D.3-ccb7-5&oh=00_AfT15FLuwwFYem0eTp18uy5XIbmcY5-pm2rS5eCDEYkrmg&oe=687A5AA4&_nc_sid=ee9879"
test_video = "https://scontent-cdg4-2.cdninstagram.com/o1/v/t2/f2/m86/AQMmrriDTSy9gdk23nSbtt_hw4vNXzWVoM8y1WuJGPtv-mK8xsuYubqRRjxU96hSKas4frOAnwGKTwJ-uJdok52b0sABK7-akd8Iz8E.mp4?_nc_cat=101&_nc_sid=5e9851&_nc_ht=scontent-cdg4-2.cdninstagram.com&_nc_ohc=AZQz2QjB05oQ7kNvwFbi4hf&efg=eyJ2ZW5jb2RlX3RhZyI6Inhwdl9wcm9ncmVzc2l2ZS5JTlNUQUdSQU0uQ0xJUFMuQzMuNzIwLmRhc2hfYmFzZWxpbmVfMV92MSIsInhwdl9hc3NldF9pZCI6MTI0NDY5MTEyNjU0MTAwNiwidmlfdXNlY2FzZV9pZCI6MTAwOTksImR1cmF0aW9uX3MiOjEzLCJ1cmxnZW5fc291cmNlIjoid3d3In0%3D&ccb=17-1&vs=3baf228e9a25eecd&_nc_vs=HBksFQIYUmlnX3hwdl9yZWVsc19wZXJtYW5lbnRfc3JfcHJvZC80QjQ1NDRDM0JBOTYzMDJEQjNCNzhCMTcyNTdGNkE4NF92aWRlb19kYXNoaW5pdC5tcDQVAALIARIAFQIYOnBhc3N0aHJvdWdoX2V2ZXJzdG9yZS9HSWExWEI3R2RzbUI2TzBFQUlvU1g1OXBYVEpOYnFfRUFBQUYVAgLIARIAKAAYABsCiAd1c2Vfb2lsATEScHJvZ3Jlc3NpdmVfcmVjaXBlATEVAAAmnOuex8eCtgQVAigCQzMsF0AqIcrAgxJvGBJkYXNoX2Jhc2VsaW5lXzFfdjERAHX-B2XmnQEA&_nc_zt=28&oh=00_AfS8IFs1ucxgvKVcWKl9kO9seoCrGu3pON9VwwaWa3_JAQ&oe=6876604E"

def test_s3_url_upload():
    s3_manager = S3Manager(bucket_name=bucket_name)
    image_url = test_image

    try:
        permalink = s3_manager.upload_image_from_url(image_url)
        print(f"Image uploaded successfully. Permalink: {permalink}")
    except Exception as e:
        print(f"Error: {str(e)}")


def test_s3_video_upload():
    s3_manager = S3Manager(bucket_name=bucket_name)
    video_url = test_video

    try:
        permalink = s3_manager.upload_video_from_url(video_url)
        print(f"Video uploaded successfully. Permalink: {permalink}")
    except Exception as e:
        print(f"Error: {str(e)}")

def test_airtable_csv_update():
    load_dotenv('.env.local')

    # Ensure required environment variables are set
    if not os.getenv('AIRTABLE_BASE_ID') or not os.getenv('AIRTABLE_TABLE_NAME') or not os.getenv('AIRTABLE_API_KEY'):
        load_dotenv('.env')
    if not os.getenv('AIRTABLE_BASE_ID') or not os.getenv('AIRTABLE_TABLE_NAME') or not os.getenv('AIRTABLE_API_KEY'):
        raise ValueError("Missing required environment variables: AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, AIRTABLE_API_KEY")

    exporter = AirtableCSVManager(
        base_id=os.getenv('AIRTABLE_BASE_ID'),
        table_name=os.getenv('AIRTABLE_TABLE_NAME'),
        api_key=os.getenv('AIRTABLE_API_KEY')
    )

    result = exporter.update_csv_from_airtable()
    print(result)


def test_create_s3_folder():
    s3_manager = S3Manager(bucket_name=bucket_name)
    folder_name = "test-folder/"

    try:
        folder_path = s3_manager.create_folder(folder_name)
        print(f"Folder created successfully: {folder_path}")
    except Exception as e:
        print(f"Error creating folder: {str(e)}")


if __name__ == "__main__":
    test_create_s3_folder()
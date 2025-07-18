from s3_manager import S3Manager
from airtable_csv import AirtableCSVManager
from dotenv import load_dotenv
import os

bucket_name = 'instagram-files-permalink'

test_image = "https://scontent-cdg4-3.cdninstagram.com/v/t51.2885-15/517242755_18519186250052586_837350672080328910_n.jpg?stp=dst-jpg_e35_p1080x1080_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6IkNBUk9VU0VMX0lURU0uaW1hZ2VfdXJsZ2VuLjE0NDB4MTgwMC5zZHIuZjgyNzg3LmRlZmF1bHRfaW1hZ2UifQ&_nc_ht=scontent-cdg4-3.cdninstagram.com&_nc_cat=106&_nc_oc=Q6cZ2QEJI5KPcWj9nR7sIT4XPZ1fXmOO_K3B1JwTvSpjLLh-wd-RCM6CHVI6vehXX44OCUY&_nc_ohc=OBOZS-pfv7YQ7kNvwGDVZoR&_nc_gid=N2UOuyw34wCn7mV-IofyDQ&edm=ACWDqb8BAAAA&ccb=7-5&ig_cache_key=MzY3Mjk0MDk5MDkwMTUzODQ1Ng%3D%3D.3-ccb7-5&oh=00_AfT15FLuwwFYem0eTp18uy5XIbmcY5-pm2rS5eCDEYkrmg&oe=687A5AA4&_nc_sid=ee9879"
test_video = "https://scontent-ams4-1.cdninstagram.com/o1/v/t2/f2/m86/AQPxz7jGXQ_e_cktNHaohLM8eKtvjspiGG_4az-hgCNHSJ_2T3PIosMj8aMAw7eYdNmpI-E-UGvunA7OMu5UuTTSb73MGpBZEE2gO4w.mp4?_nc_cat=109&_nc_sid=5e9851&_nc_ht=scontent-ams4-1.cdninstagram.com&_nc_ohc=_PIjjDS0_QMQ7kNvwG9s29n&efg=eyJ2ZW5jb2RlX3RhZyI6Inhwdl9wcm9ncmVzc2l2ZS5JTlNUQUdSQU0uQ0xJUFMuQzMuNzIwLmRhc2hfYmFzZWxpbmVfMV92MSIsInhwdl9hc3NldF9pZCI6NzI0OTk3MjcwMjg1NDMyLCJ2aV91c2VjYXNlX2lkIjoxMDA5OSwiZHVyYXRpb25fcyI6NiwidXJsZ2VuX3NvdXJjZSI6Ind3dyJ9&ccb=17-1&vs=67cf893e164e3ef&_nc_vs=HBksFQIYUmlnX3hwdl9yZWVsc19wZXJtYW5lbnRfc3JfcHJvZC8zNzRBNTU0MDk0QTQzRkMzMDIzQkJGNDQ5NkMzQkQ5N192aWRlb19kYXNoaW5pdC5tcDQVAALIARIAFQIYOnBhc3N0aHJvdWdoX2V2ZXJzdG9yZS9HSUxURFI5QVJkMGxTVVFDQUR2aldadG16REpVYnFfRUFBQUYVAgLIARIAKAAYABsCiAd1c2Vfb2lsATEScHJvZ3Jlc3NpdmVfcmVjaXBlATEVAAAm8LGRzLLYyQIVAigCQzMsF0AaiDEm6XjVGBJkYXNoX2Jhc2VsaW5lXzFfdjERAHX-B2XmnQEA&_nc_zt=28&oh=00_AfT39L3Vu7-LF7ObBSPETlX2WGiaCBt1XRf-J8GTBVTK1w&oe=687AC12E"

def test_s3_url_upload():
    s3_manager = S3Manager(bucket_name=bucket_name)
    image_url = test_image

    try:
        result = s3_manager.upload_image_from_url(image_url)
        print(f"Image uploaded successfully. Permalink: {result['permalink']}")
        print(f"File size: {result['file_size']} MB")
    except Exception as e:
        print(f"Error: {str(e)}")


def test_s3_video_upload():
    s3_manager = S3Manager(bucket_name=bucket_name)
    video_url = test_video

    try:
        result = s3_manager.upload_video_from_url(video_url)
        print(f"Video uploaded successfully. Permalink: {result['permalink']}")
        print(f"File size: {result['file_size']} MB")
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

def test_upload_video_to_new_folder():
    s3_manager = S3Manager(bucket_name=bucket_name)
    folder_name = "test-video-folder/"
    s3_manager.set_folder(folder_name)

    try:
        result = s3_manager.upload_video_from_url(test_video, content_type="video/mp4")
        print(f"Video uploaded successfully to {folder_name}. Permalink: {result['permalink']}")
        print(f"File size: {result['file_size']} MB")
    except Exception as e:
        print(f"Error uploading video: {str(e)}")

def test_upload_with_name():
    s3_manager = S3Manager(bucket_name=bucket_name)
    folder_name = "test-video-folder/"
    s3_manager.set_folder(folder_name)

    try:
        result = s3_manager.upload_video_from_url(test_video, content_type="video/mp4", object_name="1")
        print(f"Video uploaded successfully with custom name to {folder_name}. Permalink: {result['permalink']}")
        print(f"File size: {result['file_size']} MB")
    except Exception as e:
        print(f"Error uploading video with custom name: {str(e)}")


if __name__ == "__main__":
    test_upload_with_name()
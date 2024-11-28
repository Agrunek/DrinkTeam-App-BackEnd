from azure.storage.blob import BlobServiceClient
from fastapi import File, UploadFile, HTTPException
import sqlalchemy.orm as _orm

AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=bazadanych9797;AccountKey=API_KEY;EndpointSuffix=core.windows.net"
AZURE_CONTAINER_NAME = "drink-team-images"


blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

async def upload_recipe_image_to_azure(recipe_id : int, upload_file : UploadFile = File(...)):
    
    print(f" => Recipe id = {recipe_id}  File = {upload_file.filename}")

    file_name = f"recipe{recipe_id}/{upload_file.filename}"

    file_data = await upload_file.read()

    try:
        blob_client = container_client.get_blob_client(file_name)
        blob_client.upload_blob(data = file_data, overwrite = True)

        return blob_client.url
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

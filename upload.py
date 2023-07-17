import os
from idrive_client_id import idrive_id
from synology_client_id import synology_id

# Example usage
client = idrive_id()
synology_client = synology_id()


def upload_file_to_idrive(file_path, idrive_bucket_name, synology_bucket_name, idrive_switch, synology_switch):

    # Extract the filename from the file path
    filename = file_path.split("/")[-1]

    # Construct the destination key (filename)
    destination_key = os.path.basename(filename)

    # Upload the file
    if idrive_switch:
        client.upload_file(file_path, idrive_bucket_name, destination_key)
        print(f"IDRIVE: File uploaded successfully to '{destination_key}' in the '{idrive_bucket_name}' bucket.")
    else:
        print("Idrive is disabled")
    
    if synology_switch:
        synology_client.upload_file(file_path, synology_bucket_name, destination_key) 
        print(f"SYNOLOGY: File uploaded successfully to '{destination_key}' in the '{synology_bucket_name}' bucket.")
    else:
        print("Synolgy is disabled")



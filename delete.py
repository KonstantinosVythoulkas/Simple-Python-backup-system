from idrive_client_id import idrive_id
from synology_client_id import synology_id

# Example usage
idrive_client = idrive_id()
synology_client = synology_id()



def count_files(idrive_bucket_name, synology_bucket_name,MAX_WEEKLY_BACKUPS,MAX_DAILY_BACKUPS):
    response_idrive = idrive_client.list_objects_v2(Bucket=idrive_bucket_name)
    response_synology = synology_client.list_objects_v2(Bucket=synology_bucket_name)

    weekly_files_idrive = [file['Key'] for file in response_idrive['Contents'] if 'Weekly' in file['Key']]
    daily_files_idrive = [file['Key'] for file in response_idrive['Contents'] if 'Daily' in file['Key']]

    weekly_files_synology = [file['Key'] for file in response_synology['Contents'] if 'Weekly' in file['Key']]
    daily_files_synology = [file['Key'] for file in response_synology['Contents'] if 'Daily' in file['Key']]

    #IDrive
    if (len(weekly_files_idrive) > MAX_WEEKLY_BACKUPS):
            
            sorted_weekly_files = sorted(weekly_files_idrive, key=lambda x: response_idrive['Contents'][weekly_files_idrive.index(x)]['LastModified'])
            oldest_weekly_file = sorted_weekly_files[0]
            
            idrive_client.delete_object(Bucket=idrive_bucket_name, Key=oldest_weekly_file)
            print(f"IDRIVE: Oldest weekly file '{oldest_weekly_file}' has been deleted.")

    if (len(daily_files_idrive) > MAX_DAILY_BACKUPS):
            sorted_daily_files = sorted(daily_files_idrive, key=lambda x: response_idrive['Contents'][daily_files_idrive.index(x)]['LastModified'])
            oldest_daily_file = sorted_daily_files[0]

            idrive_client.delete_object(Bucket=idrive_bucket_name, Key=oldest_daily_file)
            print(f"IDRIVE: Oldest daily file '{oldest_daily_file}' has been deleted.")

    #Synology
    if (len(weekly_files_synology) > MAX_WEEKLY_BACKUPS):
            
            sorted_weekly_files = sorted(weekly_files_synology, key=lambda x: response_idrive['Contents'][weekly_files_synology.index(x)]['LastModified'])
            oldest_weekly_file = sorted_weekly_files[0]
            
            synology_client.delete_object(Bucket=synology_bucket_name, Key=oldest_weekly_file)
            print(f"SYNOLOGY: Oldest weekly file '{oldest_weekly_file}' has been deleted.")

    if (len(daily_files_synology) > MAX_DAILY_BACKUPS):
            sorted_daily_files = sorted(daily_files_synology, key=lambda x: response_idrive['Contents'][daily_files_synology.index(x)]['LastModified'])
            oldest_daily_file = sorted_daily_files[0]

            synology_client.delete_object(Bucket=synology_bucket_name, Key=oldest_daily_file)
            print(f"SYNOLOGY: Oldest daily file '{oldest_daily_file}' has been deleted.")




    



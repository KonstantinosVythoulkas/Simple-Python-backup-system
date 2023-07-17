import upload
import delete
import shutil
import os
import datetime
import zipfile
import schedule
import time
import yaml
from idrive_client_id import idrive_id
from synology_client_id import synology_id



SETTINGS_FILE = 'settings.yml'
previous_timestamp = None
setup_data = {}



def read_settings_file(file_path):
    with open(file_path, 'r') as file:
        setup_data = yaml.safe_load(file)
    return setup_data

def check_settings_file_modification(file_path):
    global previous_timestamp, setup_data
    current_timestamp = os.path.getmtime(file_path)
    if current_timestamp != previous_timestamp:
        # File has been modified, read and update setup_data
        setup_data = read_settings_file(file_path)
        previous_timestamp = current_timestamp

setup_data = read_settings_file(SETTINGS_FILE)

previous_timestamp = os.path.getmtime(SETTINGS_FILE)

def update_variables():
    global SOURCEFOLDERS, DAILY_DESTINATIONFOLDER, WEEKLY_DESTINATIONFOLDER, MAX_DAILY_BACKUPS, MAX_WEEKLY_BACKUPS
    setup_data = read_settings_file(SETTINGS_FILE)

    SOURCEFOLDERS = setup_data['source_folders']['folders']
    DAILY_DESTINATIONFOLDER = setup_data['destination_folders']['daily']
    WEEKLY_DESTINATIONFOLDER = setup_data['destination_folders']['weekly']
    MAX_DAILY_BACKUPS = setup_data['store_limits']['max_daily_backups']
    MAX_WEEKLY_BACKUPS = setup_data['store_limits']['max_weekly_backups']

    



def backup_folders(source_folders, destination_folder, info):


    # Create a timestamped 
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_folder_name = f"{info}_backup_{timestamp}"
    backup_folder_path = os.path.join(destination_folder, backup_folder_name)
    
    # Create  backup folder
    os.makedirs(backup_folder_path)
    
    # Move files from source folders to backup folder
    for source_folder in source_folders:
        for root,  _, files in os.walk(source_folder):
            for file in files:
                source_path = os.path.join(root, file)
                destination_path = os.path.join(backup_folder_path, os.path.relpath(source_path, source_folder))
                shutil.copy2(source_path, destination_path)
    
    # Create a zip file
    zip_file_path = os.path.join(destination_folder, f"{info}_backup_{timestamp}.zip")
    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(backup_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                archive_path = os.path.relpath(file_path, backup_folder_path)
                zipf.write(file_path, archive_path)
    
    print(f"Backup created {zip_file_path}")
    upload.upload_file_to_idrive(zip_file_path, setup_data['cloud_bucket']['idrive_bucket_name'], setup_data['cloud_bucket']['synology_bucket_name'], setup_data['cloud_switch']['idrive'], setup_data['cloud_switch']['synology'])
    
    delete.count_files(setup_data['cloud_bucket']['idrive_bucket_name'],setup_data['cloud_bucket']['synology_bucket_name'],MAX_WEEKLY_BACKUPS,MAX_DAILY_BACKUPS)

    # Remove folder
    shutil.rmtree(backup_folder_path)
    
    # Remove oldest backup
    backups = sorted(os.listdir(destination_folder))
    if not setup_data['local_copy']:
        os.remove(zip_file_path)
        print(f"Zip file removed from local disk '{zip_file_path}'")
    else:
        if info == "Daily" and len(backups) > MAX_DAILY_BACKUPS:
            oldest_backup = backups[0]
            oldest_backup_path = os.path.join(destination_folder, oldest_backup)
            os.remove(oldest_backup_path)
            print(f"Oldest daily backup '{oldest_backup}' has been removed.")
        elif info == "Weekly" and len(backups) > MAX_WEEKLY_BACKUPS:
            oldest_backup = backups[0]
            oldest_backup_path = os.path.join(destination_folder, oldest_backup)
            os.remove(oldest_backup_path)
            print(f"Oldest weekly backup '{oldest_backup}' has been removed.")

def daily_backup():
    update_variables()
    source_folders = SOURCEFOLDERS
    destination_folder = DAILY_DESTINATIONFOLDER
    backup_folders(source_folders, destination_folder, "Daily")

def weekly_backup():
    update_variables()
    source_folders = SOURCEFOLDERS
    destination_folder = WEEKLY_DESTINATIONFOLDER
    backup_folders(source_folders, destination_folder, "Weekly")


# Set the initial timestamp of the settings file

# Schedule the daily backup to run at a specific time
#schedule.every().day.at("12:00").do(daily_backup)
schedule.every(20).seconds.do(daily_backup)
# Schedule the weekly backup to run every Monday at 12:00
schedule.every().monday.at("12:00").do(weekly_backup)
#schedule.every(20).seconds.do(weekly_backup)

# Perform  backup
daily_backup()
weekly_backup()


# Keep  script running
while True:
    

    check_settings_file_modification(SETTINGS_FILE)
    

    schedule.run_pending()

    time.sleep(1)

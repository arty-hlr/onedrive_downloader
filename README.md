# OneDrive Downloader

Fast solution to download a whole OneDrive, or only specific folders from it. Using [OneDriveSDK Python](https://github.com/OneDrive/onedrive-sdk-python).

You must first create an app with Azure and generate a secret from it ([docs here](https://docs.microsoft.com/en-us/onedrive/developer/rest-api/getting-started/?view=odsp-graph-online)), and paste the ID and secret into the script.

Currently possibility to choose folders to blacklist or whitelist, and recovery mode by storing the ID of the last item downloaded to continue downloading exactly where you left off.

# TO DO
+ Pass arguments (folders etc) to script

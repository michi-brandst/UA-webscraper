# Unearted Arcana webscraper

A simple python script to check for new releases of [Uneathed Arcana](https://dnd.wizards.com/articles/unearthed-arcana) from Wizards of the Coast for Dungeons and Dragons 5th Edition.
The releases will be compared with the PDFs already present in the shared folder of our Nextcloud instance. New releases will be downloaded, named correctly and posted to the folder. 
Additionally, a message will be posted in the notifications channel of our Discord server if a new PDF is available via a webhook. The script will be called via a crontab on one of our Raspberry Pi devices.
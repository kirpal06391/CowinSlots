Make following changes before running the code:
1. Change district_id on Line 5 in getVaccineStatus.sh file.
2. Change Line 22 & 54 in getSlotAlert.py with event of IFTTT applet and webhook_key from IFTTT webhook service

After making above changes you can setup a cron to run python3 {path_to_this_folder}/getSlotAlert.py every 15 minutes, 1 hour etc. as per your liking.

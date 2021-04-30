# email_attachments
This python script helps you downloading all the attachments inside your inbox

To use this script, consider folowing the steps below :

step 1: dowload and unzip the project

step 2:  update the configuration file config.ini with your own credentials

step 3: run the script imap.py with the python command : py imap.py

step 4: when the execution is finished , dive in to the "attachments" folder and get all your attachments that have been downloaded.

NB: if your want to download only the attachments of unseen messages , consider updating the line 36 with this : "typ, data = imap.search(None, "UNSEEN")





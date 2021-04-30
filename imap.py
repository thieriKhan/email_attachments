import email
import imaplib
import os
from configparser import ConfigParser
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent


def main(user, imap_server, imap_user, imap_pass):

    imap = None
    print(f"\n \t please wait while finding to the mail server  for {user} ... \n")
    try:
        imap = imaplib.IMAP4_SSL(imap_server)
    except Exception as e:
        print(f"there is a probleme with the imap address for {user} or the connection may be bad.\n the error code is : {e}")
        exit()

    print("\n\t the server has been reached \n")
    print("\n \t please wait while connecting to the mail server ...")
    ## login to server

    try:
        imap.login(imap_user, imap_pass)
    except Exception as e:
        print(f"{user} credentials are not valid  and the error type is: {e}")
        exit()
    print("\n your are now connected ")

    ##login completed


    imap.select('Inbox')

    typ, data = imap.search(None, "ALL")

    if typ != "OK":
        print("there was an error while searching for the emails")
        raise

    if not len(data[0]):
        print("there is no unseen message")
        exit()
    for num in data[0].split():
        typ, data = imap.fetch(num, '(RFC822)')


        if (typ != "OK"):
            print(f"there was a problem while fetching the mail : {num} for {user}")
            raise
        messages = email.message_from_bytes(data[0][1])
        sender = messages['from'].replace(" ", "_").replace("<","" ).replace(">", "")


        for part in messages.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            os.makedirs(os.path.join(BASE_DIR,'attachments', user, sender), exist_ok=True)
            if bool(filename):
                filePath = os.path.join(BASE_DIR, 'attachments', user, sender, filename)
                if not os.path.isfile(filePath):
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))

    print("\n the files have successfuly downloaded")


if __name__ == '__main__':
    print(BASE_DIR)
    if  not os.path.isfile(os.path.join(BASE_DIR,'config.ini')) :
        cfFile = open(os.path.join(BASE_DIR,'config.ini'), 'x')
        cfFile.write("[user1]/n Imap_Server = outlook.com  email = khansappi@outlook.com /n password = bonjour16TOI@gmail.com")

    config = ConfigParser()
    config.read('config.ini')

    for user in config.sections():
        main(user, config.items(user)[0][1], config.items(user)[1][1], config.items(user)[2][1])


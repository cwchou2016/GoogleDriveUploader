#!/usr/bin/python

import os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def GetFolderID(dname, parents_id):
    '''
    Search directory name under a folder and return its id
    '''
    file_list = drive.ListFile(
        {'q': "title='{}' and '{}' in parents and trashed=False".format(
            dname, parents_id)}).GetList()
    if file_list:
        print "Folder {} exists".format(dname)
        folder_id = file_list[0]['id']
    else:
        folder = drive.CreateFile({'title': dname,
                                   'parents': [{'id': parents_id}],
                                   'mimeType':
                                   'application/vnd.google-apps.folder'})
        folder.Upload()
        folder_id = folder['id']
        print "Folder {} created".format(dname)

    return folder_id


def GetRootID():
    '''
    Return root id
    '''
    file_iter = drive.ListFile({'q': '"root" in parents and trashed=false',
                                'maxResults': 10})
    for file_list in file_iter:
        for f in file_list:
            if f['parents'][0]['isRoot']:
                return f['parents'][0]['id']


def GetPathID(r_path, parents_id):
    '''
    Search a path under a folder and return its id
    '''
    dname = r_path.split("/")
    for d in dname:
        if d != "":
            parents_id = GetFolderID(d, parents_id)
    return parents_id


def Update(file_path, parents_id):
    '''
    Upload a file under a folder
    '''
    root, fname = os.path.split(file_path)
    file_list = drive.ListFile(
        {'q': 'title="{}" and "{}" in parents and trashed=False'.format(
            fname, parents_id)}).GetList()
    if file_list:
        print "File {} exists".format(fname)
    else:
        file1 = drive.CreateFile({'title': fname,
                                  'parents': [{'id': parents_id}]})
        # can't upload empty files, set empty file's content as " "
        if os.stat(file_path).st_size != 0:
            file1.SetContentFile(file_path)
        else:
            print "File {} is empty".format(fname)
            file1.SetContentString(" ")
        file1.Upload()
        print "File {} uploaded".format(fname)


def KeepTrying(num, func, **kwargs):
    '''
    Retry function(func) for num times with its argument(**kwargs)
    '''
    if num <= 0:
        msg = "num error"
        return msg
    else:
        while (num > 0):
            try:
                f = func(**kwargs)
                return f
            except Exception as e:
                print "Error: {}, retrying....".format(e)
                num -= 1
        else:
            return e



print "Autherizting..................",
gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("/home/pi/mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("/home/pi/mycreds.txt")

drive = GoogleDrive(gauth)

print "Done"

# Sync local folder
HOME_DIR = '/home/pi/New'

# folder id of sync google drive folder
root_id = "0B4Q9hJD-SUamcm5CV1FzcFhYWjQ"  # drive/pi

os.chdir(HOME_DIR)

for root, dirs, files in os.walk(os.getcwd()):
    r_path = root.split(HOME_DIR)[1]
    path_id = KeepTrying(10, GetPathID, r_path=r_path, parents_id=root_id)

    for fname in files:
        file_path = os.path.join(root, fname)
        msg = KeepTrying(10, Update, file_path=file_path, parents_id=path_id)
        if msg is not None:
            print msg


print "Upload complete"

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os


def GetFolderID(dname, parents_id):
    file_list=drive.ListFile({'q':"title='{}' and '{}' in parents and trashed=False".format(dname, parents_id)}).GetList()
    if file_list:
        print "Folder {} exists".format(dname)
        folder_id=file_list[0]['id']
    else:
        folder=drive.CreateFile({'title':dname,
                                'parents':[{'id':parents_id}],
                                'mimeType':'application/vnd.google-apps.folder'})
        folder.Upload()
        folder_id=folder['id']
        print "Folder {} created".format(dname)

    return folder_id

def GetPathID(r_path, parents_id):
    dname=r_path.split("/")
    for d in dname:
        if d!="":
            parents_id=GetFolderID(d, parents_id)
    return parents_id
        

def Update(file_path, parents_id):
    root, fname=os.path.split(file_path)
    file_list=drive.ListFile({'q':"title='{}' and '{}' in parents and trashed=False".format(fname, parents_id)}).GetList()
    if file_list:
        print "File {} exists".format(fname)
    else:
        file1=drive.CreateFile({'title':fname,
                                'parents':[{'id':parents_id}]})
        # can't upload empty files, set empty file's content as " "
        if os.stat(file_path).st_size!=0:
            file1.SetContentFile(file_path)
        else:
            print "File {} is empty".format(fname)
            file1.SetContentString(" ")
        file1.Upload()
        print "File {} uploaded".format(fname)



gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")
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
gauth.SaveCredentialsFile("mycreds.txt")

drive=GoogleDrive(gauth)

HOME_DIR='/home/pi/New'
root_id='0B4Q9hJD-SUamcm5CV1FzcFhYWjQ'

os.chdir(HOME_DIR)

for root, dirs, files in os.walk(os.getcwd()):
    r_path=root.split(HOME_DIR)[1]
    path_id=GetPathID(r_path, root_id)
    for fname in files:
        file_path=os.path.join(root, fname)
        Update(file_path, path_id)
        

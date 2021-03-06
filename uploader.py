#!/usr/bin/python

import os

import httplib2
from apiclient import discovery
from apiclient.http import MediaFileUpload

import quickstart
import setting

SCOPE = 'https://www.googleapis.com/auth/drive'
ROOT = setting.ROOT
# ROOT = 'root'  # Google drive folder id
PATH = setting.PATH


class DriveService():
    def __init__(self, scope=SCOPE):
        """Initiating DriveService authorization and
        get root folder ID
        """
        credentials = quickstart.get_credentials(scope)
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('drive', 'v3', http=http)

    def creatfolder(self, fname, parent_id):
        """Create a folder under parent_id

        Return the id of new folder.

        Return:
            folder_id
        """
        metafile = {
            'name': fname,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }

        folder = self.service.files().create(
            body=metafile, fields='id').execute()

        return folder.get('id')

    def getfolderID(self, fname, parent_id=ROOT, create=True):
        """Get the folder ID under a folder.

        create: If the subfolder does not exist, create one.

        Return:
            folder_id
        """
        result = self.service.files().list(
            q=('mimeType="application/vnd.google-apps.folder"' +
               ' and trashed = False' + ' and name="{}"'.format(fname) +
               ' and "{}" in parents'.format(parent_id)),
            fields='files(id)').execute().get('files', [])

        if not result:
            if create:
                return self.creatfolder(fname, parent_id)
            else:
                return None
        elif len(result) == 1:
            return result[0]['id']

    def getpathID(self, r_path, parent_id=ROOT, create=True):
        """Get the relative path ID under a folder.

        create: If the path does not exist, create one.

        Return:
            path_id
        """
        r_path = r_path.split("/")

        for folder in r_path:
            if folder:
                parent_id = self.getfolderID(folder, parent_id, create)
                if parent_id is None:
                    return None

        return parent_id

    def fileondrive(self, fname, parent_id):
        """Check if a file is in a google drive folder

        Return:
            Bool
        """
        result = self.service.files().list(
            q='name = "{}" and trashed = False'.format(fname) +
            ' and "{}" in parents'.format(parent_id),
            fields="files(name, id, mimeType, parents)").execute().get(
                'files', [])

        if result:
            print "{} exists".format(fname)
            return True
        else:
            print '{} was not found, preparing upload'.format(fname)
            return False

    def getlocalfiles(self, path=PATH):
        '''Get all files and folders in PATH

        Return:
            file_dict
        '''
        file_dict = {'local': [], 'upload': []}
        for root, folder, files in os.walk(path):
            r_path = root.split(PATH)[1]
            for f in files:
                file_dict['local'].append((r_path, f))

                folder_id = self.getpathID(r_path)

                if self.fileondrive(f, folder_id) is False:
                    file_dict['upload'].append((os.path.join(root, f),
                                                folder_id))
        return file_dict

    def upload(self, file_r_path, parent_id):
        """Upload a file to google drive

        Return:
            None
        """
        fname = os.path.split(file_r_path)[1]

        metadata = {"name": fname, "parents": [parent_id]}

        mbody = MediaFileUpload(file_r_path, resumable=True)
        f = self.service.files().create(
            body=metadata, media_body=mbody).execute()

        print "{}......................Complete\n".format(f['id'])


def test_authorization():
    service = DriveService()

    results = service.service.files().list(
        pageSize=10,
        fields="nextPageToken, files(parents,id, name)").execute()

    items = results.get('files', [])

    if not items:
        print "No files found."
    else:
        print('Files:')

        for item in items:
            print "{}, ({})".format(item['name'], item['id'])


if __name__ == '__main__':
    #  test_authorization()
    #  print "test OK"

    service = DriveService()

    os.chdir(PATH)
    print "The following directory is going to upload to google drive:"
    print os.getcwd()

    for root, folder, files in os.walk(PATH):
        r_path = root.split(PATH)[1]
        for f in files:
            folder_id = service.getpathID(r_path)

            if service.fileondrive(f, folder_id) is False:
                f_path = os.path.join(root, f)
                service.upload(f_path, folder_id)

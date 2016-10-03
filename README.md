# GoogleDriveUploader
Python script of Google drive uploader for raspberry pi. <br>
It's based on pydrive. https://github.com/googledrive/PyDrive

### UPDATES
* **2016-09-14 UPDATE** <br>
  Httplib2 error keeps showing up from time to time.
  It's assumed to be caused by unstable wifi connection of raspberry pi 3.
  So a stupid "try and except" method was used to avoid this error.

### NOTES
* Authentication: https://googledrive.github.io/PyDrive/docs/build/html/quickstart.html
* [settings.yaml](/yaml_setting/settings.yaml) for auto refresh toaken and save credential


# GoogleDriveUploader
Python script of Google drive uploader for raspberry pi. <br>
It's based on [pydrive](https://github.com/googledrive/PyDrive).

### UPDATES
* **2016-09-14 UPDATE** <br>
  Httplib2 error keeps showing up from time to time.
  I assumed it's caused by the unstable wifi connection of raspberry pi 3.
  So I used a simple "try and except" method to avoid this error.
  Hoping other people have better solutions.

### NOTES
* Authentication: https://googledrive.github.io/PyDrive/docs/build/html/quickstart.html
* [settings.yaml](/yaml_setting/settings.yaml) for auto refresh toaken and save credential


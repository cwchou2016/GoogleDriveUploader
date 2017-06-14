# GoogleDriveUploader
Python script of Google drive uploader for raspberry pi. <br>

Create setting.py:

    # Local directory to upload
    PATH=       # your value
    
    # Google drive folder id
    ROOT=       # your value
   

### UPDATES
* *82017-06-14 UPDATE** <br>
  Fix bugs
  Use setting.py to assign values
  
* **2017-06-11 UPDATE** <br>
  Rewrite with Google Drive API v3
  
* **2016-09-14 UPDATE** <br>
  Httplib2 error keeps showing up from time to time.
  I assumed it's caused by the unstable wifi connection of raspberry pi 3.
  So I used a simple "try and except" method to avoid this error.
  Hoping other people have better solutions.

### NOTES



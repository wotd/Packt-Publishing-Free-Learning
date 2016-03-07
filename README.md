## Free Learning PacktPublishing scripts

**grabPacktFreeBook.py** - script that automatically grabs a daily free eBook from https://www.packtpub.com/packt/offers/free-learning

**downloadPacktFreeBooks.py** - script which downloads already claimed eBooks from your account "https://www.packtpub.com/account/my-ebooks"

### Requirements:
* Install Python 3.x
* Install pip (if you have not it installed yet)
  To install pip, download:  https://bootstrap.pypa.io/get-pip.py ,
  then run the following commands:
  ```  
  python get-pip.py
  pip install requests
  pip install beautifulsoup4
  ```
* change your login credentials in **loginData.cfg** file
  
### Usage:
**[grabPacktFreeBook.py]**
* You can manually run grabPacktFreeBook.py script to get the book
  ```sh
  $ python grabPacktFreeBook.py
  ```
* Or set it to be invoked automatically:  
  **LINUX**:
  modify access permissions of the script:  
  ```sh
  $ chmod a+x grabPacktFreeBook.py 
  ```
  CRON setup (more: https://help.ubuntu.com/community/CronHowto) :
  ```sh
  $ sudo crontab -e
  ```
  paste (modify all paths correctly according to your setup):
  ```
  0 12 * * * cd /home/me/Desktop/PacktScripts/ && /usr/bin/python3 grabPacktFreeBook.py > /home/me/Desktop/PacktScripts/grabPacktFreeBook.log 2>&1
  ```
  and save the crontab file. To verify if CRON fires up the script correctly, run a command:
  ```sh
  $ sudo grep CRON /var/log/syslog
  ```
  **WINDOWS**:



**[downloadPacktFreeBooks.py]**
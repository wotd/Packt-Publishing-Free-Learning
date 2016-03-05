# FreeLearningPacktPublishing_UsefulScripts

#grabPacktFreeBook.py 
[script that automatically grabs a daily free eBook from](https://www.packtpub.com/packt/offers/free-learning)

### Requirements
* Install Python 3.x
* Install pip (if you don't have it yet)
  to install pip, download:  https://bootstrap.pypa.io/get-pip.py 
  then run the following:    python get-pip.py
* run:                       pip install requests
* change your login credentials in #loginData.cfg file
  
### Usage
* you can manually run #grabPacktFreeBook.py script to get the book
* LINUX:
  #chmod a+x grabPacktFreeBook.py 
  Cron setup:
  #0 12 * * * cd /home/GrabBookCatalog/ && /usr/bin/python grabPacktFreeBook.py > /tmp/packt_free_ebook.log>&1
  All paths must be correct!
* WINDOWS:
  

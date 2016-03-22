@echo off
echo *** Grabbing free eBook from Packt Publishing.... ***
rem If you want to log downloading history, just remove rem
rem echo ***Date: %DATE:/=-% [%TIME::=:%] *** >> grabPacktFreeBook.log
rem python grabPacktFreeBook.py >> grabPacktFreeBook.log 2>&1
rem echo:
rem echo:>> grabPacktFreeBook.log
python grabPacktFreeBook.py 
echo *** Done ! ***
pause
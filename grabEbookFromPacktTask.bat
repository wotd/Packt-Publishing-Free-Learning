echo *** Grabbing free eBook from Packt Publishing.... ***
echo ***Date: %DATE:/=-% [%TIME::=:%] *** >> grabPacktFreeBook.log
python grabPacktFreeBook.py >>grabPacktFreeBook.log 2>&1
echo:
echo *** Done ! ***
echo:>> grabPacktFreeBook.log
pause
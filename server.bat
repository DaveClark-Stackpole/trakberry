@ echo off
echo This is execuing local server for deployment!
cd /d "c:\Programs\local"
python manage.py runserver 127.0.0.1:8080 --insecure

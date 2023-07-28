echo " BUILD STARTING... "
python3.9 -m pip install -r requirements.txt
python3.9 manage.py migrate --clear
python3.9 manage.py makemigrations store --clear
python3.9 manage.py collectstatic --noinput --clear
echo " BUILD ENDING "
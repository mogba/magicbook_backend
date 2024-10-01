# build_files.sh
cd ..
pip install -r requirements.txt
python3.11.1 manage.py collectstatic --noinput
cd scripts

# generate_swagger_schema.sh
cd ..
python manage.py spectacular --color --file schema.yml
cd scripts

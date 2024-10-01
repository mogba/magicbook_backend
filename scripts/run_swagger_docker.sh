# run_swagger_docker.sh
cd ..
docker run -p -d 80:8080 -e SWAGGER_JSON=/schema.yml -v ${PWD}/schema.yml:/schema.yml swaggerapi/swagger-ui
cd scripts

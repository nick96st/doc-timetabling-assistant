

FOLDER STRUCTURE

BACKEND
1) the folder doc_ta is top level django project folder
2) doc_ta/doc_ta is the location of settings and master url settings(Others are default lauch Django stuff)
3) doc_ta/ta_main is the app folder for the main features of timetabling assistant
3.1)Migrations - just a migration files created during the Dev process(Can be deleted and run Django makemigrations to make into a single file)
3.2)Templates - just our index.html file
3.3) Tests folders
3.4) apps.py, urls.py (autogenerated)
3.5) asp_code_generator.py,asp_constraints,asp_manipulators.py,models.py,views.py,admin.py - CORE DEVELOPMENT PRODUCT OF BACKEND

Some Files
1) requirements.txt - holds all the python dependencies and installed libs
2) update_dependencies.sh - run this to update the requirements.txt after a new pip install
3) run_server.sh - it is the script that will execute using the command docker-compose up
                 should apply migrations to database
4) install_dependencies.sh - this is used by docker to have the proper python dependencies
5) manage.py (script that runs all django comands - autogenerated)

FRONTEND
- Typical app(js files)/css(css files) folders
- Webpack and npm settings files

OTHER
clingo tar.gz - Official download from the website
docker-compose.yml
Dockerfile
get-pip.py - File to get pip installed so if you add new python deps to able to forge a new requirements.txt(check pip freeze)
travis.yml
.gitignore

asp - the folder that contains extracted clingo[blabla].tar.gz

RUNNING DJANGO COMMANDS IN DOCKER
1)from root folder run: "sudo docker-compose run web Backend/doc_ta/manage.py [command] " which is equiv to "python manage.py [command]" in Django tutorials

RUNNING TESTS IN DOCKER
1) from root run : sudo docker-compose run web Backend/doc_ta/manage.py test
2) if u want only some tests run check how it is done in Django(for example run:[whole command] ta_main.tests.test_asp_manipulators_tests)

RUNNING SERVER ON VM
At the moment the settings only lauches a "localhost" server - you need to add few settings to be accessable on DoC VM
1) Set the ALLOWED_HOSTS to ["YOUR-VM-IP"]
2) Change the setting in docker-compose that the server is 127.0.0.1:80 not 8000 and the port setting from 8000:8000 to 80:80
3) Make sure you got the Clingo stuff extracted in asp folder
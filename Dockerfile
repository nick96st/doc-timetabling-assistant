FROM python:2.7

# Set working directory to /app
WORKDIR /app

# Copy current directory contents into the container at /app
ADD . /app

# Install all needed packages in requirements.txt
RUN pip install -r Backend/requirements.txt
RUN wget https://netcologne.dl.sourceforge.net/project/potassco/clingo/4.5.4/clingo-4.5.4-linux-x86_64.tar.gz
ADD clingo-4.5.4-linux-x86_64.tar.gz /app

# Expose port 80 for webapp
EXPOSE 80

# Define environment variable
#ENV NAME World
#RUN python Backend/doc_ta/manage.py makemigrations
#RUN python Backend/doc_ta/manage.py migrate
#RUN mkdir docker-entrypoint-init-db.d
#ADD ./init.sql /docker-entrypoint-init-db.d/init.sql # adds the sql user/db creation script to specific docker folder
#ENV POSTGRES_DB doctimetable_default_db
#ENV POSTGRES_USER foofighter
#ENV POSTGRES_PASSWORD dleifynot

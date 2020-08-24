# JustTestTornadoPlusWsagger
You must have PostgreSQL installed to run this demo.

1. Install a database if needed

2. Install Python prerequisites
    with `pip -r requirements.txt`

3. Create a database and user, and grant permissions:
   CREATE DATABASE document;
   CREATE USER document WITH PASSWORD 'document';
   GRANT ALL ON DATABASE document TO document;

4.
http://localhost:8888/api/doc

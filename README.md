# Text Search Engine

Test job

#### Stack:

- [Python](https://www.python.org/downloads/)
- [FastApi](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Elasticsearch](https://www.elastic.co/)

## Local Developing

All actions should be executed from the source directory of the project and only after installing all requirements.

1. Firstly, create and activate a new virtual environment:
   ```bash
   python -m venv ../venv
   source ../venv/bin/activate
   ```

2. Install packages:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Launch PostgreSQL and create a database.

4. [Install Elasticsearch with Docker](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html).

5. Copy the http_ca.crt security certificate from your Docker container to your local machine:
   ```bash
   docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt .
   ```
6. Create .env and add environment variables
7. Import test data and create an index in elasticsearch
   ```bash
   python import_data.py
   ```
8. Run:
   ```bash
   uvicorn src.main:app --reload
   ```
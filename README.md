# Text Search Engine

#### Stack:

- [Python](https://www.python.org/downloads/)
- [FastApi](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Elasticsearch](https://www.elastic.co/)

## Running with Docker Compose

All actions should be executed from the source directory of the project.

1. Start docker:
   ```bash
   docker compose build
   docker compose up
   ```

2. Waiting for all containers to start and for elasticsearch to finally start.
3. Run the bash terminal process in the running fastapi_app container:
   ```bash
   docker exec -it fastapi_app bash
   ```
4. Importing data into databases inside a container:
   ```bash
   python import_data.py
   ```
   
## Local Developing and Testing

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

5. Create .env and add environment variables
6. Import test data and create an index in elasticsearch
   ```bash
   python import_data.py
   ```
7. Run:
   ```bash
   uvicorn src.main:app --reload
   ```
8. Testing:
   ```bash
   pytest -s -v tests/
   ```
# Text Search Engine

Test job

#### Stack:

- [Python](https://www.python.org/downloads/)
- [FastApi](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Elasticsearch](https://www.elastic.co/)

## Local Developing

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
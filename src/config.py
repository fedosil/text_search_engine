from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

DB_TEST_HOST = os.environ.get("DB_TEST_HOST")
DB_TEST_PORT = os.environ.get("DB_TEST_PORT")
DB_TEST_NAME = os.environ.get("DB_TEST_NAME")
DB_TEST_USER = os.environ.get("DB_TEST_USER")
DB_TEST_PASS = os.environ.get("DB_TEST_PASS")
#
ES_PASS = os.environ.get("ES_PASS")
ES_USER = os.environ.get("ES_USER")
ES_HOST = os.environ.get("ES_HOST")
ES_PORT = os.environ.get("ES_PORT")
ES_PATH_CA_CERTS = os.environ.get("ES_PATH_CA_CERTS")

ES_TEST_PASS = os.environ.get("ES_TEST_PASS")
ES_TEST_USER = os.environ.get("ES_TEST_USER")
ES_TEST_HOST = os.environ.get("ES_TEST_HOST")
ES_TEST_PORT = os.environ.get("ES_TEST_PORT")
ES_TEST_PATH_CA_CERTS = os.environ.get("ES_TEST_PATH_CA_CERTS")


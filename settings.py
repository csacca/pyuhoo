from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

USERNAME = getenv("USERNAME")
PASSWORD = getenv("PASSWORD")

from pyspark.sql import SparkSession
from glob import glob
import logging
import os
from boto3.session import Session
from dotenv import load_dotenv

load_dotenv()
ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

session = Session(aws_access_key_id=ACCESS_KEY,
                  aws_secret_access_key=SECRET_KEY)
s3 = session.resource('s3')

class SilverTransformation:
    """
    This class is responsible to extract all data from OpenBreweryDB API
    """

    def __init__(self):
        self.logger = logging.getLogger("Bronze to Silver")
        logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
        self.spark = SparkSession.builder.getOrCreate()

    @staticmethod
    def formatted_source_paths():
        return [file.replace('\\', "/") for file in glob("data/bronze/*")]

    def read_from_bronze(self):
        try:
            df = self.spark.read.json(self.formatted_source_paths(), multiLine=True)
        except Exception as e:
            self.logger.error(e)
            raise
        return df

    def load(self):
        self.read_from_bronze().show()


SilverTransformation().load()

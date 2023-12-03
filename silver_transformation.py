from pyspark.sql import SparkSession
from pyspark.sql.functions import trim
from glob import glob
import logging


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
        return [file.replace('\\', "/") for file in glob("/data/bronze/*")]

    def read_from_bronze(self):
        try:
            self.logger.info(f"reading data from {self.formatted_source_paths()}")
            df = self.spark.read.json(self.formatted_source_paths(), multiLine=True)
        except Exception as e:
            self.logger.error(e)
            raise
        return df

    def load(self):
        df = self.read_from_bronze()
        assert df.count() > 0, "Nothing to process"
        try:
            df = df.withColumn("country", trim(df.country))
            df = df.withColumn("state", trim(df.state))
            df.write.partitionBy("country", "state").mode("overwrite").parquet("/data/silver")
        except Exception as e:
            self.logger.error(e)


if __name__ == '__main__':
    SilverTransformation().load()

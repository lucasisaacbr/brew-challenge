from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import trim
import logging


class GoldTransformation:
    def __init__(self):
        self.logger = logging.getLogger("Bronze to Silver")
        logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
        self.spark = SparkSession.builder.getOrCreate()

    def read_from_silver(self, partition: dict = {"country": "*", "state": "*"}):
        df = self.spark.read.parquet(f"/data/silver/country={partition.get('country')}/state={partition.get('state')}")
        df = df.select("brewery_type", "brewery_country", "brewery_state")
        df.createOrReplaceTempView("breweries")
        return df

    def get_quantity_of_stores_per_type_and_location_sql(self):
        df = self.spark.sql("""
            SELECT brewery_type, count(*) AS total,  brewery_country, brewery_state 
            FROM breweries
            GROUP BY brewery_type,  brewery_country, brewery_state
            ORDER BY 3,4,2
        """)
        df.createOrReplaceTempView("breweries_agg")
        return df

    def print_data_for_each_country(self):
        countries = [row.brewery_country for row in
                     self.spark.sql("""SELECT distinct brewery_country FROM breweries""").collect()]

        for country in countries:
            self.logger.info(f" ### Showing results for {country} ### ")
            self.spark.sql(f"""
                SELECT * 
                FROM breweries_agg
                WHERE brewery_country = '{country}'
                ORDER BY 3,4,2
            """).show()

    def load(self):
        df = self.read_from_silver()
        assert df.count() > 0, "Nothing to process"

        try:
            result = self.get_quantity_of_stores_per_type_and_location_sql()
        except Exception as e:
            self.logger.error(e)

        self.print_data_for_each_country()

        # Again partitionBy will the column from the dataframe, duplicating it. 
        result = df.withColumn("country", trim(df.brewery_country))
        result = df.withColumn("state", trim(df.brewery_state))
        result.write.partitionBy("brewery_country", "brewery_state").mode("overwrite").parquet("/data/gold")
        self.logger.info("Job Completed Successfully!")


if __name__ == '__main__':
    GoldTransformation().load()

import requests
import logging
from math import ceil
import json


class BronzeExtraction:
    """
    This class is responsible for extracting all data from the OpenBreweryDB API.
    """

    def __init__(self):
        self.logger = logging.getLogger("BreweryAPI to Bronze")
        logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

    def pages_to_look_up(self, per_page):
        """
        Define how many pages to look up to get the full data from API.
        :param per_page: number of records. Max of 200 based on API docs.
        :return:
        """
        try:
            r = requests.get('https://api.openbrewerydb.org/v1/breweries/meta')
            assert r.status_code == 200, "API Status Code different than 200"
            api_result = r.json()
            total_of_breweries = api_result.get('total')
            assert total_of_breweries is not None, f"Something wrong with API call response: {total_of_breweries}"
            return ceil(int(total_of_breweries) / per_page)
        except Exception as e:
            self.logger.error(e)
            raise

    def get_data_from_api(self):
        pages = self.pages_to_look_up(per_page=200)
        for page in range(1, pages + 1):
            try:
                r = requests.get(f'https://api.openbrewerydb.org/v1/breweries?page={page}&per_page=200')

                assert r.status_code == 200, "API Status Code different than 200"
                self.logger.info(f"Starting to record file: /data/bronze/breweries_page_{page}.json")
                out_file = open(f"/data/bronze/breweries_page_{page}.json", "w")
                json.dump(r.json(), out_file, sort_keys=True, indent=4)
                out_file.close()

            except FileNotFoundError as e:
                self.logger.error(e)
                raise
        self.logger.info("Job Completed Successfully!")


if __name__ == '__main__':
    BronzeExtraction().get_data_from_api()

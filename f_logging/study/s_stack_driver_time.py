from google.cloud import logging
# from loguru import logger
import datetime


start = datetime.datetime.now()

json_key = 'd:\\professor\\gcp\\stack_driver.json'

client = logging.Client.from_service_account_json(json_key)
logger = client.logger('stackdriver')
for _ in range(1000):
    logger.log_struct({'a': 1, 'b': 2})
client.close()

finish = datetime.datetime.now()
print(finish - start)

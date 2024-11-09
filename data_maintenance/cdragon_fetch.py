# Intended to be loaded as stand-alone cloud function

from google.cloud import storage
import httpx


CDRAGON_SRC_URL = 'https://raw.communitydragon.org/latest/cdragon/tft/en_us.json'
DST_BUCKET = 'tft_set_data'


def write_to_bucket(bucket_name, file_path, data, mode):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    with bucket.blob(file_path).open(mode, encoding='utf-8') as f:
        f.write(data)


json_data = httpx.get(CDRAGON_SRC_URL).text
write_to_bucket(
    bucket_name=DST_BUCKET, file_path='base_tft_json', data=json_data, mode='wt')

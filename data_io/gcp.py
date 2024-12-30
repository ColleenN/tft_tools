from google.cloud import storage


def read_from_bucket(bucket_name, file_path):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name, timeout=.1, retry=None)
    return bucket.blob(file_path).download_as_string()


def write_to_bucket(bucket_name, file_path, data, mode):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name, timeout=.1, retry=None)
    with bucket.blob(file_path).open(mode, encoding='utf-8') as f:
        f.write(data)

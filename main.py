import os
import subprocess
from datetime import datetime
import boto
from boto.s3.key import Key
from dotenv import load_dotenv

load_dotenv()

# Amazon S3 settings.
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID_2')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY_2')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

DB_USER = os.getenv('DB_USER')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PASS = os.getenv('DB_PASS')

BACKUP_PATH = r'/usr/src/app'

FILENAME_PREFIX = 'myapp.backup'




def upload_to_s3(source_path, destination_filename):
    """
    Upload a file to an AWS S3 bucket.
    """
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(AWS_BUCKET_NAME)
    k = Key(bucket)
    k.key = destination_filename
    k.set_contents_from_filename(source_path)


def main():
    now = datetime.now().strftime("%Y-%m-%d")
    filename = f"dbtest_{now}.sql"
    destination = f"/tmp/{filename}"

    os.system(f"PGPASSWORD={DB_PASS} pg_dumpall --globals-only --no-role-passwords -h {DB_HOST} -U {DB_USER} > {destination}")
    upload_to_s3(destination, filename)
    print (f'Uploading {filename} to Amazon S3...')





if __name__ == '__main__':
    main()
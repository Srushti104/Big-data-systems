from google.cloud import storage
import glob
import os
import pandas as pd
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ''

storage_client = storage.Client()
buckets = list(storage_client.list_buckets())
bucket = storage_client.get_bucket("sevir-306302")


def upload_csv_storm():
    blob = bucket.blob('Storm/StormEvents_fatalities.csv')
    blob.upload_from_filename('C:/Users/gnana/OneDrive/Desktop/Stormdata/StormEvents_locations/StormEvents_fatalities-ftp_v1.0_d2019_c20210223.csv')
    print('Storm data uploaded')


def upload_csv_catalog():
	csv_files = glob.glob("C:/Users/gnana/OneDrive/Desktop/Catalog/*.csv")
	for csv in csv_files:
		#print(os.path.basename(img))
		blob = bucket.blob('Catalog/'+os.path.basename(csv))
		blob.upload_from_filename('C:/Users/gnana/OneDrive/Desktop/Catalog/'+os.path.basename(csv))
		print('Catalog data uploaded')

upload_csv_storm()
upload_csv_catalog()







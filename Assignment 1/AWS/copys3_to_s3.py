
import boto3
import pandas as pd

s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-1'
)
def copy_to_bucket(bucket_from_name, bucket_to_name, file_name):
    ''' copy files from public s3 to s3  '''
    copy_source = {
        'Bucket': bucket_from_name,
        'Key': file_name
    }
    s3.Object(bucket_to_name, file_name).copy(copy_source)


df=pd.read_csv("https://raw.githubusercontent.com/MIT-AI-Accelerator/eie-sevir/master/CATALOG.csv")

df['time_utc'] = pd.to_datetime(df['time_utc'], format='%Y-%m-%d %H:%M:%S')
df1 = df[df.time_utc.dt.to_period("M") == "2019-01"]
df2 = df1[~df1.id.str.contains('^R')]
df3 = pd.DataFrame({'file_name':df2.file_name.unique()})
print(df3.file_name[0])

''' upload HDF5 files '''
for f in range(len(df3.file_name)):
    print("Uploading file: ", df3.file_name[f])
    copy_to_bucket("sevir", 'dsrushti-1', 'data/'+df3.file_name[f])
    print("Uploaded file: ", df3.file_name[f])

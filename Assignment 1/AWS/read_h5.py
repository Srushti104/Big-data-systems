
import h5py
import s3fs
import os.path
from os import path
import pandas as pd
import matplotlib.pyplot as plt


df=pd.read_csv("https://raw.githubusercontent.com/MIT-AI-Accelerator/eie-sevir/master/CATALOG.csv")

df['time_utc'] = pd.to_datetime(df['time_utc'], format='%Y-%m-%d %H:%M:%S')
df1 = df[df.time_utc.dt.to_period("M") == "2019-01"]
df2 = df1[~df1.id.str.contains('^R')]

df3 = pd.DataFrame({'file_name':df2.file_name.unique()})
df3['file_index'] = [list(set(df2['file_index'].loc[df2['file_name'] == x['file_name']]))
    for _, x in df3.iterrows()]


for f in range(len(df3.file_name)):
    print(df3.file_name[f])
    index = df3.file_index[f]
    print(index)
    img_type = df3.file_name[f].split('/')[0]
    new_file_name = df3.file_name[f].split('/')[-1]
    print(img_type)
    print(new_file_name)

    for i in index:
        fs = s3fs.S3FileSystem(anon=True)
        with fs.open('s3://sevir/data/'+ df3.file_name[f], mode='rb') as f:
            hf = h5py.File(f)
            event_id = hf['id'][i]
            img_type_data = hf[img_type][i]
            print("Read finished: ", i)

            print('Event ID:', event_id)
            print('Image data:', img_type_data)

            # if path.exists("SEVIR_IR069_RANDOMEVENTS_2019_0101_0430_New.h5"):
            #
            # with h5py.File('SEVIR_IR069_RANDOMEVENTS_2019_0101_0430_New.h5', 'a') as hf_new:
            #     hf_new.put('id', data=event_id)
            #     hf_new.put('ir069', data=ir)
            #         #hf_new['ir069'][i]
            # else:
        with h5py.File(new_file_name, 'w') as hf_new:
            hf_new.create_dataset('id', data=event_id)
            hf_new.create_dataset(img_type, data=img_type_data)
        print("Write finished: ", i)

        with h5py.File(new_file_name, mode='a') as h5f:
            dset = h5f[new_file_name]
            dset.resize((x + 1,) + (i,384,384,49))
            dset[x] = [values]
            x += 1
            h5f.flush()


# hf.close()
# hf_new.close()

print('Event ID:', event_id)
print('Image shape:', img_type)



import h5py
import s3fs
import matplotlib.pyplot as plt

file_list ['vil/2019/SEVIR_VIL_STORMEVENTS_2019_0101_0630.h5', 'vis/2019/SEVIR_VIS_STORMEVENTS_2019_0101_0131.h5', 'ir107/2019/SEVIR_IR107_STORMEVENTS_2019_0101_0630.h5', 'ir069/2019/SEVIR_IR069_STORMEVENTS_2019_0101_0630.h5']

filename = "s3://sevir/data/vil/2019/SEVIR_VIL_STORMEVENTS_2019_0101_0630.h5"

#file - vil/2019/SEVIR_VIL_STORMEVENTS_2019_0101_0630.h5
#index - [128, 672, 292, 644, 550, 807, 168, 779, 140, 621, 18, 19, 403, 309, 570, 411, 701]

fs = s3fs.S3FileSystem(anon=True)
with fs.open(filename, mode='rb') as f:
    hf = h5py.File(f)
    event_id = hf['id'][145]
    vil = hf['vil'][145]

fig,axs=plt.subplots(1,4,figsize=(10,5))
axs[0].imshow(vil[:,:,10])
axs[1].imshow(vil[:,:,20])
axs[2].imshow(vil[:,:,30])
axs[3].imshow(vil[:,:,40])
plt.savefig('vil.png')


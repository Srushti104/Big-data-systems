# Lab 6 - SEVIR : A Storm Event Imagery Dataset for Deep Learning Applications in Radar and Satellite Meteorology

The Storm EVent ImagRy dataset (SEVIR), a dataset designed for advancing machine learning for meteorology. SEVIR contains image sequences for over 10,000 weather events that cover 384 km x 384 km patches and span 4 hours. Images in SEVIR were sampled and aligned across 5 different sensing modalities: three channels (C02, C09, C13) from the GOES-16 advanced baseline imager (ABI) [22], NEXRAD derived vertically integrated liquid (VIL) mosaics created by the FAA’s NextGenWeather processor Testbed [4], and GOES-16 Geostationary Lightning Mapper (GLM) flashes [11]. Events in SEVIR were carefully sampled to ensure the dataset contains
relevant severe storm cases. 

• Publicly available terabyte-sized SEVIR dataset of 10,000 weather events aligned across 5 imaging modalities.  
• Detailed overview of two machine learning applications that can be studied using SEVIR.  
• Source code for data readers, baseline model implementations, metrics, loss functions and trained models for Nowcast and Synthetic Weather Radar applications.  

Link to [Research Paper](https://proceedings.neurips.cc/paper/2020/file/fa78a16157fed00d7a80515818432169-Paper.pdf)

Link to [Github](https://github.com/MIT-AI-Accelerator/neurips-2020-sevir)

Link to [Synthetic Radar Notebook](https://github.com/MIT-AI-Accelerator/neurips-2020-sevir/blob/master/notebooks/AnalyzeSyntheticRadar.ipynb)

## Configuration:
  Install the following python packages:
  * Tensorflow 2.1.0 or higher 
  * pandas
  * matplotlib
  * h5py

### Pretrained models:
   Before running the notebook create a folder under as SYNRAD under models download the pretrained models from the below links and place them under SYNRAD

   Gan_mae_weights.h5: https://www.dropbox.com/s/d1e2p36nu4sqq7m/gan_mae_weights.h5?dl=0

   Synradmse_vgg_weights.h5: https://www.dropbox.com/s/a39ig25nxkrmbkx/mse_vgg_weights.h5?dl=0

   Synradmse_weights.h5: https://www.dropbox.com/s/6cqtrv2yliwcyh5/mse_weights.h5?dl=0




## Codelab Document:
  For more information refer the [Codelab Document](https://docs.google.com/document/d/1U_E9OhYmezjdiWyntQrGYI4fWmiUgKk4I4VXRZtmsAE/edit#"Codelab Document")

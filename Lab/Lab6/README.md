# Lab 6 - SEVIR : A Storm Event Imagery Dataset for Deep Learning Applications in Radar and Satellite Meteorology

The Storm EVent ImagRy dataset (SEVIR), a dataset designed for advancing machine learning for meteorology. SEVIR contains image sequences for over 10,000 weather events that cover 384 km x 384 km patches and span 4 hours. Images in SEVIR were sampled and aligned across 5 different sensing modalities: three channels (C02, C09, C13) from the GOES-16 advanced baseline imager (ABI) [22], NEXRAD derived vertically integrated liquid (VIL) mosaics created by the FAA’s NextGenWeather processor Testbed [4], and GOES-16 Geostationary Lightning Mapper (GLM) flashes [11]. Events in SEVIR were carefully sampled to ensure the dataset contains
relevant severe storm cases. 

• Publicly available terabyte-sized SEVIR dataset of 10,000 weather events aligned across 5 imaging modalities.  
• Detailed overview of two machine learning applications that can be studied using SEVIR.  
• Source code for data readers, baseline model implementations, metrics, loss functions and trained models for Nowcast and Synthetic Weather Radar applications.  

Link to [Research Paper](https://proceedings.neurips.cc/paper/2020/file/fa78a16157fed00d7a80515818432169-Paper.pdf)

Link to [Github](https://github.com/MIT-AI-Accelerator/neurips-2020-sevir)

Link to [Synthetic Radar Notebook](https://github.com/MIT-AI-Accelerator/neurips-2020-sevir/blob/master/notebooks/AnalyzeSyntheticRadar.ipynb)

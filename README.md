# First look at AWS Chronos
Foundation models for time series have been getting a lot of hype recently. So I decided to try out [AWS Chronos](https://github.com/amazon-science/chronos-forecasting). 

So far, the results are underwhelming. Looking [under the hood](https://arxiv.org/abs/2403.07815), it would appear like the model is trained on only a few billion data points. While that might sound like a lot, that's about how much data the geophysics community had [twenty five years ago](https://ds.iris.edu/files/stats/data/archive/Archive_Growth.jpg).  A single, medium sampling rate seismometer operating for five years collects about 10 billion data points. And we have thousands of seismometers like that.  Not to mention remote sensing data.

So how bad is it? I ran the data on 100 time series from the [MEaSUREs Greenland 6 and 12 day Ice Sheet Velocity Mosaics from SAR](https://nsidc.org/data/nsidc-0766/versions/2). The result? The MAE of the forecast was 63.7 m/a and the MAE achieved by just assuming d/dt=0 (i.e., that the time series flatlines to the last value during the evaluation period) was 29.0. 

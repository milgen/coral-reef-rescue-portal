# Coral Reef Rescue Portal

This repository contains the prototype implementation of the Coral Reef Recsue Portal developed during 
the eight weeks of
[The Big Blue Copernicus Hackathon](https://mothershipmissions.com/thebigblue). 

## Sub-Modules Organization
### Demo

The [demo](demo) consists of a map display, a data panel which presents different layers of processed and fetched data, 
a selection panel where the user can select location and date, 
and a time series trend graph to demonstrate the changes of sedimentation through time. 
The processed data includes a classified and reclassified image of sedimentation 
and will be extended to include a map of chlorophyll algae, sea
surface temperature, and turbidity. 
The relevant overlay data includes basemaps, weather
data, precipitation data, and the location of coral reefs.

### Data Analysis
Thd [data analysis](data-analysis) contains scripts and notebooks for data preprocessing and analysis.
 
Before getting to the prototype, we spent a great deal of effort on establishing a processing
chain starting with image acquisition, and continuing with pre-processing and preparation,
classification, batch processing, aggregation, and time series analysis. We experimented
with several tools and algorithms before deciding on the optimal solutions. We used Sentinel
2 data, ranging from 2016 to 2020. This gave us about 130 images, with a maximum
frequency of 1 image per 5 days. We selected images with less than 70% cloud coverage,
and then stacked the images to derive the statistics, during the aggregation.


## Installation and running the code

### Run the demo
You can find the instructions [here](demo/README.md).
### Run the data analysis
You can run scripts and notebooks locally, but the data is not part of the repository. 
Details are described [here](data-analysis/README.md)


### Run the data analysis code on the VM
#### Setup conda
1. Source conda: `source /opt/conda/etc/profile.d/conda.sh`
2. Activate coraladies environment: `conda activate coraladies`
3. Optional: Install libraries with `pip install <missing-lib>`

#### Get or update the source code
 1. Clone the repository: `git clone https://github.com/Coraladies/coral-reef-rescue-portal.git`
 2. Get latest code from github:`git pull`

#### Run a Python Script
1. Goto source code: `cd ~/code/coral-reef-rescue-portal`
3. Got to data-analysis: `cd data-analysis`
4. Look at the example script `run_analyse_timeseries.py`


## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details

## Acknowledgments

The [ACOLITE tool provided by RBINS](https://odnature.naturalsciences.be/remsem/software-and-data/acolite) gave us a quick start in producing sedimentation results and formed a decent basis to achieve preprocessing results for Sentinel-2 imagery.
ACOLITE is a processor for Landsat (5/7/8) and Sentinel-2 (A/B) imagery developed at RBINS.




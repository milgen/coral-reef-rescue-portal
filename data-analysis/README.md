## Installation

### Setup a conda environment
Prerequisite is that conda is installed.
1. Create a new environment, we are using coraladis: `conda  conda create --name coraladies python=3.7`
2. Activate the environment: `conda activate coraladies`
3. Install basemap using conda: `conda install basemap`
4. Install required python libraries with pip: `pip install -r requirements.txt`

In case of problems with geopandas try
`pip install --force-reinstall geopandas`

### Optional: Install GDAL
Installation of GDAL on linux:
`sudo apt install gdal-bin`
`sudo apt install python-gdal` 
`sudo apt install python3-gdal`
`sudo apt install python3-rtree`

## Running the trend analysis notebook 
Make sure that you are in the data-analysis directory where the notebook is loacted.
Run jupyter with: `jupyter notebook trend_analysis.ipynb`
A browser window will displaying the notebook will open.
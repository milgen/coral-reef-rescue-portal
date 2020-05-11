from netCDF4 import Dataset
import numpy as np
import glob

def get_product_paths(root_dir, date=''):
    """
    Returns path to the results produced by the Acolite processor for the given date or date range.
    Each file conatains the result of processed product and comes in  netCDF4 format.

    Parameters
    ----------
    root_dir : starting point to locate result files
        Description of arg1
    date : date str of the format '%Y-%m%-d or parts
        Examples are 2019, 2020-03, 2017-01-31

    Returns
    -------
    str
       Full path to netCDF result files for the given date

    """
    nc = glob.glob(f'{root_dir}/*{date}*/*L2W.nc')
    if len(nc) == 0:
        print(f"no product found for date: '{date}'")
    return nc


def aggregate_timeline(root_dir, date, algorithm, thres):
    """
    Aggregates results  into a 3 dim data grid.
    Results containing more than a specified threshold of empty values to  will be skipped.

    Parameters
    ----------
    root_dir : str
       Starting point to locate result files
    date : str
       Date str of the format '%Y-%m%-d or parts. Examples are 2019, 2020-03, 2017-01-31
    algorithm : str
       Variable name specifying the algorithm used, one of: spm_nechad2016, t_nechad2016, t_dogliotti, fai
    thres: float
        The threshold of empty to value ratio used to skip data added to the timeline.

    Returns
    -------
    (list, array)
       Tuple of dates and values. Dates are a list of date strings with format Y%-m%-%d.
       Values is a 3-dim array containing the result for every time frame and the given algorithm for each pixel/location,
       dimensions are time frames * nlats * nlon
    """
    prod_paths = get_product_paths(root_dir, date)

    assert (len(prod_paths) > 0), f"No processing results found at: '{root_dir}' " \
                                  f"for {date or 'all dates'}. Stopping processing"

    value_array = []
    date_array = []

    for prod in prod_paths:
        date = __to_datestr(prod)
        rootgrp = Dataset(prod, 'r')
        values = rootgrp.variables[algorithm][:]
        nans = np.count_nonzero(np.isnan(values))
        nan_ratio = nans/values.size
        if nan_ratio > thres:
            print(f"Data array of data: {date} contains a {nan_ratio*100}% of empty values, only {thres*100}% is accepted")
        else:
            date_array.append(date)
            value_array.append(values)
        rootgrp.close()
    all_values = np.stack(value_array)

    return date_array, all_values


def convert_to_dataframe(dates, data_grid, thres_col=0.9):
    """
    Converts a 3dim data grid to a dataframe.

    Parameters
    ----------

    dates : list
       List of date str of the format '%Y-%m-%d'.
    data_grid : array
       Data array with result value for each pixel/location.
    thres: float
        The threshold of empty to value ratio used to skip skip adding timeslice (column) to the dataframe.

    Returns
    -------
    dataframe
       The dataframe contains a time slice per column and one element (flattend) from the data_grid as row.
    """
    import pandas as pd

    data = data_grid.reshape(data_grid.shape[0], -1)
    index = pd.DatetimeIndex(dates)
    df = pd.DataFrame(data, index=index)

    #nan_count = df.isnull().sum(axis=1)
    #print(f"number of nan per date:\n{nan_count}")
    if thres_col > 0.:
        cols = len(df.columns)
        thres_value = len(df)*thres_col
        print(f"using a threshold of minimum of {thres_value} non nan values per col")
        #axis 1 stands for col!!!!!
        df = df.dropna(thresh=thres_value, axis=1, how='all')
        nan_count = df.isnull().sum(axis=1)
        print(f"ratio of number of cols dropped: {(cols-len(df.columns))/cols}")
        print(f"number of nan per date after dropping cols:\n{nan_count}")
    return df


def count_nans(all_values):
    """
    Counts the number of nan values from the given array along the first/time axis.

    Parameters
    ----------
    all_values : array of dim time frames * lats * lons
        Results for one parameter (spm or turbidity) for all dates

    Returns
    -------
    array
        Aggregate number of nans for each pixel/location per time

    """
    return np.apply_along_axis(lambda x: np.count_nonzero(np.isnan(x)), 0, all_values)


def __to_datestr(filename): return '-'.join(filename.split('_')[-8:-5])


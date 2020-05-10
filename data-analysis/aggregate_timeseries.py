import numpy as np
import warnings
import acolite_result_reader, clustering
import os


def remove_outliers(time_data):
    """Sets negative and very high values to nan. Operates in place """
    time_data[time_data < 0.001] = np.nan
    time_data[time_data > 10000] = np.nan


def print_stats(time_data):
    values = time_data.flatten()
    nan_ratio = time_data[np.isnan(time_data)].count()/values.size
    min = np.nanmin(values, axis=0)
    max = np.nanmax(values, axis=0)
    mean = np.nanmean(values, axis=0)
    var = np.nanvar(values, axis=0)
    std = np.nanstd(values, axis=0)
    return nan_ratio, min, max, mean, var, std


def simple_thresholding(values):

    data = np.ndarray.copy(values)
    hv = data[np.logical_not(np.isnan(data))]

    #print(f"non nan values in data: {hv.size}\n std: {np.std(hv)}, mean: {np.mean(hv)}, meadian: {np.median(hv)}, max: {np.max(hv)}, min: {np.min(hv)}")
    #print(f"count  < mean: {hv[hv <= np.mean(hv)].count()}, count > mean + std: {hv[hv > np.mean(hv) + np.std(hv)].count()}")
    #print(f"rel mean: {hv[hv <= np.median(hv)].count() / hv.size}, rel mean+std {(hv[hv > (np.median(hv) + np.std(hv))].count()) / hv.size}")

    thres = 2 * np.mean(hv)

    data[np.isnan(data)] = 0.
    data[data < thres] = 0.
    indices = np.argwhere(data)
    return thres, indices, data


def save_as_csv(values, target_dir, filename):
    np.savetxt(os.path.join(target_dir, filename), values, delimiter=",")


def read_from_csv(path):
    from numpy import genfromtxt
    return genfromtxt(path, delimiter=',')


def plot(data, outputdir, filename, title):
    import matplotlib.pyplot as plt
    from matplotlib.colors import LogNorm

    plot_data = np.ndarray.copy(data)
    plot_data[np.isnan(plot_data)] = 1
    plot_data[plot_data == 0.] = 1

    fig = plt.imshow(plot_data, norm=LogNorm(1, 100))

    fig.set_cmap(plt.cm.RdBu_r)
    plt.colorbar()
    plt.title(title)
    plt.savefig(os.path.join(outputdir, filename))
    plt.close('all')


def aggregate(root_dir, date, algorithm, outputdir,
              kernel_size, number_of_clusters):


    dates, values = acolite_result_reader.aggregate_timeline(root_dir, date, algorithm, thres=0.85)

    nan_ratio, min, max, mean, var, std = print_stats(values)
    print(f"nan ratio: {nan_ratio}")
    print(f"min: {min}")
    print(f"max: {max}")
    print(f"mean: {mean}")
    print(f"var: {var}")
    print(f"std: {std}")

    remove_outliers(values)

    #using maximum values
    data = np.nanmax(values, axis=0)

    thres, indices, thres_data = simple_thresholding(data)
    print(f"Thresolding data with: {thres}")

    ### filter and clustering
    print(f"Preparing for clustering, using median filter with kernel size {kernel_size}")
    print(f"Clustering into {number_of_clusters} clusters")
    groups = clustering.cluster(indices, data.shape, kernel_size=kernel_size, number_of_clusters=number_of_clusters)

    ## saving intermediate results
    prefix = "ts_"
    postfix = f"_{algorithm}"

    ## extract dataframe per group and save it as csv
    for cluster, cluster_indices in groups.items():
        cluster_values = values[:, cluster_indices[:, 0], cluster_indices[:, 1]]
        print(f"cluster {cluster} with size: {cluster_values.shape}")
        df = acolite_result_reader.convert_to_dataframe(dates, cluster_values, thres_col=0.)
        filename = f"{prefix}df_cluster_{cluster}{postfix}.csv"
        df.to_csv(os.path.join(outputdir, filename))

    print(f"plotting and saving intermediate results to: {outputdir}")

    #don't need indices, use dataframe ! save_as_csv(indices, outputdir, 'thres_indices.csv')

    filename = f"{prefix}time_averaged_maxima{postfix}.png"
    title = f"Areas with highest values for {algorithm} (time averaged)"
    plot(data, outputdir, filename, title)

    title = f"Hotspots for {algorithm} (threshold {str(round(thres, 3))})"
    filename = f"{prefix}time_averaged_hotspots_thres{str(round(thres))}_{postfix}.png"
    plot(thres_data, outputdir, filename, title)


if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)

        ###########################
        ## provide parameter values:

        root_dir = 'data/l2w'
        # root_dir = '/data/results/batch_run'

        # all dates included
        date = ''
        algorithm = 'spm_nechad2016'

        outputdir = '/home/angela/transfer/as/local'
        # outputdir = '/home/eouser/transfer/as'

        kernel_size = 7
        number_of_clusters = 3
        ###########################

        aggregate(root_dir, date, algorithm, outputdir, kernel_size, number_of_clusters)







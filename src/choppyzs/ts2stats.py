#!/usr/bin/env python3
"""
    This bins time series drought data by boundaries described in the
    given shape file.
"""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed, \
    ThreadPoolExecutor

import xarray
import rasterio
import pandas as pd
import geopandas as gpd
from rasterstats import zonal_stats

try:
    from choppyzs.imagediff import check_if_file_exists
    from choppyzs.logz import create_logger
except ImportError:
    from .imagediff import check_if_file_exists
    from .logz import create_logger

logger = create_logger()


def _init_pool(b_df, scpdsi_data, affine_data):
    """ Used to set up data for workers """
    global boundaries_df, scpdsi, affine, logger

    try:
        from choppyzs.logz import create_logger
    except ImportError:
        from .logz import create_logger

    logger = create_logger()

    boundaries_df = b_df
    scpdsi = scpdsi_data
    affine = affine_data


def _agg_ts_data(nc_time):
    """ This creates a single dataframe for the given nc_time

    Called via map() for all dates.

    :returns: single dataframe of nc_time data
    """
    logger.info(f'Parsing time {nc_time}')

    nc_arr = scpdsi.sel(time=nc_time)
    nc_arr_values = nc_arr.values

    stats_data = zonal_stats(boundaries_df,
                             nc_arr_values, affine=affine,
                             stats='min,max,mean,median,majority,sum,std,count,range'.split(
                                 ','),
                             nodata=-9999,  # to shut up stupid warning
                             geojson_out=False,
                             all_touched=True)
    sd = pd.DataFrame.from_dict(stats_data)

    dat = pd.concat([boundaries_df, sd], axis=1)

    dat['time'] = nc_time

    return dat


def ts_to_stats(shape_file_archive, ts_file):
    """ Aggregate time series drought data by month and region.

    :param shape_file_archive: zip file of boundaries
    :param ts_file: is NetCDF file of time series drought data
    :return: dataframe of drought data by region and month
    """

    def read_ts(ts_file):
        """ read the time series data file
        :returns: time series data and affine transform
        """
        logger.info(f'Reading {ts_file}')

        # Get the time series of drought data
        drought_ts = xarray.load_dataset(ts_file)

        # Bendy affine transform data
        affine = rasterio.open(ts_file).transform

        return drought_ts, affine

    def chop(boundaries_df, drought_ts, affine):
        """ perform the data aggregation
        :return: dataframe of aggregated data
        """
        scpdsi = drought_ts['scpdsi']
        times = drought_ts['time'].values

        with ProcessPoolExecutor(initializer=_init_pool,
                                 initargs=(boundaries_df,
                                           scpdsi,
                                           affine)) as pool:
            df_futures = pool.map(_agg_ts_data,
                                  times)

            dfs = list(df_futures)

        logger.info(f'Have {len(dfs)} dataframes.')

        return pd.concat(dfs, ignore_index=True)
        # end chop()

    check_if_file_exists(shape_file_archive)
    check_if_file_exists(ts_file)

    # Extract a geopandas dataframe from the given shape file.
    boundaries_df = gpd.read_file(shape_file_archive)

    # Now grab the time series data
    drought_ts, affine = read_ts(ts_file)

    # Now do the chopping
    df = chop(boundaries_df, drought_ts, affine)

    df.drop(columns='geometry',
            inplace=True,
            errors='ignore')

    return df


if __name__ == '__main__':
    # Just a simple test harness

    logger.info('running ts2stats test')

    if Path('/examples').exists():
        df = ts_to_stats('/examples/lichtenstein.zip',
                         '/examples/drought.nc')
    else:
        df = ts_to_stats('examples/lichtenstein.zip',
                         'examples/drought.nc')

    if df is not None and not df.empty:
        df.to_csv('new_zonal_stats.csv', index=False)
    else:
        logger.warning('No data to write.')

    logger.info('Done')

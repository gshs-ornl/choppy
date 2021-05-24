#!/usr/bin/env python3
# description {{{1 ------------------------------------------------------------
""" This module provides the Chop class which is used for zonal statistics
    processing provided a shapefile and a raster.
"""
# 1}}} ------------------------------------------------------------------------
# legal {{{1 ------------------------------------------------------------------
__author__ = "Joshua N. Grant"
__maintainer__ = "Joshua N. Grant"
__email__ = "grantjn@ornl.gov"
__copyright__ = "Copyright 2019, UT-BATTELLE"
__license__ = "MIT"
__status__ = "Production"
__version__ = "1.0.4"

# 1}}} ------------------------------------------------------------------------
# imports {{{1 ----------------------------------------------------------------
import os
import sys
import csv
from pathlib import Path
import pandas as pd
import patoolib as pa
import geopandas as gpd
from tempfile import TemporaryDirectory
from rasterstats import zonal_stats


# 1}}} ------------------------------------------------------------------------
# Choppy class {{{1 -----------------------------------------------------------
class Choppy:
    """ Choppy class is the initiatition and subsequent functions used to
  retrieve the zonal statistics provided an ESRI shapefile and subsequently
  related files in an arhive and then perform zonal statistics upon a raster
  also passed.

  Parameters:
      shape_archive    a shapefile archive
      raster_file      a rasterfile
      output_dir       the output directory
      output_file      the desired output filename
      statistics       a comma separated list of statistics to perform
      all_touched      bool, should all shapes touched be included
      output_format    the output format, must be one of xlsx, csv, tsv, or
                       none if using the module inside other scripts or modules
      geometry         also export the geometry information, may cause problems
                       with csv or tsv outputs
  """

    def __init__(self, shape_archive, raster_file, output_dir=os.getcwd(),
                 statistics='min,max,mean,median,majority,sum,std,count,range',
                 output_file='zonal_stats', all_touched=False,
                 output_format='xlsx', geometry=False):
        """ Initialize a Choppy class for preparation for zonal statistics """
        # create a temporary workspace
        if output_format not in ['xlsx', 'csv', 'tsv', 'none']:
            raise RuntimeError(f'This format ({output_format}) is not '
                               f'acceptable!')
        self.working_directory = TemporaryDirectory()
        if ',' in statistics:
            self.statistics = statistics.split(',')
        if ',' not in statistics:
            self.statistics
        self.output_format = output_format
        if not output_file.lower().endswith(output_format):
            self.output_file = output_file + '.' + output_format
        else:
            self.output_file = output_file
        self.all_touched = all_touched
        self.raster_file = raster_file
        self.shape_archive = shape_archive
        pa.extract_archive(shape_archive, outdir=self.working_directory.name)
        print(os.listdir(self.working_directory.name))
        shape_dir_name = os.path.basename(
            os.path.splitext(self.shape_archive)[0])
        shape_dir_path = os.path.join(self.working_directory.name,
                                      shape_dir_name)
        for f in os.listdir(self.working_directory.name):
            if f.endswith('.shp'):
                self.shape_file = os.path.join(self.working_directory.name,
                                               f)
            else:
                pass
        if os.path.isfile(self.shape_file):
            self.shape_file_present = True
        else:
            self.shape_file_present = False
            print('Shapefile was not found')
            sys.exit()
        self.output_path = os.path.join(output_dir, self.output_file)
        if output_format == 'json':
            self.geojson = True
        else:
            self.geojson = False
        self.all_touched = all_touched
        self.shapes = gpd.read_file(self.shape_file)

    def __str__(self):
        """ Display information about a Choppy object """
        return 'Choppy class object:\n\t' + \
               'input shape archive:\t' + self.shape_archive + '\n\t' + \
               'input shape file:\t' + self.shape_file + '\n\t' + \
               'input raster file:\t' + self.raster_file + '\n\t' + \
               'output directory:\t' + self.output_path + '\n\t' + \
               'statistics:\t\t' + ','.join(self.statistics) + '\n\t' + \
               'all touched:\t\t' + str(self.all_touched) + '\n\t'

    def chop(self):
        stats_data = zonal_stats(self.shape_file,
                                 self.raster_file, geojson_out=self.geojson,
                                 all_touched=self.all_touched,
                                 stats=self.statistics)
        sd = pd.DataFrame.from_dict(stats_data)
        df = pd.DataFrame(self.shapes)
        dat = pd.concat([df, sd], axis=1).drop(columns='geometry')
        if self.output_format == 'csv':
            dat.to_csv(self.output_path, index=False)
        elif self.output_format == 'tsv':
            dat.to_csv(self.output_path, sep='\t', index=False)
        elif self.output_format == 'xlsx':
            dat.to_excel(self.output_path)
        elif self.output_format == 'none':
            print(dat)
        self.data = dat
        return dat
# 1}}} ------------------------------------------------------------------------


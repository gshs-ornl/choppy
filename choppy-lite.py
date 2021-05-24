#!/usr/bin/env python3
# description {{{1 -----------------------------------------------------------
""" This module provides the ability to obtain zonal statistics provided a
shapefile and a raster
"""
# 1}}} -----------------------------------------------------------------------
# imports {{{1 ---------------------------------------------------------------
import os
import sys
import csv
import argparse
import pandas as pd
import patoolib as pa
import geopandas as gpd
from tempfile import TemporaryDirectory
from rasterstats import zonal_stats
from scipy import stats
from choppyzs.choppy import Choppy
# 1}}} -----------------------------------------------------------------------
# legal {{{1 -----------------------------------------------------------------
__author__ = 'Joshua N. Grant'
__email___ = 'grantjn@ornl.gov'
__copyright__ = 'Copyright 2019, UT-BATTELLE'
# 1}}} -----------------------------------------------------------------------
# color class {{{1 -----------------------------------------------------------
class Color:
  default = '\033[39m'
  red = '\033[31m'
  green = '\033[32m'
  yellow = '\033[33m'
  blue = '\033[34m'
  magenta = '\033[35m'
  cyan = '\033[36m'
  lgray = '\033[37m'
  dgray = '\033[90m'
  lred = '\033[91m'
  lgreen = '\033[92m'
  lyellow = '\033[93m'
  lblue = '\033[94m'

# 1}}} -----------------------------------------------------------------------
# display info {{{1 ----------------------------------------------------------
def banner():
  print(Color.green + '    __  __ __   ___   ____  ____  __ __     ')
  print('   /  ]|  |  | /   \ |    \|    \|  |  |    ')
  print('  /  / |  |  ||     ||  o  )  o  )  |  |    ')
  print(' /  /  |  _  ||  O  ||   _/|   _/|  ~  |    ')
  print('/   \_ |  |  ||     ||  |  |  |  |___, |    ')
  print('\     ||  |  ||     ||  |  |  |  |     |    ')
  print(' \____||__|__| \___/ |__|  |__|  |____/     ')
  print(Color.dgray + "                                ((///&                     ")
  print("                              ((((& //////                 ")
  print("                             (((      ////////#            ")
  print("                            ((((      #//////////**        ")
  print("                    @@@@@@@&(((//    ////////%    (*****   ")
  print("                  @@,        @@//////////%@/          ****,")
  print("                 @             (@///////@               *, ")
  print("                @                @////#@                @  ")
  print("               @                 %@///@                 ,@ ")
  print("               @         %@@      @///@         ,@@      @ ")
  print("               @        ,@@@@    @&///@         @@@@    &  ")
  print("                @         .     (@/////@         .      @  ")
  print("                 @%            @%///////@@            @    ")
  print("                     %      @@(//////////*@@@      @@@     ")
  print("                   (((//////////////////**********,        ")
  print("                  (((//////////////////**********,         ")
  print("                 ((((/////////////////**********,&         ")
  print("                (#########(((((((((((((((((((((/*          ")
  print("               ((" + Color.lred + "@%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%      ")
  print("  " + Color.dgray + "             %((" + Color.lred + "@%@" + Color.dgray + "///////////////**********,.   " + Color.lred +" %%      ")
  print("  " + Color.dgray + "            ((("+ Color.lred + "@%@" + Color.dgray + "///////////////**********,   " + Color.lred +"  %%      ")
  print("  " + Color.dgray + "           (((/" + Color.lred + "@%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%       ")
  print("  " + Color.dgray + "          (((//////////////////**********,               ")
  print("           ((((/////////////////**********,                ")
  print(Color.yellow + "          #(//*&" + Color.dgray + "///////////////**********,/                ")
  print(Color.yellow + "          (//**,,." + Color.dgray + "  &/////////**********,.                 ")
  print(Color.yellow + "         (//**,,,% " + Color.dgray + "      ////**********,.                  ")
  print(Color.yellow + "        ((/***,,.   " + Color.dgray + "          *********,                   ")
  print(Color.yellow + "       #(/***,,.    " + Color.dgray + "              %***,                    ")
  print(Color.yellow + "      #(//**,,.                                            ")
  print(Color.yellow + "     &(//**,,.                                             ")
  print(Color.yellow + "     (//**,,,#  " + Color.cyan + "                 _______________           ")
  print(Color.yellow + "    ((/***,,,   " + Color.cyan + "                 ___  /__(_)_  /_____      ")
  print(Color.yellow + "   #(//**,,.    " + Color.cyan + "                 __  /__  /_  __/  _ \     ")
  print(Color.yellow + "  #(//**,,.     " + Color.cyan + "                 _  / _  / / /_ /  __/     ")
  print(Color.yellow + " %(//**,,.      " + Color.cyan + "                 /_/  /_/  \__/ \___/      ")
  print(Color.yellow + " (//**,,.#                                                 ")
  print(Color.yellow + "((/***,,*                   " + Color.yellow + "v " + Color.lblue + "0.1.2  ")
  print(Color.yellow + "(/***,,." + Color.default)

# 1}}} -----------------------------------------------------------------------
# create the argument parser {{{1 --------------------------------------------
def parse_args():
  """ Argument parser for choppy-lite """
  parser = argparse.ArgumentParser(description="Add values via command \
        line to send to choppy")
  parser.add_argument('--shp-file', type=argparse.FileType('r'),
        help='The shape file to use', dest='shape_file', action = 'store')
  parser.add_argument('--shapes-directory', type=str, action = 'store',
        dest='shapes_dir', help='the directory where the shape files exist')
  parser.add_argument('-s','--shape_archive', type=argparse.FileType('r'),
        help="The archived files to use to extract features and \
        compare against the raster", dest="shape_archive", action="store")
  parser.add_argument('-r','--raster', type=argparse.FileType('r'),
        help="The rasterfile to use for retrieving zonals stats from",
        dest="raster", action="store")
  parser.add_argument('-x','--stats', dest='stats', type=str, help="Which \
        stats should be used to to compute the zonal statistics",
        action='store')
  parser.add_argument('-g','--geometry', dest='report_geometry',
        action='store_true', help='Should the geometry field be exported?')
  parser.add_argument('-o','--output-dir', dest='output_dir', type=str,
        help="Where should the file be stored?", action='store')
  parser.add_argument('-f','--output-format', dest='output_format', type=str, \
        action='store',help="the type of format to output the file as")
  parser.add_argument('-d','--destination', dest='output_file', action='store', \
        type=str, help='the destination output file')
  parser.add_argument('-a','--all-touched', dest='all_touched', \
        action='store_true')
  parser.set_defaults(stats='min,max,mean,median,majority,sum,std,count,range', \
        output_dir=os.getcwd(), output_format='csv', \
        output_file='zonal_stats', all_touched=False, report_geometry=False)
  return parser.parse_args()
# 1}}} -----------------------------------------------------------------------
if __name__ == "__main__":
  banner()
  if not len(sys.argv) > 0:
    sys.exit()
  args = parse_args()
  print(type(args.shape_archive))
  c = Choppy(shape_archive=args.shape_archive,
             raster_file=args.raster,
             output_dir=args.output_dir,
             statistics=args.stats,
             output_file=args.output_file,
             all_touched=args.all_touched,
             output_format=args.output_format,
             geometry=args.report_geometry)
  c.chop()





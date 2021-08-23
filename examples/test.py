#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from choppyzs.logz import create_logger
logger = create_logger()

from time import perf_counter

from choppyzs.netcdf import NetCDF2Stats as NTS

if __name__ == "__main__":
    start_time = perf_counter()
    # nts = NTS('Shapes.zip', 'drought.nc')
    nts = NTS('lichtenstein.zip', 'drought.nc', all_touched=True)
    logger.info(f'ctor time: {perf_counter() - start_time}')

    chop_time = perf_counter()
    nts.chop()
    logger.info(f'chop time: {chop_time - start_time}')

    export_time = perf_counter()
    nts.export()
    logger.info(f'export time: {export_time - chop_time}')
    logger.info(f'total time: {perf_counter() - start_time}')

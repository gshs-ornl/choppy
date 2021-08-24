#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from choppyzs.logz import create_logger
logger = create_logger()

from time import perf_counter

from choppyzs.ts2stats import ts_to_stats

if __name__ == "__main__":
    start_time = perf_counter()

    # nts = NTS('Shapes.zip', 'drought.nc')
    df = ts_to_stats('lichtenstein.zip', 'drought.nc')

    if df is not None and not df.empty:
        df.to_csv('zonal_stats.csv', index=False)
    else:
        logger.warning('No data to write.')

    logger.info(f'total time: {perf_counter() - start_time}')

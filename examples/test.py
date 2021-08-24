#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
from choppyzs.logz import create_logger
logger = create_logger()

from time import perf_counter

from choppyzs.ts2stats import ts_to_stats

if __name__ == "__main__":
    start_time = perf_counter()

    shape_file = Path('lichtenstein.zip')

    # nts = NTS('Shapes.zip', 'drought.nc')
    df = ts_to_stats(shape_file, 'drought.nc')

    if df is not None and not df.empty:
        df.to_csv(shape_file.with_suffix('.csv'), index=False)
    else:
        logger.warning('No data to write.')

    logger.info(f'total time: {perf_counter() - start_time}')

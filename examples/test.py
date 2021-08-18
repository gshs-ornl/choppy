#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from choppyzs.netcdf import NetCDF2Stats as NTS

if __name__ == "__main__":
    nts = NTS('Shapes.zip', 'drought.nc')
    nts.chop()
    nts.export()

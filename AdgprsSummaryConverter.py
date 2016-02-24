#!/usr/bin/env python3
"""
Script to convert the parts of the HDF5 format written by ADGPRS simulator
corresponding to ECLIPSE's SUMMARY files to more convenient formats.
Currently, JSON and CSV output is available.

Required libraries are:
    python3-h5py
    python3-numpy
"""
from AdgprsSummary import AdgprsSummary
from JsonSummaryWriter import JsonSummaryWriter
from CsvSummaryWriter import CsvSummaryWriter
import argparse

parser = argparse.ArgumentParser(description='Convert ADGPRS HDF5 summaries to more readable formats.')
parser.add_argument('infile', metavar='INFILE', type=str,
                    help='path to ADGPRS HDF5 summary file')
parser.add_argument('outfile', metavar='OUTFILE', type=str,
                    help='path to output file')
parser.add_argument('-f', '--format', metavar='FORMAT', type=str,
                    help='format of output file (csv or json)')
args = parser.parse_args()

# Read the HDF5 file
summary = AdgprsSummary(args.infile)

# Save in a new format
if args.format == 'csv' or args.format == 'CSV':
    CsvSummaryWriter(summary, args.outfile)
else:
    JsonSummaryWriter(summary, args.outfile)

# Close the HDF5 file
summary.h5file.close()

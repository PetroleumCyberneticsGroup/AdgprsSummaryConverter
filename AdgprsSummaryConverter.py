#!/usr/bin/env python3
"""
Script to convert the parts of the HDF5 format written by ADGPRS simulator
corresponding to ECLIPSE's SUMMARY files to more convenient formats.
Currently, only JSON output is available. CSV output will be implemented
in the future.

Required libraries are:
    python3-h5py
    python3-numpy
"""
from AdgprsSummary import AdgprsSummary
from JsonSummaryWriter import JsonSummaryWriter
import argparse

parser = argparse.ArgumentParser(description='Convert ADGPRS HDF5 summaries to more readable formats.')
parser.add_argument('infile', metavar='INFILE', type=str,
                    help='path to ADGPRS HDF5 summary file')
parser.add_argument('outfile', metavar='OUTFILE', type=str,
                    help='path to output file')
args = parser.parse_args()

summary = AdgprsSummary(args.infile)
JsonSummaryWriter(summary, args.outfile)

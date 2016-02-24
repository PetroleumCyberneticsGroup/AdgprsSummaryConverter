# AdgprsSummaryConverter
A small python program that extracts summary information from HDF5 files created by ADGPRS and saves them in a more convenient format.

## Requirements
Python 3 with the `numpy` and `h5py` libraries.

## Example usage
```
./AdgprsSummaryConverter path/to/CASE.SUM.H5 path/to/output/file.json
./AdgprsSummaryConverter path/to/CASE.SUM.H5 path/to/output/file.csv -f csv
```

"""Main module."""
import csv 
import linecache 
import numpy as np 

class Dataset:
    def __init__(self, filename):
        self._filename = filename
        self._total_data = 0
        self._columns = self._get_columns()
        
        with open(filename, "r") as f:
            self._total_data = len(f.readlines()) - 1
    
    def __getitem__(self, idx):
        if isinstance(idx, slice):
            step = (1 if idx.step == None else idx.step)
            return [self.__getitem__(i) for i in range(idx.start, idx.stop, step)]
        elif isinstance(idx, list):
            return [self.__getitem__(i) for i in idx]
        elif isinstance(idx, int):
            line = linecache.getline(self._filename, idx + 2)
            csv_data = csv.reader([line])
            data = [x for x in csv_data][0]
            return np.array(data).astype(object)
        else:
            raise TypeError(f"Index must be list or int, not {type(idx).__name__}")
    
    def __len__(self):
        return self._total_data

    def _get_columns(self):
        line = linecache.getline(self._filename, 1)
        csv_data = csv.reader([line])
        return [x for x in csv_data][0]

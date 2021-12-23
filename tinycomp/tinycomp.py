"""Main module."""
import csv 
import linecache 
import numpy as np 

class Dataset:
    def __init__(self, filename):
        self._filename = filename
        self._total_data = self._numline(filename)
        self.columns = self._get_columns()
        self.shape = (self._total_data, len(self.columns))
        
    def __getitem__(self, idx):
        if isinstance(idx, slice):
            step = (1 if idx.step == None else idx.step)
            return np.array([self._getline(i) for i in range(idx.start, idx.stop, step)]).astype(float)
        elif isinstance(idx, list):
            return np.array([self._getline(i) for i in idx]).astype(float)
        elif isinstance(idx, int):
            return np.array(self._getline(idx)).astype(float)
        else:
            raise TypeError(f"Index must be list or int, not {type(idx).__name__}")
            
    def _getline(self, idx):
        line = linecache.getline(self._filename, idx + 2)
        csv_data = csv.reader([line])
        data = [x for x in csv_data][0]
        return data
    
    def _numline(self, filename):
        n = 0
        with open(filename, "r") as f:
            n = len(f.readlines()) - 1
        return n

    def __len__(self):
        return self._total_data

    def _get_columns(self):
        line = linecache.getline(self._filename, 1)
        csv_data = csv.reader([line])
        return [x for x in csv_data][0]
    
    def nlargest(self, indices, n=20, axis=-1):
        s = self[indices[0]]
        for idx in indices[1:]:
            s += self[idx]

        return [self.columns[idx] for idx in np.argsort(s, axis=axis)[-n: ]]
    
    def nsmallest(self, indices, n=20, axis=-1):
        s = self[indices[0]]
        for idx in indices[1:]:
            s += self[idx]

        return [self.columns[idx] for idx in np.argsort(s, axis=axis)[0: n]]

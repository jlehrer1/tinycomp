"""Main module."""
import csv 
import linecache 
import numpy as np 

class Dataset:
    def __init__(self, filename: str, rows: list=None):
        """
        Dataset method can either be initialized with a list of rows (mutable by changing the rows attribute),
        or a new list of rows may be passed in for each method that requires it, but not both (this would be ambiguous).
        
        Parameters:
        filename: Path to csv file 
        rows (optional): List of rows to initialize the dataset with
        
        Returns:
        None
        """
        # Private attributes
        self._filename = filename
        self._total_data = self._numline(filename)
        
        # Public attributes 
        self.rows = rows
        
        # Public attributes (Pandas API-like)
        self.index = rows
        self.columns = self._get_columns()
        self.shape = (self._total_data, len(self.columns))
        
    # Python dunder methods
    
    def __getitem__(self, idx):
        if isinstance(idx, slice):
            step = (1 if idx.step == None else idx.step)
            return np.array([self._getline(i) for i in range(idx.start, idx.stop, step)]).astype(float)
        elif isinstance(idx, (list, range)):
            return np.array([self._getline(i) for i in idx]).astype(float)
        elif isinstance(idx, int):
            return np.array(self._getline(idx)).astype(float)
        else:
            raise TypeError(f"Index must be list or int, not {type(idx).__name__}")

    def __len__(self):
        return self._total_data

    def __str__(self):
        if self.rows is not None:
            return str(self.__getitem__(self.rows))
        else:
            return 'Dataset()'
            
    def __repr__(self):
        return self.__str__()
    
    def _getline(self, idx):
        """
        Returns a line from a csv file as a list of strings (not type-checked)
        
        Parameters:
        idx: Row to return from file 
        
        Returns:
        list: Row of file with each comma-separated value as a distinct value in the list 
        """
        line = linecache.getline(self._filename, idx + 2)
        csv_data = csv.reader([line])
        data = [x for x in csv_data][0]
        return data
    
    def _numline(self, filename):
        """
        Gets the number of lines in a file, should only be used for getting the total number of rows on object initialization
        
        Parameters:
        filename: Path to the file to get the number of lines from
        
        Returns:
        n: Number of lines in the file
        """
        n = 0
        with open(filename, "r") as f:
            n = len(f.readlines()) - 1
        return n
    
    def _row_get(self, rows: list):
        """
        Returns rows from a file, either with a passed list or from the list of rows upon object initialization.
        Also performs error checking to make sure either rows were set upon initialization or passed, but not both or neither. 
        
        Parameters:
        rows: List of rows
        
        Returns:
        list: Array of row values from file 
        """
        
        if self.rows is None and rows is None:
            raise ValueError(
                f"""{self.__class__} object was not initialized with a list of rows.
                Either reinitialize with a list or rows or pass a list of rows to this method."""
            )
        if self.rows is not None and rows is not None:
            raise ValueError(
                f"""{self.__class__} object was initialized with a list of rows. Therefore, a list of rows may not be 
                passed to this method. Either reinitialize without a defined list of rows or do not pass a list into this method. """
            )
        
        return rows if rows != None else self.rows

    def _get_columns(self):
        """
        Get all the columns of the csv
        
        Parameters:
        None
        
        Returns:
        list: List of column names as strings
        """
        line = linecache.getline(self._filename, 1)
        csv_data = csv.reader([line])
        return [x for x in csv_data][0]
    
    def sum(self, rows=None, axis=0):
        """Sums the given rows by the given axis"""
        rows = self._row_get(rows)
        
        return np.sum(self[rows], axis=axis)
        
    def nlargest(self, rows=None, n=20, axis=0, ascending=False):
        """
        Gets the n largest rows or columns (summed), depending on the axis 
        """
        
        rows = self._row_get(rows)
        s = np.sum(self[rows], axis=axis)
        
        if axis == 0:
            data = [self.columns[idx] for idx in np.argsort(s)[-n: ]]
        else:
            data = np.argsort(s)[-n: ]
            
        return data if ascending else data[::-1]

    def nsmallest(self, rows=None, n=20, axis=0, ascending=False):
        """
        Gets the n smallest rows or columns (summed), depending on the axis 
        """
        
        rows = self._row_get(rows)
        s = np.sum(self[rows], axis=axis)
        print(s)
        if axis == 0:
            data = [self.columns[idx] for idx in np.argsort(s)[0: n]]
        else:
            data = np.argsort(s)[0: n]
            
        return data[::-1] if ascending else data
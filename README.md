# TinyComp: 

## A Library for Computation on Subsets of Big Numeric Data

`TinyComp` is a Python library for doing computations on small subsets of a **numeric** `.csv` data file too large to fit entirely in memory. The library follows similarly to the `Pandas` API. Originally developed for my research at the UCSC Genomics Insitute with massive single-cell datasets, this library serves to be a minimal and quick tool for analysis on large datasets.

## Why not Dask?

Dask is great. Kinda. It is very good for doing computations across large datasets that do not fit in memory and also involve a large portion of the dataset. For example, calculating the sum over all rows or the `nlargest` rows across some subset of the columns. However, when we are doing some computation on `k` out of `M` rows where `k << m` and the rows of interest are spread out across the index, Dask does not provide much speedup since each data partition will have to be accessed. 

Therefore, this library serves a tool for doing analysis when we are only interested in subsets of the original data at a time. For example, getting the `nlargest` columns across each cluster in some clustering algorithm. We understand that this is a very particular use case, but it is useful when we don't want to fit this entire subset in memory. 

## Usage

All computations revolve around `tinycomp.Dataset`, an object that is initialized with the path to the `.csv` file we cannot read in normally with `pandas`, either because it is too large to fit in memory or too slow to be worthwhile to.

The easiest way to think of the `Dataset` object is a `pandas DataFrame` where we only have access to a subset of the rows at a time. This is because we're reading in rows with Python's `linecache` library, and then doing computations on those rows with `numpy`. Functionally though, `Dataset`'s simply output `np.ndarray`s when slices, and various sample statistics as we have in `pandas`.

We create a `Dataset` object in the following way

```python
from tinycomp import Dataset
data = Dataset('really_huge_dataset.csv')
```

Now this doesn't load anything into memory, but may take some time to instantiate since we have to calculate `__len__` by reading the number of lines in the file.

Then, we can slice normally, like so

```python
>>> data[0]
...
>>> data[600:10000:5]
...
>>> data[[65, 889, 1236]]
...
```

## Similarities to Pandas
The library API is built to be as similar as possible to `Pandas`. `Dataset`'s have `.shape, .columns` and some other common attributes, as well as `nlargest`, `nsmallest`, `max`, `min`, etc. The critical difference is *all of these methods must have an `Iterable` passed in the `rows` argument, or the class must be initialized with an Iterable of `rows`*, to specify the subset of the data we're currently working with.

```python
>>> data.nlargest(rows=range(600, 650))
['col_42',
 'col_35',
 'col_8',
    ... 
]
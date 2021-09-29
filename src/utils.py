import time
import pathlib
import os
import json
from .log import logger
import shutil

import random
import sys

import pandas as pd
import numpy as np

from functools import partial
from joblib import func_inspect as jfi


__all__ = [
    'deserialize_partial',
    'normalize_labels',
    'partial_call_signature',
    'read_space_delimited',
    'reservoir_sample',
    'serialize_partial',
    'load_json',
    'save_json'
]

_MODULE = sys.modules[__name__]
_MODULE_DIR = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))


# Timing and Performance


def timing_info(method):
    def wrapper(*args, **kw):
        start_time = time.time()
        result = method(*args, **kw)
        end_time = time.time()
        logger.info(f"timing_info: {method.__name__}"
                    f"@{round((end_time-start_time)*1000,1)} ms")

        return result

    return wrapper


def record_time_interval(section, start_time, line_break=False):
    """Record a time interval since the last timestamp"""
    end_time = time.time()
    delta = end_time - start_time
    if delta < 1:
        delta *= 1000
        units = "ms"
    else:
        units = "s"
    if line_break:
        logger.debug("PROCESS_TIME:{:>36}    {} {}\n".format(section, round(delta, 1), units))
    else:
        logger.debug("PROCESS_TIME:{:>36}    {} {}".format(section, round(delta, 1), units))
    return end_time

# def normalize_numpy_dict(d):
#     ret = d.copy()
#     for k, v in ret.items():
#         if isinstance(v, np.generic):
#             ret[k] = np.asscalar(v)
#     return ret


def clean_dir(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def save_json(filename, obj, indent=2, sort_keys=True):
    """Dump an object to disk in json format

    filename: pathname
        Filename to dump to
    obj: object
        Object to dump
    indent: integer
        number of characters to indent
    sort_keys: boolean
        Whether to sort keys before writing. Should be True if you ever use revision control
        on the resulting json file.
    """
    with open(filename, 'w') as fw:
        json.dump(obj, fw, indent=indent, sort_keys=sort_keys)


def load_json(filename):
    """Read a json file from disk"""
    with open(filename) as fw:
        obj = json.load(fw)
    return obj


def head_file(filename, n=5):
    """Return the first `n` lines of a file
    """
    with open(filename, 'r') as fd:
        lines = []
        for i, line in enumerate(fd):
            if i > n:
                break
            lines.append(line)
    return "".join(lines)


def list_dir(path, fully_qualified=False, glob_pattern='*'):
    """do an ls on a path

    fully_qualified: boolean (default: False)
        If True, return a list of fully qualified pathlib objects.
        if False, return just the bare filenames
    glob_pattern: glob (default: '*')
        File mattern to match

    Returns
    -------
    A list of names, or fully qualified pathlib objects"""
    if fully_qualified:
        return list(pathlib.Path(path).glob(glob_pattern))

    return [file.name for file in pathlib.Path(path).glob(glob_pattern)]


def read_space_delimited(filename, skiprows=None, class_labels=True):
    """Read an space-delimited file
    skiprows: list of rows to skip when reading the file.
    Note: we can't use automatic comment detection, as
    `#` characters are also used as data labels.
    class_labels: boolean
        if true, the last column is treated as the class label
    """
    with open(filename, 'r') as fd:
        df = pd.read_table(fd, skiprows=skiprows, skip_blank_lines=True, comment=None, header=None, sep=' ', dtype=str)
        # targets are last column. Data is everything else
        if class_labels is True:
            target = df.loc[:, df.columns[-1]].values
            data = df.loc[:, df.columns[:-1]].values
        else:
            data = df.values
            target = np.zeros(data.shape[0])
        return data, target


def normalize_labels(target):
    """Map an arbitary target vector to an integer vector
    Returns
    -------
    tuple: (mapped_target, label_map)
    where:
        mapped_target: integer vector of same shape as target
        label_map: dict mapping mapped_target integers to original labels
    Examples
    --------
    >>> target = np.array(['a','b','c','a'])
    >>> mapped_target, label_map = normalize_labels(target)
    >>> mapped_target
    array([0, 1, 2, 0])
    The following should always be true
    >>> all(np.vectorize(label_map.get)(mapped_target) == target)
    True
    """
    label_map = {k: v for k, v in enumerate(np.unique(target))}
    label_map_inv = {v: k for k, v in label_map.items()}
    mapped_target = np.vectorize(label_map_inv.get)(target)

    return mapped_target, label_map


def partial_call_signature(func):
    """Return the fully qualified call signature for a (partial) function
    """
    func = partial(func)
    fa = jfi.getfullargspec(func)
    default_kw = {}
    if fa.args:
        default_kw = dict(zip(fa.args, fa.defaults))
    if getattr(fa, 'kwonlydefaults', None):
        fq_keywords = {**default_kw, **fa.kwonlydefaults}
    else:
        fq_keywords = default_kw
    return jfi.format_signature(func.func, *func.args, **fq_keywords)


def process_dataset_default(**kwargs):
    """Placeholder for data processing function"""
    logger.warning(f"Default `load_function` method. No `data` or `target` generated")
    return kwargs


def deserialize_partial(func_dict, delete_keys=False):
    """Convert a serialized function call into a partial
    Parameters
    ----------
    func_dict: dict containing
        load_function_name: function name
        load_function_module: module containing function
        load_function_args: args to pass to function
        load_function_kwargs: kwargs to pass to function
    """

    if delete_keys:
        args = func_dict.pop("load_function_args", [])
        kwargs = func_dict.pop("load_function_kwargs", {})
        base_name = func_dict.pop("load_function_name", 'process_dataset_default')
        func_mod_name = func_dict.pop('load_function_module', None)
    else:
        args = func_dict.get("load_function_args", [])
        kwargs = func_dict.get("load_function_kwargs", {})
        base_name = func_dict.get("load_function_name", 'process_dataset_default')
        func_mod_name = func_dict.get('load_function_module', None)

    fail_func = partial(process_dataset_default, dataset_name=base_name)

    if func_mod_name:
        raise Exception('Not implemented yet')
        # func_mod = importlib.import_module(func_mod_name)
    else:
        func_mod = _MODULE
    func_name = getattr(func_mod, base_name, fail_func)
    func = partial(func_name, *args, **kwargs)

    return func


def serialize_partial(func):
    """Serialize a function call to a dictionary.
    Parameters
    ----------
    func: partial function.
    Returns
    -------
    dict containing:
        load_function_name: function name
        load_function_module: fully-qualified module name containing function
        load_function_args: args to pass to function
        load_function_kwargs: kwargs to pass to function
    """

    func = partial(func)
    entry = {}
    entry['load_function_module'] = ".".join(jfi.get_func_name(func.func)[0])
    entry['load_function_name'] = jfi.get_func_name(func.func)[1]
    entry['load_function_args'] = func.args
    entry['load_function_kwargs'] = func.keywords
    return entry


def reservoir_sample(filename, n_samples=1, random_seed=None):
    """Return a random subset of lines from a file
    Parameters
    ----------
    filename: path
        File to be loaded
    n_samples: int
        number of lines to return
    random_seed: int or None
        If set, use this as the random seed
    """
    if random_seed is not None:
        random.seed(random_seed)
    sample = []
    with open(filename) as f:
        for n, line in enumerate(f):
            if n < n_samples:
                sample.append(line.rstrip())
            else:
                r = random.randint(0, n_samples)
                if r < n_samples:
                    sample[r] = line.rstrip()
    return sample

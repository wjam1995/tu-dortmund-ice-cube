'''
A module to load data and scale appropriately (based on methods and classes in 
maxTools.waveform_dataset)

'''
import numpy as np

from maxTools import waveform_dataset

from sklearn.preprocessing import StandardScaler

def load_data(verbose=True, train_ratio=0.8, test_ratio=0.13, rescale=True):
    ''' 
    Load data using methods in maxTools.waveform_dataset, preprocess it, and 
    return the resulting Datasets object

    The data is preprocessed to have mean of 0 and variance of 1. 

    Arguments:
        verbose - print data about scaling
        train_ratio - ratio of data loaded designated for training
        test_ratio - ratio of data loaded set aside for testing

    Returns: 
        data - a Datasets object, a named tuple of three DataSet objects 
               (train, val and test), each with the following structure:
            waveforms - an array of shape [n, 128] with the waveform data
            labels - a one-hot array of shape [n, 2] with the correct labels
            weights - an array of shape [n] with weights for events
            ids - an array of shape [n] with ids for events
            methods for generating batches of data
            
    For further information on the DataSet object, refer to its definition in
    maxTools.waveform_dataset

    '''
    # Selected datasets
    datasets = [
        ('11538', ['DP', 'NC'], 3638),  # Tau
        ('12034', ['CC', 'NC'], 8637),  # Electron
        ('11069', ['NC'], 7287)         # Muon
        # NB - discard muon track events because of similarity to dp events
    ]

    # Read in data - output is split into train, val and test
    if verbose:
        print("Loading Data...")
    data = waveform_dataset.read_data(
            datasets, 
            combined=True, 
            train_ratio=train_ratio, 
            test_ratio=test_ratio,
            verbose=verbose
        )

    # Rescale input data to give training data mean 0 and stdev 1
    if rescale is True:
        rescaler = StandardScaler(copy=False)
        rescaler.fit_transform(data.train.waveforms)
        rescaler.transform(data.val.waveforms)
        rescaler.transform(data.test.waveforms)
        
    return data

def load_eval_data(verbose=True, train_ratio=0.8, test_ratio=0.13, rescale=True):
    ''' 
    Load evaluation data using methods in maxTools.waveform_dataset, preprocess
    it, and return the resulting Datasets object

    The data is preprocessed to have mean of 0 and variance of 1. 

    Arguments:
        verbose - print data about scaling
        train_ratio - ratio of data loaded designated for training
        test_ratio - ratio of data loaded set aside for testing

    Returns: 
        data - a Datasets object, a named tuple of three DataSet objects 
               (train, val and test), each with the following structure:
            waveforms - an array of shape [n, 128] with the waveform data
            labels - a one-hot array of shape [n, 2] with the correct labels
            weights - an array of shape [n] with weights for events
            ids - an array of shape [n] with ids for events
            methods for generating batches of data
            
    For further information on the DataSet object, refer to its definition in
    maxTools.waveform_dataset

    '''
    # Selected datasets
    datasets = [
        ('11538', ['DP', 'NDP', 'NC'], 3638),  # Tau neutrinos
        ('12034', ['CC', 'NC'], 8637),  # Electron neutrinos
        ('11069', ['NC', 'CC'], 7287),   # Muon neutrinos
        ('11057', ['AM'], 74890)        # Atmospheric muons
    ]

    # Read in data - output is split into train, val and test
    if verbose:
        print("Loading Data...")
    data = waveform_dataset.read_data(
            datasets, 
            combined=True, 
            train_ratio=train_ratio, 
            test_ratio=test_ratio,
            load_eval_data=True,
            verbose=verbose
        )

    # Rescale input data to give training data mean 0 and stdev 1
    if rescale is True:
        mask = np.logical_or((data.train.labels[:, 0] == 1), (data.train.labels[:, 1] == 1))
        rescaler = StandardScaler(copy=False)
        rescaler.fit(data.train.waveforms[mask])
        rescaler.transform(data.train.waveforms)
        rescaler.transform(data.val.waveforms)
        rescaler.transform(data.test.waveforms)
        
    return data

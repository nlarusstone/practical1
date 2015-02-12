import csv
import gzip
import pandas
import numpy as np

train_filename = '../train.csv.gz'
test_filename  = '../test.csv.gz'
pred_filename  = 'example_mean.csv'

# Load the training file.
train_data = []
with gzip.open(train_filename, 'r') as train_fh:

    # Parse it as a CSV file.
    train_csv = csv.reader(train_fh, delimiter=',', quotechar='"')
    
    # Skip the header row.
    next(train_csv, None)

    counter = 0
    # Load the data.
    for row in train_csv:
        if counter > 200:
            break
        smiles   = row[0]
        features = np.array([float(x) for x in row[1:257]])
        gap      = float(row[257])
        print(smiles)
        print""
        
        train_data.append({ 'smiles':   smiles,
                            'features': features,
                            'gap':      gap })
        counter += 1

# Compute the mean of the gaps in the training data.
#w = np.linalg.solve(np.dot(Phi.T, Phi) , np.dot(Phi.T, Y))
gaps = np.array([datum['gap'] for datum in train_data])
mean_gap = np.mean(gaps)

# Load the test file.
test_data = []
with gzip.open(test_filename, 'r') as test_fh:

    # Parse it as a CSV file.
    test_csv = csv.reader(test_fh, delimiter=',', quotechar='"')
    
    # Skip the header row.
    next(test_csv, None)
    counter = 0
    # Load the data.
    for row in test_csv:
        if counter > 200:
            break
        id       = row[0]
        smiles   = row[1]
        features = np.array([float(x) for x in row[2:258]])
        
        test_data.append({ 'id':       id,
                           'smiles':   smiles,
                           'features': features })
        counter += 1

# Write a prediction file.
with open(pred_filename, 'w') as pred_fh:

    # Produce a CSV file.
    pred_csv = csv.writer(pred_fh, delimiter=',', quotechar='"')

    # Write the header row.
    pred_csv.writerow(['Id', 'Prediction'])

    for datum in test_data:
        pred_csv.writerow([datum['id'], mean_gap])

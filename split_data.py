import sys
import os
import pandas as pd
import numpy as np
import argparse
from sklearn.model_selection import train_test_split


parser = argparse.ArgumentParser()
parser.add_argument('--data_dir', type=str, default='./data', help='data dir path')
parser.add_argument('--val_size', type=float, default=0.1, help='validation set size proportion (range: 0.0 - 1.0)')
parser.add_argument('--test_size', type=float, default=0.01, help='test set size proportion (range: 0.0 - 1.0)')
args = parser.parse_args()

data_dir = args.data_dir
val_size = args.val_size
test_size = args.test_size

print('splitting train/test with params: %s...' % (str(args)))

# load source/target
source_filenames = [f for f in os.listdir('%s/source' % data_dir) if '.png' in f]
target_filenames = [f for f in os.listdir('%s/target' % data_dir) if '.png' in f]

# validate same filenames
print('found %d source files and %d target files...' % (len(source_filenames), len(target_filenames)))
assert set(source_filenames) == set(target_filenames)
print('source and target sets are matching...')

dicts_all = []
for filename in source_filenames:
    idx = int(filename.split('_')[1].split('.')[0])
    dicts_all.append({'img_idx': idx, 'source': 'source/%s' % filename, 'target': 'target/%s' % filename})

df_all = pd.DataFrame(dicts_all)
source_train, source_val, target_train, target_val = train_test_split(df_all['source'], df_all['target'], test_size=val_size, random_state=42)
source_train, source_test, target_train, target_test = train_test_split(source_train, target_train, test_size=test_size, random_state=42)

train = pd.DataFrame([source_train, target_train]).T
validation = pd.DataFrame([source_val, target_val]).T
test = pd.DataFrame([source_test, target_test]).T

print('split sets to sizes train: %d, validation: %d, test: %d...' % (len(train), len(validation), len(test)))

print('saving to csvs...')
train.to_csv('%s/train.csv' % data_dir, index=False)
validation.to_csv('%s/val.csv' % data_dir, index=False)
test.to_csv('%s/test.csv' % data_dir, index=False)

print('success')

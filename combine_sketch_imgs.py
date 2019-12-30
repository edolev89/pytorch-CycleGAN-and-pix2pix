import os
import argparse
import pandas as pd
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('--from_data_dir', type=str, default='.', help='from data dir path')
parser.add_argument('--to_data_dir', type=str, default='.', help='to data dir path')
parser.add_argument('--resize_to', type=int, default=None, help='to size')
parser.add_argument('--resize_mode', type=str, default=None, help='antialiase or none')
parser.add_argument('--sets', nargs='+', default=['train', 'test', 'val'], help='train,val,test')
parser.add_argument('--output_format', type=str, default='png', help='output format')
parser.add_argument('--filename_index_offset', type=int, default=0, help='output format')
args = parser.parse_args()

from_data_dir = args.from_data_dir
to_data_dir = args.to_data_dir
resize_to = args.resize_to
sets = args.sets
output_format = args.output_format
resize_mode = args.resize_mode
filename_index_offset = args.filename_index_offset

print('creating dirs...')

dfs = []
for set_type in sets:
    set_dir = '%s/%s' % (to_data_dir, set_type)

    if not os.path.exists(set_dir):
        os.makedirs(set_dir, exist_ok=True)

    print('loading filenames for %s...' % set_type)
    filenames_df = pd.read_csv('%s/%s.csv' % (from_data_dir, set_type))

    dfs.append((set_dir, filenames_df))

for to_path, filenames_df in dfs:
    print('processing data...')
    for idx, filename_row in filenames_df.iterrows():
        full_source_path = '%s/%s' % (from_data_dir, filename_row['source'])
        full_target_path = '%s/%s' % (from_data_dir, filename_row['target'])
        source_img = Image.open(full_source_path)
        target_img = Image.open(full_target_path)

        if resize_to is not None:
            if resize_mode == 'antialias':
                source_img = source_img.resize((resize_to, resize_to), Image.ANTIALIAS)
                target_img = target_img.resize((resize_to, resize_to), Image.ANTIALIAS)
            else:
                source_img = source_img.resize((resize_to, resize_to))
                target_img = target_img.resize((resize_to, resize_to))

        w, h = source_img.size
        new_img = Image.new('L', (w * 2, h))
        new_img.paste(source_img, (0, 0))
        new_img.paste(target_img, (w, 0))

        filename = idx + filename_index_offset
        new_img.save('%s/%d.%s' % (to_path, filename, output_format))
#        if idx == 5:
#            break

print('done')

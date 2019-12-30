import pandas as pd
import os
from collections import defaultdict

all_dict = defaultdict(list)
for name, full_path, rel_path in [('source', 'datasets/sketch/test/output/sketch', 'test/output/sketch'), ('target', 'datasets/sketch/test/output/depth', 'test/output/depth')]:
    for filename in os.listdir(full_path):
        if '.png' in filename:
            all_dict[name].append('%s/%s' % (rel_path, filename))

pd.DataFrame(all_dict).to_csv('datasets/sketch/test.csv', index=False)

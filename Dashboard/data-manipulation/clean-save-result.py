import os
import json
import pickle5 as pkl
from pathlib import Path
from collections import defaultdict

curr_dir = Path(os.getcwd())
parent_dir = curr_dir.parent
source_dir = parent_dir.parent
result_dir = os.path.join(source_dir, 'pkl_results')
output_dir = os.path.join(parent_dir, 'dashboard', 'src', 'charts', 'data')
output_file_nn_houses = os.path.join(output_dir, 'nn_houses.json')
output_file_nn_appliances = os.path.join(output_dir, 'nn_appliances.json')
output_file_svm = os.path.join(output_dir, 'svm_results.json')

if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

houses = defaultdict(list)
appliances = []

for file in os.listdir(result_dir):

    file_dir = os.path.join(result_dir, file)
    model = file.split('_')[0]

    if model == 'nn':

        house = file[11:18]
        appliance = file[19:-4]

        inner_dict = {'appliance': appliance}
        appliance_dict = {'appliance': appliance, 'house': house}

        with open(file_dir, 'rb') as f:

            df = pkl.load(f)
            df['timestamp'] = df['timestamp'].astype(str)
            total_usage = df['prediction'].sum()
            appliance_dict['usage'] = total_usage
            inner_dict['values'] = df.to_dict(orient='records')

        appliances.append(appliance_dict)
        houses[house].append(inner_dict)

    if model == 'svm':

        appliance = file[19:-4]

        with open(file_dir, 'rb') as f:

            appliances[appliance] = pkl.load(f)


if not os.isfile(output_file_nn_houses):
    with open(output_file_nn_houses, 'w') as f:
        json.dump(houses, f)

if not os.isfile(output_file_nn_appliances):
    with open(output_file_nn_appliances, 'w') as f:
        json.dump(appliances, f)

if not os.isfile(output_file_svm):
    with open(output_file_svm, 'w') as f:
        json.dump(houses, f)




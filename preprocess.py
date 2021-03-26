import pandas as pd
import os

"""
Data is organized into a dictionary where key=house number and value= pandas dataframe for that house
Each house dataframe is composed of columns=appliance and rows=timestamp
For our 2 appliances I chose lighting and washer/dryer. Once the dataframes are built, I exclude all other appliances from the dataframe
My thought is to train on houses 1-4, test on houses 5-6
I use abbreviation l_wd to stand for lighting/washer_dryer
"""

cwd = os.getcwd()
path = f'{cwd}/'

def gather_all_files(path):

    all_files = []

    for house_num in range(1, 7):
        house_file = f'{path}low_freq/house_{house_num}'
        all_files.append(house_file)

    return all_files


def create_dataframes(all_files):

    house_data_dict = {}
    house_num = 1
    for file in all_files:

        with open(f'{file}/labels.dat') as f:
            labels = f.read().splitlines()
            for i in range(len(labels)):
                labels[i] = labels[i].replace(' ', '_')

        df = pd.read_table(f'{file}/channel_1.dat', sep=' ', names=['timestamp', labels[0]])
        df['timestamp'] = df['timestamp'].astype("datetime64[s]")

        for i in range(1, len(labels)):

            data = pd.read_table(f'{file}/channel_{i+1}.dat', sep=' ', names=['timestamp', labels[i]])
            data['timestamp'] = data['timestamp'].astype("datetime64[s]")
            df = pd.merge(df, data, how='inner', on='timestamp')

        df = df.set_index(df['timestamp'].values)
        df.drop(['timestamp'], axis=1, inplace=True)
        df.index.name = 'timestamp'

        house_data_dict[house_num] = df
        house_num += 1

    return house_data_dict


def select_appliances(house_data_dict):

    reduced_house_data_dict = {}
    for i in range(1, 7):
        df = house_data_dict[i]
        l_wd_cols = [col for col in df.columns if 'lighting' in col]
        l_wd_cols += [col for col in df.columns if 'washer_dryer' in col]
        l_wd_cols += [col for col in df.columns if 'mains' in col]
        df = df[l_wd_cols]
        reduced_house_data_dict[i] = df

    return reduced_house_data_dict

def get_preproccess_data():
    all_files = gather_all_files(path)
    house_data_dict = create_dataframes(all_files)
    reduced_house_data_dict = select_appliances(house_data_dict)

    return reduced_house_data_dict

def main():
    reduced_house_data_dict = get_preproccess_data()
    for i in range(1, 7):

        print(f'House {i} Shape: {reduced_house_data_dict[i].shape}')
        print(f'First 3 Rows House {i}: {reduced_house_data_dict[i].head(3)}')

if __name__ == "__main__" :
    main()
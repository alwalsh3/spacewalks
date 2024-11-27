import matplotlib.pyplot as plt
import pandas as pd


def read_json_to_dataframe(input_file):
    """
    Read the data from a JSON file into a Pandas dataframe.
    Clean the data by removing any incomplete rows and sort by date

    Args:
        input_file (str): the path to the JSON file.
    Returns:
        eva_df (pd.DataFrame): The cleaned and sorted data as a dataframe
    """
    eva_df = pd.read_json(input_file, convert_dates=['date'])
    eva_df['eva'] = eva_df['eva'].astype(float)
    eva_df.dropna(axis=0, inplace=True)
    eva_df.sort_values('date', inplace=True)
    return eva_df


def write_dataframe_to_csv(df, output_file):
    """
    Saves the dataframe containing data from JSON file to a CSV

    Args:
        df (pd.DataFrame): dataframe condtaining JSON file data
        output_file (str): name of CSV file to be saved to
    """
    print(f'Saving to CSV file {output_file}')
    df.to_csv(output_file, index=False)


# https://data.nasa.gov/resource/eva.json (with modifications)
input_file = open('eva-data.json', 'r')
output_file = open('eva-data.csv', 'w')  # JSON data output to this CSV file
graph_file = './cumulative_eva_graph.png'  # name that graph will be saved to


# Read in and clean up data - including sorting by date
eva_data = read_json_to_dataframe(input_file)

# convert and save data to CSV file
write_dataframe_to_csv(eva_data, output_file)


# extract duration date from dataframe, and calculate sum of duration
# of spacewalks in hours
eva_data['duration_hours'] = eva_data['duration'].str.split(":").apply(
    lambda x: int(x[0]) + int(x[1])/60)
eva_data['cumulative_time'] = eva_data['duration_hours'].cumsum()

# plot cumulative time vs date and save output graph
plt.plot(eva_data['date'], eva_data['cumulative_time'], 'ko-')
plt.xlabel('Year')
plt.ylabel('Total time spent in space to date (hours)')
plt.tight_layout()
plt.savefig(graph_file)
plt.show()

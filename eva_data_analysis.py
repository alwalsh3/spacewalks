import os
import matplotlib.pyplot as plt
import pandas as pd
import sys

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


def plot_cumulative_time_in_space(df, graph_file):
    """
    fill in...
    """
    # extract duration date from dataframe, and calculate sum of duration
    # of spacewalks in hours
    df = add_duration_hours_variable(df)
    df['cumulative_time'] = df['duration_hours'].cumsum()

    plt.plot(df['date'], df['cumulative_time'], 'ko-')
    plt.xlabel('Year')
    plt.ylabel('Total time spent in space to date (hours)')
    plt.tight_layout()
    plt.savefig(graph_file)
    plt.show()


def text_to_duration(duration):
    """
    Convert a text format duration "HH:MM" to duration in hours

    Args:
        duration (str): The duration in HH:MM

    Returns:
    duration_hours (float): The duration in hours
    """
    hours, minutes = duration.split(":")
    duration_hours = int(hours) + int(minutes)/60
    return duration_hours


def add_duration_hours_variable(df):
    """
    Add duration in hours (duration_hours) variable to the dataset

    Args:
        df (pd.DataFrame): The input dataframe

    Returns:
        df_copy (pd.DataFrame): A copy of the df_ with the new duration_hours variable added
    """
    df_copy = df.copy()
    df_copy['duration_hours'] = df_copy['duration'].apply(text_to_duration)
    return df_copy


if __name__ == "__main__":

    if not os.path.exists('./results/'):
        os.makedirs('./results/')
    if len(sys.argv) < 3:
        # less than 3 command line arguments, assuming we use default file names
        # https://data.nasa.gov/resource/eva.json (with modifications)
        input_file = open('data/eva-data.json', 'r')
        output_file = open('results/eva-data.csv', 'w')  # JSON data output to this CSV file
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

    graph_file = 'results/cumulative_eva_graph.png'  # name that graph will be saved to

    # Read in and clean up data - including sorting by date
    eva_data = read_json_to_dataframe(input_file)

    # convert and save data to CSV file
    write_dataframe_to_csv(eva_data, output_file)

    # plot cumulative time vs date and save output graph
    plot_cumulative_time_in_space(eva_data, graph_file)

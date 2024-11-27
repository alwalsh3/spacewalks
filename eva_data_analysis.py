import matplotlib.pyplot as plt
import pandas as pd

# https://data.nasa.gov/resource/eva.json (with modifications)
input_file = open('eva-data.json', 'r') 
output_file = open('eva-data.csv','w') # JSON data output to this CSV file
graph_file = './cumulative_eva_graph.png' # name and location that graph will be saved to

# Read in and clean up data - including sorting by date
eva_df = pd.read_json(input_file, convert_dates=['date'])
eva_df['eva'] = eva_df['eva'].astype(float)
eva_df.dropna(axis=0, inplace=True)
eva_df.sort_values('date', inplace=True)

# convert and save data to CSV file
eva_df.to_csv(output_file, index=False)

# extract duration date from dataframe, and calculate sum of duration of spacewalks in hours
eva_df['duration_hours'] = eva_df['duration'].str.split(":").apply(lambda x: int(x[0]) + int(x[1])/60)
eva_df['cumulative_time'] = eva_df['duration_hours'].cumsum()

# plot data and save graph file
plt.plot(eva_df['date'],eva_df['cumulative_time'], 'ko-')
plt.xlabel('Year')
plt.ylabel('Total time spent in space to date (hours)')
plt.tight_layout()
plt.savefig(graph_file)
plt.show()

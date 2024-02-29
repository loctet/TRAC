import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
import time
import plotly.graph_objects as go
from Settings import s_labels, s_time_metrics


def comma_separated_strings(string):
    """
    Splits a string into a list using commas as separators.

    :param string: The input string to split (str).
    :return: A list of strings obtained by splitting the input string. (list)
    """
    return string.split(',')

class CSVDataPlotter:
    """
    A class to plot data from CSV files using various types of plots including candlestick,
    2D line, bar, scatter, 3D scatter, and 4D scatter plots.
    """
    def __init__(self, csv_file_path):
        """
        Initializes the CSVDataPlotter with the path to a CSV file.

        Parameters:
        - csv_file_path (str): The path to the CSV file to plot data from.
        """
        self.csv_file_path = csv_file_path
        self.data = pd.read_csv(csv_file_path)

    def plot_candle(self, fields, pl_lines):
        """
        Plots a candlestick chart for grouped state data from the CSV file.

        Parameters:
        - fields (list): The fields to group the data by.
        - pl_lines (list): The lines to plot.
        """
        # Aggregate the data to get min/max num_states and execution_time for each group
        self.data[pl_lines[0]] = self.data[pl_lines[0]] / 10000000

        grouped = self.data.groupby(fields[0]).agg(
            min_num_states=pd.NamedAgg(column='num_states', aggfunc='min'),
            max_num_states=pd.NamedAgg(column='num_states', aggfunc='max'),
            min_execution_time=pd.NamedAgg(column=pl_lines[0], aggfunc='min'),
            max_execution_time=pd.NamedAgg(column=pl_lines[0], aggfunc='mean')
        ).reset_index()

        grouped[fields[0]] = grouped.groupby(fields[0])[pl_lines[0]].transform(lambda x: x.median())

        # Create a candlestick chart
        fig = go.Figure(data=[go.Candlestick(x=grouped[fields[0]],
                    open=grouped['min_num_states'], high=grouped['max_execution_time'],
                    low=grouped['min_execution_time'], close=grouped['max_num_states'],
                    increasing_line_color='green', decreasing_line_color='red')])

        fig.update_layout(
            title='Candlestick Chart for Grouped State Data',
            xaxis_title='Group',
            yaxis_title='Value',
            yaxis=dict(
                autorange=True,
                showgrid=True,
                zeroline=True,
                dtick=5,
                gridcolor='rgb(255, 255, 255)',
                gridwidth=1,
                zerolinecolor='rgb(255, 255, 255)',
                zerolinewidth=2,
            ),
            margin=dict(
                l=40,
                r=40,
                b=20,
                t=40,
            ),
            paper_bgcolor='rgb(243, 243, 243)',
            plot_bgcolor='rgb(243, 243, 243)',
        )

        fig.show()

    def plot_csv_data_2d(self, fields, pl_lines, typeP = 'line'):
        """
        Plots 2D data from the CSV file as line, bar, or scatter plots.
        
        :param fields: The fields to plot.
        :type fields: list
        
        :param pl_lines: The lines to plot.
        :type pl_lines: list
        
        :param typeP: The type of plot ('line', 'bar', or 'scatter').
        :type typeP: str
        """
        self.data = self.data[self.data["is_time_out"] == False]
        for field in fields:
            sorted_data = self.data.sort_values(field)

            to_normalize = sorted_data['average_bf_num']
            # Normalize the 'average_bf_num' for color mapping
            average_bf_num_normalized = to_normalize

            plt.figure(figsize=(12, 8))
            space = - 0.2
            for line in pl_lines:
                sorted_data[line] = sorted_data[line] / 10e6
                if typeP == 'line': 
                    plt.plot(sorted_data[field], sorted_data[line])
                elif typeP == 'bar' :
                    plt.bar(sorted_data[field] + space, sorted_data[line], 0.4)
                elif typeP == 'scatter' :
                    plt.scatter(sorted_data[field], sorted_data[line], c=average_bf_num_normalized)
                space += 0.2

                plt.xlabel(s_labels[field])
                plt.ylabel('Time in ms')
                plt.title(f'Variation of {line} Metrics with {s_labels[field]}')
                plt.legend()
                plt.grid(True)
                plt.yscale("linear")
                plt.xscale("linear")
                plt.colorbar(label="Branching factor", orientation="vertical") 
                plt.savefig(self.csv_file_path.replace(".csv",  f'_{line} Metrics with {field}_{time.time()}_linear_linear.png'))
                plt.show()

    def plot_csv_data_3d(self, fields, time_metrics):
        """
        Plots 3D data from the CSV file.

        :param fields: The fields to plot on the x and y axes.
        :type fields: list
        :param time_metrics: The metrics to plot on the z-axis.
        :type time_metrics: list
        """

        if len(fields) != 2 or len(time_metrics) == 0:
            raise Exception("fields len should be 2")

        for metric in time_metrics:
            fig = plt.figure(figsize=(10, 7))
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(self.data[fields[0]], self.data[fields[1]], self.data[metric], label=metric)
            ax.set_xlabel(fields[0])
            ax.set_ylabel(fields[1])
            ax.set_zlabel(f'{metric}')
            ax.set_title(f'3D Plot of {metric} against {fields[0]} and {fields[1]}')
            ax.legend()

            plt.savefig(self.csv_file_path.replace(".csv", f"3D Plot of {metric} against {fields[0]} and {fields[1]}_{time.time()}.png"))
            plt.show()

    def plot_csv_data_4d(self, fields):
        """
        Plots 4D data from the CSV file using color mapping for the fourth dimension.

        Parameters:
        - fields (list): The fields to plot on the x, y, and z axes.
        """
        data = self.data
        _4d_data_in = data['average_bf_num']

        # Create a colormap
        cmap = plt.get_cmap('viridis')

        for i, metric in enumerate(s_time_metrics):
            fig = plt.figure(figsize=(10, 7))
            ax = fig.add_subplot(111, projection='3d')
            scatter = ax.scatter(data[fields[0]], data[fields[1]], data[metric], c=_4d_data_in, cmap=cmap)

            # Set labels, title, and axes limits
            ax.set_xlabel(s_labels[fields[0]])
            ax.set_ylabel(s_labels[fields[1]])
            ax.set_zlabel(f'{s_labels[metric]}')
            ax.set_title(f'{s_labels[metric]}')
            
            # Set x and y axes to start from 1
            ax.set_xlim([1, max(data[fields[0]])])
            ax.set_ylim([1, max(data[fields[1]])])
            #ax.set_zlim([1, max(data[metric])])

            # Colorbar to show the scale of 'average_bf_num'
            cbar = fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)
            cbar.set_label('Average BF Num (N)')
            
            # Save the plot to a PNG file
            plt.savefig(self.csv_file_path.replace(".csv", f"{fields[0]}_{fields[1]}_{metric}_4d_{time.time()}.png"))
        
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Plots')
    parser.add_argument('directory', type=str, help='Dir where tests data CSV is located')
    parser.add_argument('--shape', type=str, default = '2d', choices= ['2d', '3d', '4d'], help='Type of shape')
    parser.add_argument('--file', type=str, default = 'merged_list_of_files_info', help='Csv File Name without "csv"')
    parser.add_argument('--fields', type=comma_separated_strings, default = ['num_states'], help='collumn to plot agains time num_state is the defalt')
    parser.add_argument('--pl_lines', type=comma_separated_strings, default=['participants_time', 'non_determinism_time', 'a_consistency_time', 'z3_running_time'], help='Lines to plot')
    parser.add_argument('--type_plot', type=str, default= 'line',  choices= ['line', 'scatter', 'bar'], help='Type of 2D to plot')
    
    args = parser.parse_args()
    
    path = os.path.join('./examples/random_txt/', args.directory, f"{args.file}.csv")
    plotter = CSVDataPlotter(path)

    if args.shape == '2d':
        plotter.plot_csv_data_2d(args.fields, args.pl_lines, args.type_plot)
    elif args.shape == "3d":
        plotter.plot_csv_data_3d(args.fields, args.pl_lines)
    elif args.shape == "4d":
        plotter.plot_csv_data_4d(args.fields)
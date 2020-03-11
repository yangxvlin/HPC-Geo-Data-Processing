"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-3-10 15:28:34
Description: 
"""

from datetime import datetime
from functools import reduce

import mpi4py.MPI as MPI
import numpy as np
import argparse
from pprint import pprint
from TwitterData import TwitterData
from util import read_grid_information, read_data_line_by_line, preprocess_data
from GridSummary import GridSummary


def main(grid_data_path, geo_data_path):
    grids_summary = read_grid_information(grid_data_path)
    grids_summary_dict = {}
    # all_grids_id = []
    for g in grids_summary:
        grids_summary_dict[g.grid.id] = g

    # initialize communicator
    comm = MPI.COMM_WORLD
    comm_rank = comm.Get_rank()
    comm_size = comm.Get_size()
    # print(comm_rank, comm_size)

    start = datetime.now()

    # only one process, no need to split data
    if comm_size == 1:
        for line in read_data_line_by_line(geo_data_path):
            preprocessed_line = preprocess_data(line)
            # the line is data
            if preprocessed_line:
                twitter_data = TwitterData(preprocessed_line)
                grids_summary = list(map(lambda x: x.summarize(twitter_data), grids_summary))

    else:
        if comm_rank == 0:
            next_target = 1
            send_count = 0

            for line in read_data_line_by_line(geo_data_path):
                preprocessed_line = preprocess_data(line)
                # the line is data
                if preprocessed_line:
                    send_count += 1
                    comm.send(preprocessed_line, next_target)
                    # scatter data line by line to slave process
                    next_target += 1
                    if next_target == comm_size:
                        next_target = 1
                # print("process #{} line {}".format(comm_rank, i))

            for i in range(1, comm_size):
                comm.send(None, i)
            print("process #{} send {} lines.".format(comm_rank, send_count))

        else:
            recv_count = 0
            while True:
                local_preprocessed_line = comm.recv(source=0)
                if not local_preprocessed_line:
                    break

                recv_count += 1
                twitter_data = TwitterData(local_preprocessed_line)
                grids_summary = list(map(lambda x: x.summarize(twitter_data), grids_summary))

            print("process #{} recv {} lines.".format(comm_rank, recv_count))
            # print(grids_summary)
            # print(grids_summary_dict)

    reduced_grids_summary_dict = comm.reduce(grids_summary_dict, root=0, op=GridSummary.merge_grid_summary_list)

    # output summary in root process
    if comm_rank == 0:
        merged_grids_summary = sorted(reduced_grids_summary_dict.values(), key=lambda x: x.count, reverse=True)
        pprint(merged_grids_summary)

        end = datetime.now()
        print(f"Programs runs", end - start)


if __name__ == "__main__":
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='python to process data')
    # Required grid data path
    parser.add_argument('-grid', type=str, help='A required string path to grid file')
    # Required geo data path
    parser.add_argument('-data', type=str, help='A required string path to geo data file')
    args = parser.parse_args()

    grid = args.grid
    data = args.data

    main(grid, data)

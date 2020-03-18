"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-3-10 15:28:34
Description: 
"""

from datetime import datetime
import mpi4py.MPI as MPI
import numpy as np
import argparse
from pprint import pprint
from TwitterData import TwitterData
from LanguageSummary import LanguageSummary
from util import read_language_code, read_data_line_by_line, preprocess_data, top_n_hash_tags


LANGUAGE_CODE_FILE = "./language.json"


def main(geo_data_path):
    """
    :param geo_data_path:
    TODO optimize summarize(), i.e. do graph search in stead of looping over all grids
    """
    # initialize communicator
    comm = MPI.COMM_WORLD
    comm_rank = comm.Get_rank()
    comm_size = comm.Get_size()
    # print(comm_rank, comm_size)

    start = datetime.now()
    language_summary_dict = read_language_code(LANGUAGE_CODE_FILE)
    # TODO should read grid info in each process?
    # read_grid_info_end = datetime.now()
    # print("process #{} takes {} to read grid info.".format(comm_rank, read_grid_info_end - start))

    # only one process, no need to split data
    if comm_size == 1:
        line_count = 0
        for line in read_data_line_by_line(geo_data_path):
            preprocessed_line = preprocess_data(line)
            line_count += 1
            # the line is data
            if preprocessed_line:
                twitter_data = TwitterData(preprocessed_line)
                try:
                    language_summary_dict[twitter_data.language_code].summarize(twitter_data)
                except KeyError:
                    print("unknown language_code:", twitter_data.language_code)
        print("processor #{} processes {} lines.".format(comm_rank, line_count))

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

            for i in range(1, comm_size):
                comm.send(None, i)
            print("processor #{} send {} lines.".format(comm_rank, send_count))

        else:
            recv_count = 0
            while True:
                local_preprocessed_line = comm.recv(source=0)
                if not local_preprocessed_line:
                    break

                recv_count += 1
                twitter_data = TwitterData(local_preprocessed_line)
                language_summary_dict[twitter_data.language_code].summarize(twitter_data)

            print("processor #{} recv {} lines.".format(comm_rank, recv_count))

    reduced_language_summary_dict = comm.reduce(language_summary_dict, root=0, op=LanguageSummary.merge_language_list)

    # output summary in root process
    if comm_rank == 0:
        merged_language_summary_list = sorted(reduced_language_summary_dict.values(), key=lambda x: x.count, reverse=True)
        pprint(top_n_hash_tags(reduced_language_summary_dict.values()))

        pprint(merged_language_summary_list[:10])
        # pprint(merged_language_summary_list)

        end = datetime.now()
        print(f"Programs runs", end - start)


if __name__ == "__main__":
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='python to process data')
    # Required geo data path
    parser.add_argument('-data', type=str, help='A required string path to data file')
    args = parser.parse_args()

    data = args.data

    main(data)

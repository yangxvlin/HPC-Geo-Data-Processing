"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-3-10 15:28:34
Description: main function
"""
import argparse
import heapq
import operator
import time
from collections import Counter

import numpy as np
from mpi4py import MPI

from util import read_data_line_by_line, preprocess_data, dump_time, read_n_lines, read_language_code_dict, processing_data, merge_list, dump_hash_tag_output, \
    dump_country_code_output, dump_num_processor


def main(country_code_file_path, twitter_data_path):
    """
    :param country_code_file_path: the path of country_code_file
    :param twitter_data_path: the path of twitter_data
    """
    program_start = time.time()
    # initialize communicator
    comm = MPI.COMM_WORLD
    comm_rank = comm.Get_rank()
    comm_size = comm.Get_size()

    language_code_dict = None

    # read country_code in master process
    if comm_rank == 0:
        dump_num_processor(comm_size)
        # the starting timestamp
        tmp_start = time.time()
        # read country_code info and broad cast
        language_code_dict = read_language_code_dict(country_code_file_path)
        dump_time(comm_rank, "reading country code file", time.time() - tmp_start)

    # counting hash_tag
    hash_tag_count = Counter()
    language_code_count = Counter()

    # calculating number of lines of data to be processed, line to start, line to end
    tmp_start = time.time()
    n_lines = comm.bcast(read_n_lines(twitter_data_path), root=0)
    lines_per_core = n_lines // comm_size
    lines_to_end = n_lines + 1  # ignore first line
    line_to_start = 1 + lines_per_core * comm_rank  # ignore first line
    line_to_end = line_to_start + lines_per_core
    if comm_rank == comm_size - 1:  # last core to finish all remaining lines
        line_to_end = lines_to_end

    # processing lines in specified range
    for line_number, line in enumerate(read_data_line_by_line(twitter_data_path)):  # ignore first line
        if line_number == line_to_end:
            break
        if line_number >= line_to_start:
            preprocessed_line = preprocess_data(line)
            if preprocessed_line:
                processing_data(preprocessed_line, hash_tag_count, language_code_count)
    dump_time(comm_rank, "processing data", time.time() - tmp_start)

    n = 10
    tmp_start = time.time()
    # concurrent calculating top n hash_tags, languages used
    if comm_size > 1:
        # 1) merge Counter from each processor
        reduced_language_code_count = comm.reduce(language_code_count, root=0, op=operator.add)
        reduced_hash_tag_count = comm.reduce(hash_tag_count, root=0, op=operator.add)
        reduced_hash_tag_count = reduced_hash_tag_count.most_common(n)
        reduced_language_code_count = reduced_language_code_count.most_common(n)
        # 2) split merged to each processor
        # if comm_rank == 0:
        #     split_language_code_np_array = np.array_split(list(reduced_language_code_count.items()), comm_size)
        #     split_hash_tag_np_array = np.array_split(list(reduced_hash_tag_count.items()), comm_size)
        # else:
        #     split_language_code_np_array = None
        #     split_hash_tag_np_array = None
        #
        # # 3) scatter merged to each processor
        # local_language_code = list(map(lambda x: (x[0], int(x[1])), comm.scatter(split_language_code_np_array, root=0)))
        # local_hash_tag = list(map(lambda x: (x[0], int(x[1])), comm.scatter(split_hash_tag_np_array, root=0)))
        #
        # # 4) merge each processor's top n calculation result
        # reduced_language_code_count = comm.reduce(heapq.nlargest(n, local_language_code, lambda x: x[1]), root=0, op=merge_list)
        # reduced_hash_tag_count = comm.reduce(heapq.nlargest(n, local_hash_tag, lambda x: x[1]), root=0, op=merge_list)
    # single processor calculating top n
    else:
        reduced_hash_tag_count = hash_tag_count.most_common(n)
        reduced_language_code_count = language_code_count.most_common(n)
    dump_time(comm_rank, "calculating top n", time.time() - tmp_start)

    # output summary in root process
    if comm_rank == 0:
        dumping_time_start = time.time()
        dump_hash_tag_output(reduced_hash_tag_count)
        dump_country_code_output(reduced_language_code_count, language_code_dict)

        end = time.time()
        dump_time(comm_rank, "dumping output", end - dumping_time_start)
        program_run_time = end - program_start
        print("Programs runs {}(s)".format(program_run_time))


if __name__ == "__main__":
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='python to process data')
    # Required country code file
    parser.add_argument('-country', type=str, help='A required string path to country code file')
    # Required geo data path
    parser.add_argument('-data', type=str, help='A required string path to data file')
    args = parser.parse_args()

    country = args.country
    data = args.data

    main(country, data)

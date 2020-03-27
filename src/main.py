"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-3-10 15:28:34
Description: main function
"""
import heapq
import operator
from mpi4py import MPI
from collections import Counter
import argparse
import numpy as np
from LanguageSummary import LanguageSummary
from TwitterData import TwitterData
from util import read_language_code, read_data_line_by_line, preprocess_data, dump_country_code_output, dump_hash_tag_output, dump_time, processing_data, \
    read_n_lines, read_language_code_dict, processing_data2, dump_country_code_output2, merge_list, chunks, dump_hash_tag_output3, dump_country_code_output3, \
    merge_dict
import time


def main(country_code_file_path, twitter_data_path):
    """
    :param country_code_file_path: the path of country_code_file
    :param twitter_data_path: the path of twitter_data
    """
    # initialize communicator
    comm = MPI.COMM_WORLD
    comm_rank = comm.Get_rank()
    comm_size = comm.Get_size()

    # the starting timestamp
    start = time.time()

    # read country_code info
    # language_summary_dict = read_language_code(country_code_file_path)
    language_code_dict = comm.bcast(read_language_code_dict(country_code_file_path), root=0)
    # TODO should language info in each process?
    dump_time(comm_rank, "reading country code file", time.time() - start)

    # counting hash_tag
    hash_tag_count = Counter()
    language_code_count = {}

    # only one processor, no need to split data
    if comm_size == 1:
        for line in read_data_line_by_line(twitter_data_path):
            preprocessed_line = preprocess_data(line)
            # the line is data
            # line_count += 1
            if preprocessed_line:
                twitter_data = TwitterData(preprocessed_line)

                hash_tag_count += twitter_data.hash_tags

                if twitter_data.language_code in language_code_count:
                    language_code_count[twitter_data.language_code] += 1
                else:
                    language_code_count[twitter_data.language_code] = 1

        n = 10
        reduced_hash_tag_count = hash_tag_count.most_common(n)
        reduced_language_code_count = Counter(language_code_count).most_common(n)

    # multi processor
    else:
        n_lines = comm.bcast(read_n_lines(twitter_data_path), root=0)
        # to test smallTwitter.json, uncomment the following line
        # n_lines = 5000
        # TODO is my line splits correct?
        lines_per_core = n_lines // comm_size
        lines_to_end = n_lines+1  # ignore first line
        line_to_start = 1 + lines_per_core * comm_rank  # ignore first line
        line_to_end = line_to_start + lines_per_core
        if comm_rank == comm_size-1:  # last core to finish all remaining lines
            line_to_end = lines_to_end

        for line_number, line in enumerate(read_data_line_by_line(twitter_data_path)):  # ignore first line
            if line_number == line_to_end:
                break
            if line_number >= line_to_start:
                preprocessed_line = preprocess_data(line)
                if preprocessed_line:
                    processing_data2(preprocessed_line, hash_tag_count, language_code_count)
                else:
                    print(line_number)

        # reduce LanguageSummary, hash_tag_count from slave processors to master processor
        # reduced_language_summary_dict = comm.reduce(language_summary_dict, root=0, op=LanguageSummary.merge_language_list)
        reduced_language_code_count = comm.reduce(language_code_count, root=0, op=merge_dict)
        reduced_hash_tag_count = comm.reduce(hash_tag_count, root=0, op=operator.add)

        if comm_rank == 0:
            # split_language_code_np_array = np.array_split(list(reduced_language_code_count.items()), comm_size)
            split_language_code_np_array = np.array_split(list(reduced_language_code_count.items()), comm_size)
            split_hash_tag_np_array = np.array_split(list(reduced_hash_tag_count.items()), comm_size)
        else:
            split_language_code_np_array = None
            split_hash_tag_np_array = None

        local_language_code = list(map(lambda x: (x[0], int(x[1])), comm.scatter(split_language_code_np_array, root=0)))
        local_hash_tag = list(map(lambda x: (x[0], int(x[1])), comm.scatter(split_hash_tag_np_array, root=0)))

        # print(comm_rank, local_language_code, local_hash_tag)

        n = 10
        reduced_language_code_count = comm.reduce(heapq.nlargest(n, local_language_code, lambda x: x[1]), root=0, op=merge_list)
        reduced_hash_tag_count = comm.reduce(heapq.nlargest(n, local_hash_tag, lambda x: x[1]), root=0, op=merge_list)

    # output summary in root process
    if comm_rank == 0:
        dumping_time_start = time.time()
        dump_hash_tag_output3(reduced_hash_tag_count)
        dump_country_code_output3(reduced_language_code_count, language_code_dict)

        end = time.time()
        dump_time(comm_rank, "dumping output", end - dumping_time_start)
        program_run_time = end - start
        print("Programs runs {}(s)".format(program_run_time))


def single_node_single_core_task(twitter_data_path, hash_tag_count, language_code_count, comm_rank):
    """
    :param twitter_data_path: the path of twitter_data
    :param hash_tag_count: Counter({hash_tag: int}) object
    :param language_code_count: {country_cde: int} object
    :param comm_rank: the rank of the current processor
    """
    # line_count = 0
    for line in read_data_line_by_line(twitter_data_path):
        preprocessed_line = preprocess_data(line)
        # the line is data
        # line_count += 1
        if preprocessed_line:
            processing_data2(preprocessed_line, hash_tag_count, language_code_count)

    # print("processor #{} processes {} lines.".format(comm_rank, line_count))


def multi_core_master_processor_task(twitter_data_path, comm_size, comm, comm_rank):
    """
    :param twitter_data_path: the path of twitter_data
    :param comm_size: number of working processors
    :param comm: communicator object
    :param comm_rank: the rank of the current processor
    """
    next_target = 1
    line_count = 0

    time_start = time.time()

    for line in read_data_line_by_line(twitter_data_path):
        preprocessed_line = preprocess_data(line)
        # the line is data
        line_count += 1
        if preprocessed_line:
            comm.send(preprocessed_line, next_target)
            # scatter data line by line to slave process
            next_target += 1
            if next_target == comm_size:
                next_target = 1

    # send None to slave processors to stop receiving
    for i in range(1, comm_size):
        comm.send(None, i)
    dump_time(comm_rank, "reading file", time.time() - time_start)
    print("processor #{} processes {} lines.".format(comm_rank, line_count))


def multi_core_slave_processor_task(comm, hash_tag_count, language_summary_dict, comm_rank):
    """
    :param comm: communicator object
    :param hash_tag_count: Counter({hash_tag: int}) object
    :param language_summary_dict: {country_cde: LanguageSummary} object
    :param comm_rank: the rank of the current processor
    """
    processing_time_start = time.time()
    recv_count = 0

    while True:
        local_preprocessed_line = comm.recv(source=0)
        # master processor has sent all data
        if not local_preprocessed_line:
            break
        recv_count += 1
        processing_data(local_preprocessed_line, hash_tag_count, language_summary_dict)

    dump_time(comm_rank, "processing", time.time() - processing_time_start)
    print("processor #{} recv {} lines.".format(comm_rank, recv_count))


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

"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-3-10 15:28:34
Description: 
"""
import operator
from datetime import datetime
from mpi4py import MPI
from collections import Counter
import argparse
from TwitterData import TwitterData
from LanguageSummary import LanguageSummary
from util import read_language_code, read_data_line_by_line, preprocess_data, dump_country_code_output, dump_hash_tag_output


def main(country_code_file_path, twitter_data_path):
    """
    :param country_code_file_path:
    :param twitter_data_path:
    """
    # initialize communicator
    comm = MPI.COMM_WORLD
    comm_rank = comm.Get_rank()
    comm_size = comm.Get_size()

    start = datetime.now()
    language_summary_dict = read_language_code(country_code_file_path)
    # TODO should language info in each process?
    # read_grid_info_end = datetime.now()
    # print("process #{} takes {} to read grid info.".format(comm_rank, read_grid_info_end - start))

    hash_tag_count = Counter()

    # only one process, no need to split data
    if comm_size == 1:
        line_count = 0
        for line in read_data_line_by_line(twitter_data_path):
            preprocessed_line = preprocess_data(line)
            # the line is data
            line_count += 1
            if preprocessed_line:
                twitter_data = TwitterData(preprocessed_line)

                for hash_tag in twitter_data.hash_tags:
                    hash_tag_count[hash_tag] += 1

                try:
                    language_summary_dict[twitter_data.language_code].summarize(twitter_data)
                except KeyError:
                    language_summary_dict[twitter_data.language_code] = LanguageSummary(twitter_data.language_code, "unknown")
                    language_summary_dict[twitter_data.language_code].summarize(twitter_data)

        print("processor #{} processes {} lines.".format(comm_rank, line_count))

    else:
        if comm_rank == 0:
            next_target = 1
            line_count = 0

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

            for i in range(1, comm_size):
                comm.send(None, i)
            print("processor #{} processes {} lines.".format(comm_rank, line_count))

        else:
            recv_count = 0

            while True:
                local_preprocessed_line = comm.recv(source=0)
                if not local_preprocessed_line:
                    break

                recv_count += 1
                twitter_data = TwitterData(local_preprocessed_line)

                for hash_tag in twitter_data.hash_tags:
                    hash_tag_count[hash_tag] += 1

                try:
                    language_summary_dict[twitter_data.language_code].summarize(twitter_data)
                except KeyError:
                    language_summary_dict[twitter_data.language_code] = LanguageSummary(twitter_data.language_code, "unknown")
                    language_summary_dict[twitter_data.language_code].summarize(twitter_data)
                    # print("unknown language_code:", twitter_data.language_code)

            print("processor #{} recv {} lines.".format(comm_rank, recv_count))

    reduced_language_summary_dict = comm.reduce(language_summary_dict, root=0, op=LanguageSummary.merge_language_list)
    reduced_hash_tag_count = comm.reduce(hash_tag_count, root=0, op=operator.add)

    # output summary in root process
    if comm_rank == 0:
        dump_hash_tag_output(reduced_hash_tag_count)
        print()
        dump_country_code_output(reduced_language_summary_dict.values())

        end = datetime.now()
        print("Programs runs", end - start)


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

"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-3-21 01:34:58
Description: analysis the execution performance and draw diagrams
"""
import re
import matplotlib.pyplot as plt

OUTPUT_DIR = "../../docs/"
DATA_DIR = "../../slurm/"
DATA_FILE_TYPE = ".txt"
IMAGE_TYPE = ".png"


def read_physical_txt(file_path: str):
    run_time = None
    read_country_code_file_time = {}  # {#processor: time}
    process_time = {}
    calculate_top_n_time = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            tmp = re.match("^Programs runs [0-9.]+", line)
            if tmp:
                run_time = [float(i) for i in re.findall("[0-9.]+", line)][0]
                continue

            tmp = re.match("^===== processor #[0-9] does reading country code file for [0-9.]+", line)
            if tmp:
                processor_rank, time = [i for i in re.findall("[0-9.]+", line)]
                read_country_code_file_time[int(processor_rank)] = float(time)
                continue

            tmp = re.match("^===== processor #[0-9] does processing data for [0-9.]+", line)
            if tmp:
                processor_rank, time = [i for i in re.findall("[0-9.]+", line)]
                process_time[int(processor_rank)] = float(time)
                continue
            tmp = re.match("^===== processor #[0-9] does calculating top n for [0-9.]+", line)
            if tmp:
                processor_rank, time = [i for i in re.findall("[0-9.]+", line)]
                calculate_top_n_time[int(processor_rank)] = float(time)
                continue

    return run_time, read_country_code_file_time, process_time, calculate_top_n_time


def draw_bar_chart(file_name: str):
    x = []
    y = []
    one_node_1_core_file_path = DATA_DIR + "1node1core-physical" + DATA_FILE_TYPE
    run_time, read_country_code_file_time, process_time, calculate_top_n_time = read_physical_txt(one_node_1_core_file_path)
    x.append("1 node 1 core")
    y.append(run_time)

    one_node_8_core_file_path = DATA_DIR + "1node8core-physical" + DATA_FILE_TYPE
    run_time, read_country_code_file_time, process_time, calculate_top_n_time = read_physical_txt(one_node_8_core_file_path)
    x.append("1 node 8 core")
    y.append(run_time)

    two_node_8_core_file_path = DATA_DIR + "2node8core-physical" + DATA_FILE_TYPE
    run_time, read_country_code_file_time, process_time, calculate_top_n_time = read_physical_txt(two_node_8_core_file_path)
    x.append("2 node 8 core")
    y.append(run_time)

    plt.grid(True, axis='y')
    plt.bar(range(len(x)), y, tick_label=x)
    plt.title(file_name)
    plt.xlabel("Resources")
    plt.ylabel("second (s)")
    for i, v in enumerate(y):
        plt.text(i-0.1, v + 5, round(y[i], 2), fontsize=9, color='b')
    plt.savefig(OUTPUT_DIR + file_name + IMAGE_TYPE)
    plt.show()


if __name__ == "__main__":
    draw_bar_chart("Performance Comparision")

    pass

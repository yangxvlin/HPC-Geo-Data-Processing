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


def read_txt(file_path: str):
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
    run_time, read_country_code_file_time, process_time, calculate_top_n_time = read_txt(one_node_1_core_file_path)
    x.append("1 node 1 core")
    y.append(run_time)

    one_node_8_core_file_path = DATA_DIR + "1node8core-physical" + DATA_FILE_TYPE
    run_time, read_country_code_file_time, process_time, calculate_top_n_time = read_txt(one_node_8_core_file_path)
    x.append("1 node 8 core")
    y.append(run_time)

    two_node_8_core_file_path = DATA_DIR + "2node8core-physical" + DATA_FILE_TYPE
    run_time, read_country_code_file_time, process_time, calculate_top_n_time = read_txt(two_node_8_core_file_path)
    x.append("2 node 8 core")
    y.append(run_time)

    plt.grid(True, axis='y', alpha=0.5)
    plt.bar(range(len(x)), y, tick_label=x)
    plt.title(file_name)
    plt.xlabel("Resources")
    plt.ylabel("second (s)")
    for i, v in enumerate(y):
        plt.text(i-0.1, v + 5, round(y[i], 2), fontsize=9, color='b')
    plt.savefig(OUTPUT_DIR + file_name + IMAGE_TYPE)
    plt.show()


def draw_bar_chart2(file_name: str):
    name_list = []
    y1 = []
    y2 = []
    one_node_8_core_file_path = DATA_DIR + "1node8core-physical" + DATA_FILE_TYPE
    run_time, read_country_code_file_time, process_time, calculate_top_n_time = read_txt(one_node_8_core_file_path)
    name_list.append("1 node 8 core")
    y1.append(run_time)

    two_node_8_core_file_path = DATA_DIR + "2node8core-physical" + DATA_FILE_TYPE
    run_time, read_country_code_file_time, process_time, calculate_top_n_time = read_txt(two_node_8_core_file_path)
    name_list.append("2 node 8 core")
    y1.append(run_time)

    one_node_8_core_file_path = DATA_DIR + "1node8core-cloud" + DATA_FILE_TYPE
    run_time, read_country_code_file_time, process_time, calculate_top_n_time = read_txt(one_node_8_core_file_path)
    y2.append(run_time)

    two_node_8_core_file_path = DATA_DIR + "2node8core-cloud" + DATA_FILE_TYPE
    run_time, read_country_code_file_time, process_time, calculate_top_n_time = read_txt(two_node_8_core_file_path)
    y2.append(run_time)

    total_width, n = 0.5, 2
    width = total_width / n

    x = list(range(1, len(name_list)+1))

    plt.grid(True, axis='y', alpha=0.5)
    print(x, y1, y2)
    plt.bar(x, y1, width=width, label='physical', fc='b', align="edge")
    for i in range(len(x)):
        x[i] = x[i] + width
    print(x, y1, y2)
    plt.bar(x, y2, width=width, label='cloud', tick_label=name_list, align="edge", fc='r')
    plt.legend()
    plt.title(file_name)
    plt.xlabel("Resources")
    plt.ylabel("second (s)")
    for i, v in enumerate(y1):
        plt.text(i+1.12 - 0.05, v + 5, round(y1[i], 2), fontsize=9, color='b')
    for i, v in enumerate(y2):
        plt.text(i+1.12 + width - 0.05, v + 5, round(y2[i], 2), fontsize=9, color='r')
    plt.savefig(OUTPUT_DIR + file_name + IMAGE_TYPE)
    plt.show()


def draw_line_diagram(file_name: str):
    x1 = []
    x2 = []
    x3 = []
    x4 = []
    y1 = []
    y2 = []
    y3 = []
    y4 = []

    data_dir = DATA_DIR + "n_cores/"
    for i in range(1, 24+1):
        n_cores = i
        data_file_name = data_dir+"1node"+str(n_cores)+"core-physical"+DATA_FILE_TYPE
        run_time, read_country_code_file_time, process_time, calculate_top_n_time = read_txt(data_file_name)
        x1.append(i)
        y1.append(run_time)

    for i in range(1, 12+1):
        n_cores = i
        data_file_name = data_dir+"1node"+str(n_cores)+"core-cloud"+DATA_FILE_TYPE
        run_time, read_country_code_file_time, process_time, calculate_top_n_time = read_txt(data_file_name)
        x2.append(i)
        y2.append(run_time)

    for i in range(1, 12+1):
        n_cores = i
        data_file_name = data_dir+"2node"+str(n_cores)+"core-physical"+DATA_FILE_TYPE
        run_time, read_country_code_file_time, process_time, calculate_top_n_time = read_txt(data_file_name)
        x3.append(i*2)
        y3.append(run_time)

    for i in range(1, 12+1):
        n_cores = i
        data_file_name = data_dir+"2node"+str(n_cores)+"core-cloud"+DATA_FILE_TYPE
        run_time, read_country_code_file_time, process_time, calculate_top_n_time = read_txt(data_file_name)
        x4.append(i*2)
        y4.append(run_time)

    plt.plot(x1, y1, 'r*-', x2, y2, 'b*-', x3, y3, '+-', x4, y4, '+-')
    plt.title(file_name)
    plt.xlabel("Number of cores")
    plt.ylabel("Second (s)")
    plt.legend(["1node-physics", "1node-cloud", "2node-physics", "2node-cloud"])
    plt.show()

    y1_0 = y1[0]
    y1 = [1] + list(map(lambda x: x / y1_0, y1[1:]))
    y2_0 = y2[0]
    y2 = [1] + list(map(lambda x: x / y2_0, y2[1:]))
    y3_0 = y3[0]
    y3 = [1] + list(map(lambda x: x / y3_0, y3[1:]))
    y4_0 = y4[0]
    y4 = [1] + list(map(lambda x: x / y4_0, y4[1:]))

    plt.plot(x1, y1, 'r*-', x2, y2, 'b*-', x3, y3, '+-', x4, y4, '+-')
    plt.title("Parallel optimization rate")
    plt.xlabel("Number of cores")
    plt.ylabel("Second (s) / base execution time")
    plt.legend(["1node-physics", "1node-cloud", "2node-physics", "2node-cloud"])
    plt.show()


if __name__ == "__main__":
    # draw_bar_chart("Performance Comparision")
    # draw_bar_chart2("1 node v.s. 2 node")
    draw_line_diagram("Performance")
    pass

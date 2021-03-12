#!/usr/bin/env python3
import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt

def parse_json(file_path):
    with open(file_path, 'r') as f:
        j = json.load(f)
    return j

def plot_ssll(j):
    ll = np.array(j['warpalyzer_ll']['signal_data'])
    ss = np.array(j['warpalyzer_ss']['signal_data'])
    ll_limits = [j['warpalyzer_ll']['test_limit_2_percentile'], j['warpalyzer_ll']['test_limit_10_percentile']]
    ss_limits = [j['warpalyzer_ss']['test_limit_2_percentile'], j['warpalyzer_ss']['test_limit_10_percentile']]

    fig, (ax_ll, ax_ss) = plt.subplots(1, 2)
    ax_ll.scatter([d['x_pos'] for d in ll], [d['signal'] for d in ll])
    ax_ll.set_title('LL signal_'+j['serial_number'])
    x_lim = ax_ll.get_xlim()
    ax_ll.hlines(ll_limits[0], x_lim[0], x_lim[1], ['r'], 'dashed', '2-perc limit')
    ax_ll.hlines(ll_limits[1], x_lim[0], x_lim[1], ['orange'], 'dashed', '10-perc limit')
    ax_ll.legend()

    ax_ss.scatter([d['y_pos'] for d in ss], [d['signal'] for d in ss])
    ax_ss.set_title('SS signal_'+j['serial_number'])
    x_lim = ax_ss.get_xlim()
    ax_ss.hlines(ss_limits[0], x_lim[0], x_lim[1], ['r'], 'dashed', '2-perc limit')
    ax_ss.hlines(ss_limits[1], x_lim[0], x_lim[1], ['orange'], 'dashed', '10-perc limit')
    ax_ss.legend()
    fig.show()

def plot_neighbour(j):
    em = np.array(j['neighbour_test']['emitters']) 
    det = np.array(j['neighbour_test']['detectors']) 
    limit = j['neighbour_test']['test_limit']

    fig, ax = plt.subplots()
    ax.set_title('Component meirt_'+j['serial_number'])
    ax.scatter([d['idx'] for d in em], [d['merit'] for d in em], c='b', label='emitter')
    ax.scatter([d['idx'] for d in det], [d['merit'] for d in det], c='m', marker='s', label='detector')
    x_lim = ax.get_xlim()
    ax.hlines(limit, x_lim[0], x_lim[1], 'r', 'dashed')
    ax.legend()
    fig.show()
    
def main():

    if len(sys.argv) < 2:
        print("No json log file supplided\n")
        return
    else:
        cwd = os.path.abspath(sys.argv[1]) 
        files = os.listdir(cwd)
        for file in files:
            if file.endswith(".json"):
                j = parse_json(file)
                plot_ssll(j)
                plot_neighbour(j)    
        plt.show()
if __name__ == "__main__":
    main()

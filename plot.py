import matplotlib.pyplot as plt
import numpy as np
from config import *


class Plot_packet:
    def __init__(self,
                 ground_truth: list,
                 sensor_input: list,
                 type: FilterType,
                 estimation1: list,
                 estimation2: list):
        self.ground_truth = ground_truth
        self.sensor_input = sensor_input
        if type == FilterType.Kalman:
            self.estimation1 = estimation1
        elif type == FilterType.Particle:
            self.estimation1 = estimation1
        elif type == FilterType.Both:
            self.estimation1 = estimation1
            self.estimation2 = estimation2


def plot_error(plot_data: list[Plot_packet], type: FilterType) -> None:
    """
    Plot error with one method(Kalman/Particle)
    :param plot_data: data used to plot
    :param type: kalman or particle
    """
    plt.figure('Error')
    x = range(len(plot_data))
    sensor_error: list = [
        np.linalg.norm(pac.sensor_input - pac.ground_truth)
        for pac in plot_data
    ]
    estimation_error: list = []
    estimation_error1: list = []
    if type == FilterType.Kalman:
        estimation_error = [
            np.linalg.norm(pac.estimation1 - pac.ground_truth)
            for pac in plot_data
        ]
    elif type == FilterType.Particle:
        estimation_error = [
            np.linalg.norm(pac.estimation1 - pac.ground_truth)
            for pac in plot_data
        ]
    elif type == FilterType.Both:
        estimation_error = [
            np.linalg.norm(pac.estimation1 - pac.ground_truth)
            for pac in plot_data
        ]
        estimation_error1 = [
            np.linalg.norm(pac.estimation2 - pac.ground_truth)
            for pac in plot_data
        ]
    ratio = np.array(estimation_error)/np.array(sensor_error)



    print("The map shows a pre-determined path in black,")
    print("\t estimate produced by filter in blue,")
    print("\t and actual pose in red.")
    print()
    print("The plot shows sensor error in blue,")
    print("\t and estimate error in red.")

    print("(Estimate Error/Sensor Error) Mean: ", np.mean(ratio))
    print("(Estimate Error/Sensor Error) Variance: ", np.var(ratio))
    print("Press Enter to continue")
    plt.plot(x, estimation_error, 'r')
    plt.plot(x, sensor_error, 'b')
    plt.xlabel("iteration time")
    plt.ylabel("Estimation Error")
    if type == FilterType.Both:
        plt.plot(x, estimation_error1, 'g')

    plt.show(block=False)
    
    aa = input()
    plt.close()
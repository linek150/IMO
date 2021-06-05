import pickle
import matplotlib.pyplot as plt
from scipy import stats


def generate_plot(file_path):
    with (open(file_path, "rb")) as file:
        solution = pickle.load(file)

        r, _ = stats.pearsonr(solution[0], solution[1])
        plt.plot(solution[0], solution[1])
        plt.title(f'mean vertex similarity\nr = {r}')
        plt.xlabel('goal function')
        plt.ylabel('similarity')
        plt.show()
        r, _ = stats.pearsonr(solution[0], solution[2])
        plt.plot(solution[0], solution[2])
        plt.title(f'mean edge similarity\nr = {r}')
        plt.xlabel('goal function')
        plt.ylabel('similarity')
        plt.show()
        r, _ = stats.pearsonr(solution[0], solution[3])
        plt.plot(solution[0], solution[3])
        plt.title(f'vertex similarity to best\nr = {r}')
        plt.xlabel('goal function')
        plt.ylabel('similarity')
        plt.show()
        r, _ = stats.pearsonr(solution[0], solution[4])
        plt.plot(solution[0], solution[4])
        plt.title(f'edge similarity to best\nr = {r}')
        plt.xlabel('goal function')
        plt.ylabel('similarity')
        plt.show()


generate_plot('kroA200.pkl')
generate_plot('kroB200.pkl')

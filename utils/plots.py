import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def convergence_curve(curves, labels, path):
    plt.figure(figsize=(10, 6))
    for curve, label in zip(curves, labels):
        plt.plot(curve, label=label)
    plt.xlabel("Iteration")
    plt.ylabel("Best value found")
    plt.title("Comparative Convergence Curve")
    plt.legend()
    plt.grid(True)
    plt.savefig(path)
    plt.close()


def search_history(population_history, path):
    plt.figure(figsize=(8, 6))
    for pop in population_history:
        plt.scatter(pop[:, 0], pop[:, 1], alpha=0.5)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Search History")
    plt.savefig(path)
    plt.close()


def exploration_exploitation_balance(exploration, exploitation, path):
    plt.figure(figsize=(8, 6))
    plt.plot(exploration, label="Exploration")
    plt.plot(exploitation, label="Exploitation")
    plt.xlabel("Iteration")
    plt.ylabel("Balance")
    plt.title("Exploration vs Exploitation Balance")
    plt.legend()
    plt.grid(True)
    plt.savefig(path)
    plt.close()


def comparative_boxplot(results, labels, path):
    plt.figure(figsize=(8, 6))
    # Matplotlib's boxplot expects 'labels' for tick labels
    plt.boxplot(results, labels=labels)
    plt.title("Comparative Boxplot")
    plt.ylabel("Value")
    plt.savefig(path)
    plt.close()


def sensitivity_heatmap(matrix, xlabels, ylabels, path):
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        matrix, xticklabels=xlabels, yticklabels=ylabels, annot=True, cmap="viridis"
    )
    plt.title("Sensitivity Analysis Heatmap")
    plt.savefig(path)
    plt.close()


if __name__ == "__main__":
    curves = [np.random.rand(100), np.random.rand(100), np.random.rand(100)]
    labels = ["Alg1", "Alg2", "Alg3"]
    convergence_curve(curves, labels, "convergence_example.png")

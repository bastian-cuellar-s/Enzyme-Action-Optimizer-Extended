import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def curva_convergencia(curvas, labels, path):
    plt.figure(figsize=(10,6))
    for curva, label in zip(curvas, labels):
        plt.plot(curva, label=label)
    plt.xlabel('Iteración')
    plt.ylabel('Mejor valor encontrado')
    plt.title('Curva de Convergencia Comparativa')
    plt.legend()
    plt.grid(True)
    plt.savefig(path)
    plt.close()

def historial_busqueda(population_history, path):
    plt.figure(figsize=(8,6))
    for pop in population_history:
        plt.scatter(pop[:,0], pop[:,1], alpha=0.5)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Historial de Búsqueda')
    plt.savefig(path)
    plt.close()

def balance_exploracion_explotacion(exploration, exploitation, path):
    plt.figure(figsize=(8,6))
    plt.plot(exploration, label='Exploración')
    plt.plot(exploitation, label='Explotación')
    plt.xlabel('Iteración')
    plt.ylabel('Balance')
    plt.title('Balance Exploración vs. Explotación')
    plt.legend()
    plt.grid(True)
    plt.savefig(path)
    plt.close()

def boxplot_comparativo(resultados, labels, path):
    plt.figure(figsize=(8,6))
    plt.boxplot(resultados, labels=labels)
    plt.title('Diagrama de Cajas (Box Plot)')
    plt.ylabel('Valor')
    plt.savefig(path)
    plt.close()

def heatmap_sensibilidad(matriz, xlabels, ylabels, path):
    plt.figure(figsize=(8,6))
    sns.heatmap(matriz, xticklabels=xlabels, yticklabels=ylabels, annot=True, cmap='viridis')
    plt.title('Mapa de Calor (Heatmap) - Análisis de Sensibilidad')
    plt.savefig(path)
    plt.close()

if __name__ == "__main__":
    # Ejemplo de uso
    curvas = [np.random.rand(100), np.random.rand(100), np.random.rand(100)]
    labels = ['Algoritmo 1', 'Algoritmo 2', 'Algoritmo 3']
    curva_convergencia(curvas, labels, 'curva_convergencia.png')
    population_history = [np.random.rand(30,2) for _ in range(10)]
    historial_busqueda(population_history, 'historial_busqueda.png')
    balance_exploracion_explotacion(np.random.rand(100), np.random.rand(100), 'balance_exploracion_explotacion.png')
    boxplot_comparativo([np.random.rand(30), np.random.rand(30), np.random.rand(30)], labels, 'boxplot_comparativo.png')
    matriz = np.random.rand(5,5)
    heatmap_sensibilidad(matriz, [f'P{i}' for i in range(5)], [f'Q{j}' for j in range(5)], 'heatmap_sensibilidad.png')

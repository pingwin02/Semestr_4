import numpy as np
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA

if __name__ == '__main__':

    # Wybrane trzy punkty w przestrzeni 3D
    points_3d = np.array([[1, 8, 8], [5, 9, 7], [3, 6, 9]])
    points_3d_stand = (points_3d - np.mean(points_3d, axis=0)) / np.std(points_3d, axis=0)

    print('Współrzędne punktów 3D:')
    print(points_3d)

    print("Średnia i odchylenie stand.:")
    print(np.mean(points_3d, axis=0))
    print(np.std(points_3d, axis=0))
    print("Standaryzacja punktów 3D:")
    print(points_3d_stand)

    print("Macierz kowariancji:")
    cov = (1 / 3) * np.dot(points_3d_stand.T, points_3d_stand)
    print(cov)

    print("Wartości własne:")
    print(np.linalg.eig(cov)[0])

    print("Wektory własne:")
    print(np.linalg.eig(cov)[1])

    print("Współrzędne punktów po przekształceniu (manualnym):")
    points_2d_manual = np.dot(points_3d_stand, np.linalg.eig(cov)[1][:, :2])
    print(points_2d_manual)

    # Redukcja wymiarów za pomocą PCA
    pca = PCA(n_components=2)
    points_2d = pca.fit_transform(points_3d_stand)

    print('Współrzędne punktów 2D (po PCA):')
    print(points_2d)

    colors = ['red', 'green', 'blue']

    fig = plt.figure()
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.scatter3D(points_3d[:, 0], points_3d[:, 1], points_3d[:, 2], c=colors)
    ax1.view_init(azim=150, elev=40)
    ax1.set_title('Punkty 3D')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')

    for i, (x, y, z) in enumerate(points_3d):
        ax1.text(x, y, z, f'({x}, {y}, {z})', color=colors[i], ha='center', va='bottom')

    ax2 = fig.add_subplot(122)
    ax2.scatter(points_2d[:, 0], points_2d[:, 1], c=colors)
    ax2.scatter(points_2d_manual[:, 0], points_2d_manual[:, 1], c=colors, marker='x')
    ax2.set_title('Punkty 2D (po PCA)')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')

    for i, (x, y) in enumerate(points_2d):
        ax2.text(x, y, f'({x:.2f}, {y:.2f})', color=colors[i], ha='center', va='bottom')

    for i, (x, y) in enumerate(points_2d_manual):
        ax2.text(x, y, f'({x:.2f}, {y:.2f})', color=colors[i], ha='center', va='top')

    plt.legend(['PCA', 'Manual'])
    plt.tight_layout()
    plt.savefig('pca.png')
    plt.show()

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

L1 = 0.325
L2 = 0.275
d1 = 0.4
d4 = 0.1

tabla_dh = [
    [0,       0,  0, d1, 0],
    [0,       L1, 0, 0,  0],
    [np.pi,   L2, 0, 0,  1],
    [0,       0,  0, d4, 0],
]


def matriz_dh(alpha, a, theta, d):
    ca, sa = np.cos(alpha), np.sin(alpha)
    ct, st = np.cos(theta), np.sin(theta)
    return np.array([
        [ct,     -st,     0,   a],
        [st*ca,  ct*ca,  -sa, -sa*d],
        [st*sa,  ct*sa,   ca,  ca*d],
        [0,       0,       0,   1],
    ])


def cinematica_directa(tabla_dh, q):
    T = np.eye(4)
    posiciones = [T[:3, 3].copy()]
    transforms = [T.copy()]
    for (alpha, a, theta_fijo, d_fijo, sigma), qi in zip(tabla_dh, q):
        theta = qi if sigma == 0 else theta_fijo
        d = qi if sigma == 1 else d_fijo
        T = T @ matriz_dh(alpha, a, theta, d)
        posiciones.append(T[:3, 3].copy())
        transforms.append(T.copy())
    return np.array(posiciones), transforms, T


def pedir_q():
    q = []
    for i, fila in enumerate(tabla_dh, start=1):
        sigma = fila[4]
        if sigma == 0:
            grados = float(input(f'theta_{i} en grados: '))
            q.append(np.radians(grados))
        else:
            q.append(float(input(f'd_{i} en metros: ')))
    return q


def plot_frame(ax, T, nombre, size=0.08):
    origen = T[:3, 3]
    R = T[:3, :3]
    colores = ['r', 'g', 'b']
    ejes = ['x', 'y', 'z']
    for i in range(3):
        direccion = R[:, i] * size
        ax.quiver(*origen, *direccion, color=colores[i], arrow_length_ratio=0.2)
        punta = origen + direccion
        ax.text(*punta, ejes[i], color=colores[i])
    ax.text(*origen, f' {nombre}', color='black')


def graficar(posiciones, transforms, q):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(posiciones[:, 0], posiciones[:, 1], posiciones[:, 2],
            '-o', color='black', linewidth=2, markersize=5)

    for i, T in enumerate(transforms):
        plot_frame(ax, T, nombre=str(i))

    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    ax.set_zlabel('Eje Z')
    ax.set_title(f'SCARA - q = {np.round(q, 3)}')

    rango = max(np.ptp(posiciones, axis=0).max() / 2, 0.15)
    centro = posiciones.mean(axis=0)
    ax.set_xlim(centro[0]-rango, centro[0]+rango)
    ax.set_ylim(centro[1]-rango, centro[1]+rango)
    ax.set_zlim(0, centro[2]+2*rango)
    ax.set_box_aspect([1, 1, 1])

    plt.show()


if __name__ == '__main__':
    while True:
        q = pedir_q()
        posiciones, transforms, T_final = cinematica_directa(tabla_dh, q)
        np.set_printoptions(precision=4, suppress=True)
        print('Posicion del efector final:', posiciones[-1])
        print('T0_n:')
        print(T_final)
        graficar(posiciones, transforms, q)
        if input('Otra postura? (s/n): ').strip().lower() != 's':
            break

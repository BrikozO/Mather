import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection


def cube(a):

    img = BytesIO()
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    #Постороение куба через матрицу булевых элементов
    dots = [a,a,a]
    data = np.ones(dots, dtype=np.bool)
    indent = 0.9
    string = np.empty(dots + [4], dtype=np.float32)
    string[:] = [0, 0, 1, indent]

    #Задание параметров построения
    ax.voxels(data, facecolors=string, )

    plt.savefig(img, format='png')
    plt.close()
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url


def ball(a):

    img = BytesIO()
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    #Постороение шара через тригонометрические функции(строит полигонами)
    u = np.linspace(0, 2 * np.pi, 100) 
    v = np.linspace(0, np.pi, 100)
    x = a * np.outer(np.cos(u), np.sin(v))
    y = a * np.outer(np.sin(u), np.sin(v))
    z = a * np.outer(np.ones(np.size(u)), np.cos(v))

    #Задание параметров построения
    ax.plot_surface(x, y, z, rstride=5, cstride=5, color='b')

    plt.savefig(img, format='png')
    plt.close()
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url


def pyramid(a, b):

    img = BytesIO()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #Построение пирамиды с помощью создания матрицы
    v = np.array([[-1*(a/2), -1*(a/2), -1*(a/2)],
                  [1*(a/2), -1*(a/2), -1*(a/2)],
                  [1*(a/2), 1*(a/2), -1*(a/2)],
                  [-1*(a/2), 1*(a/2), -1*(a/2)],
                  [0, 0, 1 * b]])
    ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])
    #Расставление ранее заданых в матрице точек на трехмерной плоскости
    verts = [[v[0], v[1], v[4]], [v[0], v[3], v[4]],
             [v[2], v[1], v[4]], [v[2], v[3], v[4]], [v[0], v[1], v[2], v[3]]]

    #задание параметров построения
    ax.add_collection3d(Poly3DCollection(verts, facecolors='b', linewidths=1, edgecolors='r'))

    plt.savefig(img, format='png')
    plt.close()
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url


def cylinder(a, b):

    img = BytesIO()
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    #Постороение цилиндра через тригонометрические функции(строит полигонами)
    u = np.linspace (0,2 * np.pi, 100)
    h = np.linspace (0,a,20)
    x = b * np.outer (np.sin (u), np.ones (len (h)))
    y = b * np.outer (np.cos (u), np.ones (len (h)))
    z = np.outer (np.ones (len (u)), h)

    #Задание параметров построения
    ax.plot_surface(x, y, z, color='b')
    plt.savefig(img, format='png')
    plt.close()
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url

import matplotlib.pyplot as plt
import pandas as pd


def import_and_convert_csv(csv_file):
    df = pd.read_csv(csv_file)
    x, y, z, w = df.items()

    xs = []
    ys = []
    zs = []
    ws = []

    for i in range(len(df)):
        xs.append(x[1][i])
        ys.append(y[1][i])
        zs.append(z[1][i])
        ws.append(w[1][i])

    return xs, ys, zs, ws


def main():
    columns_array = ["R", "G", "B", "W"]

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    ax.set_xlim([0, 100])
    ax.set_ylim([0, 100])
    ax.set_zlim([0, 100])

    file_names = [
        "log_rgb_blue.txt",
        "log_rgb_brown.txt",
        "log_rgb_green.txt",
        "log_rgb_red.txt",
    ]
    color_names = ["blue", "brown", "green", "red"]

    for i in range(len(color_names)):
        x_points, y_points, z_points, w_points = import_and_convert_csv(file_names[i])
        ax.scatter(x_points, y_points, z_points, color=color_names[i], s=w_points)
        x_points.clear()
        y_points.clear()
        z_points.clear()

    ax.set_xlabel(columns_array[0])
    ax.set_ylabel(columns_array[1])
    ax.set_zlabel(columns_array[2])

    plt.show()


main()

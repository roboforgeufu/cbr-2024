import matplotlib.pyplot as plt
import pandas as pd


def import_and_convert_csv(csv_file):
    df = pd.read_csv("./logs/" + csv_file)
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

    ax.set_xlim([0, 255])
    ax.set_ylim([0, 255])
    ax.set_zlim([0, 255])

    file_names = [
        "calib_ht-nxt-color-v2_2_BLUE_2024_10_21_17_11_11_605026.csv",
        "calib_ht-nxt-color-v2_2_BROWN_2024_10_21_17_12_08_638375.csv",
        "calib_ht-nxt-color-v2_2_GREEN_2024_10_21_17_11_50_821863.csv",
        "calib_ht-nxt-color-v2_2_None_2024_10_21_17_15_04_128259.csv",
        "calib_ht-nxt-color-v2_2_RED_2024_10_21_17_11_32_133530.csv",
        "calib_ht-nxt-color-v2_2_WHITE_2024_10_21_17_12_33_465830.csv",
    ]
    color_names = ["blue", "brown", "green", "gray", "red", "white"]

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

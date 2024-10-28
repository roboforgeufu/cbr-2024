import os

os.environ["PATH"] += (
    os.pathsep + "C:/Program Files/Graphviz/bin"
)  # graphviz path (windows)

from sklearn import tree
import pandas as pd
import graphviz
import numpy as np
from sklearn.tree import _tree


def stringfy_color(color):
    return color[6:] if color.startswith("Color.") else color


LOGS_PATH = "./logs/"


def get_colors_and_features(sensor_type, sensor_position):
    if sensor_type == "ht-nxt-color-v2":
        feature_names = ["R", "G", "B", "W"]
    else:
        feature_names = ["R", "G", "B"]

    if sensor_position == "claw":
        color_names = [
            "Color.BLUE",
            "Color.BROWN",
            "Color.GREEN",
            "None",
            "Color.RED",
            "Color.WHITE",
        ]
    elif sensor_position == "floor":
        color_names = [
            "Color.BLUE",
            "Color.BLACK",
            "Color.BROWN",
            "Color.GREEN",
            "None",
            "Color.RED",
            "Color.WHITE",
            "Color.YELLOW",
        ]

    # IMPORTANTE ESTAR EM ORDEM ALFABÉTICA (E NA MESMA ORDEM QUE OS ARQUIVOS)!!!
    color_names.sort(key=stringfy_color)
    return color_names, feature_names


def get_all_files_into_dataframe(file_names):
    dataframes = []
    for csv_file in file_names:
        df = pd.read_csv(LOGS_PATH + csv_file, header=None)
        dataframes.append(df)
    full_dataframe = pd.concat(dataframes, ignore_index=True)
    return full_dataframe


def export_tree_to_pdf(tree_model, pdf_name, class_names, feature_names):
    # Exportar para pdf (visualização)
    dot_data = tree.export_graphviz(
        tree_model, feature_names=feature_names, filled=True, class_names=class_names
    )
    graph = graphviz.Source(dot_data)
    graph.render(pdf_name)


# Exportar para código
def tree_to_code(tree, feature_names, classes, function_name="predict", file=None):
    # Extraido e adaptado de: https://mljar.com/blog/extract-rules-decision-tree/
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    with open(file, "w") as f:
        print("from pybricks.parameters import Color\n", file=f)
        print("def {}({}):".format(function_name, ", ".join(feature_names)), file=f)

        def recurse(node, depth):
            indent = "    " * depth
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                print(
                    "{}if {} <= {}:".format(indent, name, np.round(threshold, 2)),
                    file=f,
                )
                recurse(tree_.children_left[node], depth + 1)
                print(
                    "{}else:  # if {} > {}".format(
                        indent, name, np.round(threshold, 2)
                    ),
                    file=f,
                )
                recurse(tree_.children_right[node], depth + 1)
            else:
                print(
                    "{}return {}".format(indent, classes[tree_.value[node].argmax()]),
                    file=f,
                )

        recurse(0, 1)


def ask_sensor():
    answer = input("Selecione o sensor:\n 1 - Hi Technic\n 2 - Ev3 ColorSensor:")
    if int(answer) == 1:
        sensor = "ht-nxt-color-v2"
    elif int(answer) == 2:
        sensor = "lego-ev3-color"

    port = int(input("Nro. da porta:"))

    answer = input("Selecione a posição do sensor:\n 1 - Chão\n 2 - Garra:")
    if int(answer) == 1:
        position = "floor"
    elif int(answer) == 2:
        position = "claw"

    return sensor, port, position


def get_filenames_for_sensor(sensor, port, color_names):
    file_names = []
    for file in os.listdir(LOGS_PATH):
        for color_name in color_names:
            if file.startswith(f"calib_{sensor}_{port}_{stringfy_color(color_name)}"):
                file_names.append(file)

    return file_names


def main():
    sensor, port, position = ask_sensor()

    color_names, feature_names = get_colors_and_features(sensor, position)

    filenames = get_filenames_for_sensor(sensor, port, color_names)

    dataframe = get_all_files_into_dataframe(filenames)
    full_color_names = list(
        elem for sublist in ([color] * 100 for color in color_names) for elem in sublist
    )

    classifier = tree.DecisionTreeClassifier(max_depth=4)
    tree_model = classifier.fit(dataframe, full_color_names)

    export_tree_to_pdf(
        tree_model, "tree", class_names=sorted(color_names), feature_names=feature_names
    )

    sensor = sensor.replace("-", "_")

    tree_to_code(
        tree_model,
        feature_names,
        classes=sorted(color_names),
        function_name=f"{sensor}_p{port}_decision_tree",
        file=f"./src/decision_trees/{sensor}_{port}.py",
    )


if __name__ == "__main__":
    main()

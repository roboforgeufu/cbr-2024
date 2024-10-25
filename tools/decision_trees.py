import os

os.environ["PATH"] += (
    os.pathsep + "C:/Program Files/Graphviz/bin"
)  # graphviz path (windows)

from sklearn import tree
import pandas as pd
import graphviz
import numpy as np

classifier = tree.DecisionTreeClassifier(max_depth=4)

file_names = [  # IMPORTANTE ESTAR EM ORDEM ALFABÉTICA!!!
    "calib_ht-nxt-color-v2_2BLUE_2024_10_21_17_11_11_605026.csv",
    "calib_ht-nxt-color-v2_2BROWN_2024_10_21_17_12_08_638375.csv",
    "calib_ht-nxt-color-v2_2GREEN_2024_10_21_17_11_50_821863.csv",
    "calib_ht-nxt-color-v2_2RED_2024_10_21_17_11_32_133530.csv",
    "calib_ht-nxt-color-v2_2WHITE_2024_10_21_17_12_33_465830.csv",
    "calib_ht-nxt-color-v2_2None_2024_10_21_17_15_04_128259.csv",
]
color_names = [  # IMPORTANTE ESTAR EM ORDEM ALFABÉTICA!!!
    "Color.BLUE",
    "Color.BROWN",
    "Color.GREEN",
    "Color.RED",
    "Color.WHITE",
    "None",
]
feature_names = ["R", "G", "B", "W"]


dataframes = []
for csv_file in file_names:
    df = pd.read_csv("./logs/" + csv_file, header=None)
    dataframes.append(df)
full_dataframe = pd.concat(dataframes, ignore_index=True)


full_color_names = list(
    elem for sublist in ([color] * 100 for color in color_names) for elem in sublist
)

# Treinamento do modelo
tree_model = classifier.fit(full_dataframe, full_color_names)


# Exportar para pdf (visualização)
dot_data = tree.export_graphviz(
    tree_model,
    feature_names=feature_names,
    filled=True,
    class_names=color_names,
)
graph = graphviz.Source(dot_data)
graph.render("tree")


# Exportar para código
from sklearn.tree import _tree


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


tree_to_code(
    tree_model,
    feature_names,
    classes=color_names,
    function_name="hitechnic_decision_tree",
    file="./src/decision_trees/ht_nxt_color_v2.py",
)

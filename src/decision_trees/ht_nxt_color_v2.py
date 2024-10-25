from pybricks.parameters import Color

def hitechnic_decision_tree(R, G, B, W):
    if R <= 206.0:
        if G <= 219.0:
            if R <= 39.5:
                if W <= 24.0:
                    return None
                else:  # if W > 24.0
                    return None
            else:  # if R > 39.5
                return Color.BLUE
        else:  # if G > 219.0
            return Color.GREEN
    else:  # if R > 206.0
        if G <= 92.0:
            return Color.RED
        else:  # if G > 92.0
            if G <= 196.5:
                return Color.BROWN
            else:  # if G > 196.5
                return Color.WHITE

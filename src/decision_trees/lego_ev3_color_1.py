from pybricks.parameters import Color

def _decision_tree(R, G, B):
    if R <= 10.5:
        if G <= 0.5:
            if R <= 0.5:
                return None
            else:  # if R > 0.5
                if R <= 4.5:
                    return Color.BROWN
                else:  # if R > 4.5
                    return Color.RED
        else:  # if G > 0.5
            if B <= 5.5:
                if G <= 7.5:
                    return Color.BROWN
                else:  # if G > 7.5
                    return Color.GREEN
            else:  # if B > 5.5
                if R <= 6.5:
                    return Color.BLUE
                else:  # if R > 6.5
                    return Color.WHITE
    else:  # if R > 10.5
        if B <= 1.0:
            return Color.RED
        else:  # if B > 1.0
            if G <= 10.0:
                return Color.BROWN
            else:  # if G > 10.0
                return Color.WHITE

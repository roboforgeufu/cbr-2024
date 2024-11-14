from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p3_decision_tree(R, G, B):
    if R <= 1.0:
        return None
    else:  # if R > 1.0
        if R <= 17.0:
            if G <= 19.5:
                if B <= 14.0:
                    return Color.BLACK
                else:  # if B > 14.0
                    return Color.BLUE
            else:  # if G > 19.5
                return Color.GREEN
        else:  # if R > 17.0
            if B <= 6.5:
                if R <= 41.5:
                    return Color.BROWN
                else:  # if R > 41.5
                    return Color.RED
            else:  # if B > 6.5
                if B <= 49.0:
                    return Color.YELLOW
                else:  # if B > 49.0
                    return Color.WHITE

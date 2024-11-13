from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p2_decision_tree(R, G, B):
    if R <= 1.0:
        return None
    else:  # if R > 1.0
        if R <= 27.0:
            if B <= 14.5:
                if G <= 19.0:
                    if R <= 8.5:
                        return Color.BLACK
                    else:  # if R > 8.5
                        return Color.BROWN
                else:  # if G > 19.0
                    return Color.GREEN
            else:  # if B > 14.5
                return Color.BLUE
        else:  # if R > 27.0
            if G <= 28.5:
                return Color.RED
            else:  # if G > 28.5
                if B <= 22.0:
                    return Color.YELLOW
                else:  # if B > 22.0
                    return Color.WHITE

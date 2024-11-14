from pybricks.parameters import Color


# Arquivo gerado automaticamente
def lilo_lego_ev3_color_p1_decision_tree(R, G, B):
    if R <= 1.5:
        return None
    else:  # if R > 1.5
        if R <= 13.5:
            if B <= 11.5:
                if G <= 12.5:
                    return Color.BLACK
                else:  # if G > 12.5
                    return Color.GREEN
            else:  # if B > 11.5
                return Color.BLUE
        else:  # if R > 13.5
            if B <= 12.0:
                if G <= 42.5:
                    if R <= 31.0:
                        return Color.BROWN
                    else:  # if R > 31.0
                        return Color.RED
                else:  # if G > 42.5
                    return Color.YELLOW
            else:  # if B > 12.0
                return Color.WHITE

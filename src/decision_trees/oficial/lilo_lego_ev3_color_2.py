from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p2_decision_tree(R, G, B):
    if R <= 2.0:
        return None
    else:  # if R > 2.0
        if R <= 11.5:
            if B <= 12.5:
                if G <= 19.0:
                    return Color.BLACK
                else:  # if G > 19.0
                    return Color.GREEN
            else:  # if B > 12.5
                return Color.BLUE
        else:  # if R > 11.5
            if B <= 39.0:
                if B <= 3.5:
                    if R <= 32.0:
                        return Color.BROWN
                    else:  # if R > 32.0
                        return Color.RED
                else:  # if B > 3.5
                    return Color.YELLOW
            else:  # if B > 39.0
                return Color.WHITE

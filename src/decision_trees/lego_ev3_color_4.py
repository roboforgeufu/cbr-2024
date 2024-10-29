from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lego_ev3_color_p4_decision_tree(R, G, B):
    if B <= 10.5:
        if R <= 2.5:
            return None
        else:  # if R > 2.5
            if R <= 31.5:
                if G <= 12.0:
                    if R <= 7.5:
                        return Color.BLACK
                    else:  # if R > 7.5
                        return Color.BROWN
                else:  # if G > 12.0
                    return Color.GREEN
            else:  # if R > 31.5
                return Color.RED
    else:  # if B > 10.5
        if G <= 34.0:
            return Color.BLUE
        else:  # if G > 34.0
            if B <= 40.0:
                return Color.YELLOW
            else:  # if B > 40.0
                return Color.WHITE

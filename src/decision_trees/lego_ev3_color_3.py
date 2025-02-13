from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lego_ev3_color_p3_decision_tree(R, G, B):
    if B <= 26.5:
        if G <= 3.5:
            return None
        else:  # if G > 3.5
            if G <= 38.0:
                if R <= 29.5:
                    if B <= 2.5:
                        if G <= 14.0:
                            if R <= 8.5:
                                return Color.BLACK
                            else:  # if R > 8.5
                                return Color.BROWN
                        else:  # if G > 14.0
                            return Color.GREEN
                    else:  # if B > 2.5
                        return Color.BLUE
                else:  # if R > 29.5
                    return Color.RED
            else:  # if G > 38.0
                return Color.YELLOW
    else:  # if B > 26.5
        return Color.WHITE

from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p4_decision_tree(R, G, B):
    if B <= 25.5:
        if G <= 27.5:
            if R <= 31.5:
                if G <= 19.0:
                    if B <= 8.0:
                        if R <= 8.0:
                            return Color.BLACK
                        else:  # if R > 8.0
                            return Color.BROWN
                    else:  # if B > 8.0
                        if R <= 8.5:
                            return Color.BLUE
                        else:  # if R > 8.5
                            return None
                else:  # if G > 19.0
                    return Color.GREEN
            else:  # if R > 31.5
                return Color.RED
        else:  # if G > 27.5
            return Color.YELLOW
    else:  # if B > 25.5
        return Color.WHITE

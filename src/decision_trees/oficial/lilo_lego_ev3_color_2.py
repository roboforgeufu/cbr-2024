from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p2_decision_tree(R, G, B):
    if G <= 0.5:
        return None
    else:  # if G > 0.5
        if B <= 8.5:
            if G <= 40.0:
                if R <= 28.5:
                    if R <= 7.5:
                        if G <= 14.5:
                            return Color.BLACK
                        else:  # if G > 14.5
                            return Color.GREEN
                    else:  # if R > 7.5
                        return Color.BROWN
                else:  # if R > 28.5
                    return Color.RED
            else:  # if G > 40.0
                return Color.YELLOW
        else:  # if B > 8.5
            if G <= 16.5:
                return Color.BLUE
            else:  # if G > 16.5
                return Color.WHITE

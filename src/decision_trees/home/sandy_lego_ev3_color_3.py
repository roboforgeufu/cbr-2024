from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def sandy_lego_ev3_color_p3_decision_tree(R, G, B):
    if G <= 0.5:
        return None
    else:  # if G > 0.5
        if G <= 16.5:
            if R <= 14.5:
                if B <= 2.5:
                    if G <= 4.5:
                        if R <= 3.5:
                            return Color.BLACK
                        else:  # if R > 3.5
                            return Color.BROWN
                    else:  # if G > 4.5
                        return Color.GREEN
                else:  # if B > 2.5
                    return Color.BLUE
            else:  # if R > 14.5
                return Color.RED
        else:  # if G > 16.5
            if B <= 18.0:
                return Color.YELLOW
            else:  # if B > 18.0
                return Color.WHITE

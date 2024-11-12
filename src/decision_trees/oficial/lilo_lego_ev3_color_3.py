from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p3_decision_tree(R, G, B):
    if G <= 3.5:
        return None
    else:  # if G > 3.5
        if B <= 18.5:
            if G <= 12.5:
                return Color.BLACK
            else:  # if G > 12.5
                if G <= 23.0:
                    if R <= 43.5:
                        return Color.BROWN
                    else:  # if R > 43.5
                        return Color.RED
                else:  # if G > 23.0
                    if R <= 27.5:
                        return Color.GREEN
                    else:  # if R > 27.5
                        return Color.YELLOW
        else:  # if B > 18.5
            if B <= 59.5:
                return Color.BLUE
            else:  # if B > 59.5
                return Color.WHITE

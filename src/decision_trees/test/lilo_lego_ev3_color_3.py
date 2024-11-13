from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def lilo_lego_ev3_color_p3_decision_tree(R, G, B):
    if G <= 2.0:
        return None
    else:  # if G > 2.0
        if G <= 12.5:
            if R <= 31.0:
                if R <= 8.5:
                    return Color.BLACK
                else:  # if R > 8.5
                    return Color.BROWN
            else:  # if R > 31.0
                return Color.RED
        else:  # if G > 12.5
            if R <= 9.5:
                if G <= 21.5:
                    return Color.BLUE
                else:  # if G > 21.5
                    return Color.GREEN
            else:  # if R > 9.5
                if B <= 10.5:
                    return Color.YELLOW
                else:  # if B > 10.5
                    return Color.WHITE

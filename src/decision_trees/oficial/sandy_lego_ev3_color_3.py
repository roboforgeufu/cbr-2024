from pybricks.parameters import Color
 # Arquivo gerado automaticamente
def sandy_lego_ev3_color_p3_decision_tree(R, G, B):
    if R <= 5.0:
        if G <= 6.5:
            if B <= 4.0:
                return Color.BLACK
            else:  # if B > 4.0
                return Color.BLUE
        else:  # if G > 6.5
            return Color.GREEN
    else:  # if R > 5.0
        if R <= 18.5:
            if B <= 2.5:
                return Color.BROWN
            else:  # if B > 2.5
                return None
        else:  # if R > 18.5
            if G <= 14.0:
                return Color.RED
            else:  # if G > 14.0
                if B <= 18.0:
                    return Color.YELLOW
                else:  # if B > 18.0
                    return Color.WHITE

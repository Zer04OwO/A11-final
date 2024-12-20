import level1
import level2
import level3
import display_win_or_loss
import pygame
import sys

"""
This provides the overall structure of the game.

Written by David Johnson for CS 1400.
"""

def main():
    """
    Call the three levels of the game and
    display a loss or win screen.
    :return: Only for exit the function
    """
    # passed_level1 = level1.level1()
    # if not passed_level1:
    #     display_win_or_loss.display_loss_screen()
    #     return

    passed_level2 = level2.level2()
    if not passed_level2:
        display_win_or_loss.display_loss_screen()
        return
    #
    passed_level3 = level3.level3()
    if not passed_level3:
        display_win_or_loss.display_loss_screen()
        return

    # If we get this far, all three levels are completed.
    display_win_or_loss.display_win_screen()


if __name__ == "__main__":
    main()
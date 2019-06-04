#!/usr/bin/env python
# -*- coding: utf-8 -*-

from colorama import Fore, Back, Style
import xmastree
import json
import os
import sys

if __name__ == '__main__':
    tree_settings = json.load(open('tree.settings', 'r'))

    # height of the tree (must be >= 3, int or float)
    size = tree_settings.get('size', 20)

    # symbol of the star on the top of the tree (any ASCII char)
    star = tree_settings.get('star', '\u2606')

    # tree needles. is used if left_needles or right_needles not specified (any ASCII char)
    needles = tree_settings.get('needles', 'Y')

    # needles of the left side of the tree. is preferable than needles if specified (any ASCII char or null)
    left_needles = tree_settings.get('left_needles', None)

    # needles of the right side of the tree. is preferable than needles if specified (any ASCII char or null)
    right_needles = tree_settings.get('right_needles', None)

    # randomly trim one symbol from sides of the tree to emitate not perfect form of the tree (true or false)
    trim_edges = tree_settings.get('trim_edges', True)

    # defines the rules for choosing decorations positions
    #    "random" - decorations placed randomly (number of decorations <= 1/4 of layer size at most)
    #    "pattern" - draw garland
    decoration_choice = tree_settings.get('decoration_choice', 'random')

    # char that represents decoration unit (any ASCII char)
    decoration_char = tree_settings.get('decoration', '*')

    # background color of terminal ("black", red", "green", "yellow", "blue", "magenta", "cyan", "white", null)
    background_color = tree_settings.get('background_color', None)

    # color of the tree ("black", red", "green", "yellow", "blue", "magenta", "cyan", "white")
    base_color = tree_settings.get('base_color', 'green')

    # color of the star ("black", red", "green", "yellow", "blue", "magenta", "cyan", "white")
    star_color = tree_settings.get('star_color', 'red')

    # color of the trunk ("black", red", "green", "yellow", "blue", "magenta", "cyan", "white")
    trunk_color = tree_settings.get('trunk_color', 'black')

    # decorations colors palette (list of colors, at most ["black", red", "green", "yellow", "blue", "magenta", "cyan", "white"])
    palette = tree_settings.get('palette', ['red', 'yellow', 'blue', 'magenta', 'cyan', 'white'])

    # defines the rules for choosing decorations colors (for each decoration unit)
    #    "random" - random color (from palette) for each decoration unit
    #    "full" - random color (from palette) for ALL decorations on the tree
    #    "by_layer" - random color (from palette) for each layer of the tree
    colors_choice = tree_settings.get('colors_choice', 'random')

    # defines the rules for choosing style of preinting tree
    #    "color" - print colorized by color_choice rules tree
    #    "mono" - print tree in default terminal's color scheme
    style = tree_settings.get('style', 'color')

    # fps with which tree will be redrawen if animation is choosen (int)
    fps = tree_settings.get('fps', 2)

    # animate tree or not (True, False)
    animation = tree_settings.get('animate', True)

    # choose brightness of the picture
    #    "bright" - the brightest
    #    "normal" - normal brightness
    #    "dim" - least bright
    brightness = tree_settings.get('brightness', 'bright')

    # generate tree, decorations positions and merge them
    base_tree = xmastree.generate_tree(size, star=star, needles=needles, left_needles=left_needles, right_needles=right_needles, trim_edges=trim_edges)
    decorations_positions = xmastree.generate_decorations(base_tree, decoration_choice=decoration_choice)
    decorated_tree = xmastree.add_decorations(base_tree, decorations_positions, decoration=decoration_char)

    # change brightness of the terminal
    if brightness == 'bright':
        print(Style.BRIGHT)
    elif brightness == 'normal':
        print(Style.NORMAL)
    elif brightness == 'dim':
        print(Style.DIM)

    # print tree
    if animation:
        xmastree.animate(decorated_tree, decorations_positions, background_color=background_color, base_color=base_color, star_color=star_color, trunk_color=trunk_color, palette=palette, colors_choice=colors_choice, style=style, fps=fps)
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        decoration_colors, bs_color, bg_color = xmastree.colorize(decorations_positions, background_color=background_color, base_color=base_color, star_color=star_color, trunk_color=trunk_color, palette=palette, colors_choice=colors_choice)
        xmastree.print_tree(decorated_tree, decorations_positions, decoration_colors, bs_color, style=style, background_color=bg_color)

    # reset terminal settings and exit
    print(Style.RESET_ALL)
    sys.exit(0)

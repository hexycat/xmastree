#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time
import os
import sys
from colorama import Fore, Back, Style


def generate_tree(size, star='☆', needles='#', decoration='*', left_needles=None, right_needles=None, trim_edges=False, decoration_choice='random'):
    # top layer size is 1
    # every next layer is bigger by 2 than previous except of the bottom one
    # overall number of tree layer is equel to size

    # TO DO: add creation decorations by patterns

    max_tree_width = 1 + 2 * (size - 1)
    base_indent_size = int(max_tree_width // 2) # number of white spaces before the middle of the tree

    # store decoration positions for each layer of tree
    decorations = dict.fromkeys(range(size), [])
    # store entire tree layer by layer
    tree = dict.fromkeys(range(size), '')

    if left_needles is None:
        left_needles = needles
    if right_needles is None:
        right_needles = needles

    for layer_id in range(size):
        tree_layer_width = layer_id * 2 + 1
        tree_side_width = int(tree_layer_width // 2)
        indent = base_indent_size - layer_id

        # add star on the top of the tree
        if layer_id == 0:
            tree[layer_id] = ' ' * indent + star
            decorations[layer_id] = [0 + indent, ]
            continue

        # add tree trunk at the bottom
        if layer_id == size - 1:
            tree[layer_id] = ' ' * (base_indent_size - 1) + '| |'
            decorations[layer_id] = [i + (base_indent_size - 1) for i in range(3)] # trunk sonsists of tree elements
            break

        # generate tree base layer (fill with needles only)
        center_needle = random.choice([left_needles, right_needles])
        layer_base = left_needles * tree_side_width + center_needle + right_needles * tree_side_width

        if trim_edges:
            left_trim = random.choice([True, False])
            right_trim = random.choice([True, False])
            layer_base = ' ' * left_trim + layer_base[1 * left_trim : tree_layer_width - 1 * right_trim] + ' ' * right_trim

        # generate decorations positions
        if decoration_choice == 'random':
            n_decorations = random.randint(0, int(tree_layer_width / 4))
            decoration_positions = random.sample(range(tree_layer_width), n_decorations)
            decoration_positions = sorted(decoration_positions)
            # keep modiffied by indent size decorations positions to handle them properly later
            decorations[layer_id] = [indent + pos for pos in decoration_positions]
        elif decoration_choice == 'pattern':
            pass

        # add decorations to base layer
        from_id = 0
        for i in range(n_decorations):
            decoration_pos = decoration_positions[i]
            layer += layer_base[from_id:decoration_pos] + decoration
            from_id = decoration_pos + 1
            if i == n_decorations - 1:
                layer += layer_base[from_id:]

        if n_decorations == 0:
            layer = layer_base
        # save layer
        tree[layer_id] = ' ' * indent + layer
        layer = ''
        layer_base = ''
    return tree, decorations


def colorize(decorations, background_color=None, base_color='green', star_color='red', trunk_color='black', palette=['red', 'yellow', 'blue', 'magenta', 'cyan', 'white'], colors_choice='random'):
    # colors_choice: ['random', 'static', 'pattern']
    # ESC == '\033'

    # FOREGROUND:
    # ESC [ 30 m      # black
    # ESC [ 31 m      # red
    # ESC [ 32 m      # green
    # ESC [ 33 m      # yellow
    # ESC [ 34 m      # blue
    # ESC [ 35 m      # magenta
    # ESC [ 36 m      # cyan
    # ESC [ 37 m      # white
    # ESC [ 39 m      # reset

    # BACKGROUND
    # ESC [ 40 m      # black
    # ESC [ 41 m      # red
    # ESC [ 42 m      # green
    # ESC [ 43 m      # yellow
    # ESC [ 44 m      # blue
    # ESC [ 45 m      # magenta
    # ESC [ 46 m      # cyan
    # ESC [ 47 m      # white
    # ESC [ 49 m      # reset

    # TO DO: add static and pattern color choices

    basic_palette = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'reset': '\033[39m'
    }

    basic_palette_back = {
        'black': '\033[40m',
        'red': '\033[41m',
        'green': '\033[42m',
        'yellow': '\033[43m',
        'blue': '\033[44m',
        'magenta': '\033[45m',
        'cyan': '\033[46m',
        'white': '\033[47m',
        'reset': '\033[49m'
    }

    decoration_colors = dict.fromkeys(decorations.keys(), []) # store color for every decoration item including star and trunk
    base_color_code = basic_palette[base_color] # store base tree color
    background_color_code = basic_palette_back.get(background_color, None)

    # generate color for decorations
    colors_codes = [basic_palette[color] for color in palette] # colors codes choosing from
    for layer_id, decors in decorations.items():
        if layer_id == 0:
            decoration_colors[layer_id] = [basic_palette[star_color], ]
            continue

        if layer_id == len(decorations) - 1:
            decoration_colors[layer_id] = [basic_palette[trunk_color] for i in range(3)] # 3 - width of tree trunk
            break

        if colors_choice == 'random':
            for i in range(len(decors)):
                decoration_colors[layer_id].append(random.choice(colors_codes))
        elif colors_choice == 'static':
            pass
        elif colors_choice == 'pattern':
            pass

    return decoration_colors, base_color_code, background_color_code


def print_tree(tree, decorations, decoration_colors={}, base_color='', style='color', background_color=None):
    # style: ['mono', 'colorize']
    if background_color is not None:
        print(background_color + '')

    if style == 'mono':
        for layer_id, string in tree.items():
            print(string)
        return

    if style == 'color':
        for layer_id, string in tree.items():
            layer_decors = decorations[layer_id]
            n_decors = len(layer_decors)
            from_pos = 0
            for i in range(n_decors):
                decor = layer_decors[i]
                try:
                    color = decoration_colors[layer_id][i]
                except:
                    color = ''
                print(base_color + tree[layer_id][from_pos:decor] + color + tree[layer_id][decor], end='')
                from_pos = decor + 1
            print(base_color + tree[layer_id][from_pos:])


def animate(tree, decorations, fps=24):
    sleep_time = 1 / fps

    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            decoration_colors, base_color, background_color = colorize(decorations, background_color='black', base_color='green', trunk_color='magenta')
            print_tree(tree, decorations, decoration_colors, base_color, style='color', background_color=background_color)
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        print(Style.RESET_ALL + Back.WHITE)
        sys.exit(0)


if __name__ == '__main__':
    print(Style.BRIGHT)
    tree, decorations = generate_tree(30, needles='Y', star='^', trim_edges=True)
    animate(tree, decorations, fps=2)

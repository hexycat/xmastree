#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time
import os
from colorama import Fore, Back, Style
import math


def generate_decorations(tree, decoration_choice='random'):
    ''' Generate decorations positions for each layer of the tree and store them in a dict '''

    size = len(tree)
    max_tree_width = 1 + 2 * (size - 1)
    base_indent_size = int(max_tree_width // 2) # number of white spaces before the middle of the tree
    decorations = dict.fromkeys(range(size), [])
    previous_end_id = 0 # is used only in "pattern" case

    for layer_id in range(size):
        tree_layer_width = layer_id * 2 + 1
        indent = base_indent_size - layer_id

        if layer_id == 0:
            decorations[layer_id] = [0 + indent, ]
            continue

        if layer_id == size - 1:
            decorations[layer_id] = [i + (base_indent_size - 1) for i in range(3)] # trunk sonsists of three elements
            break

        # generate decorations positions
        if decoration_choice == 'random':
            n_decorations = random.randint(0, int(tree_layer_width / 4))
            decoration_positions = random.sample(range(tree_layer_width), n_decorations)
            decoration_positions = sorted(decoration_positions)
        elif decoration_choice == 'pattern':
            # each tree layer splits in three parts
            # each part consiquently filled with decoration character
            # one layer contains only one decorated part
            n_decorations = math.floor((tree_layer_width + 2) / 3)
            segment_to_fill = (layer_id + 2) % 3
            start_id = segment_to_fill * n_decorations # default id from which layer is filled with decorations
            if start_id - 2 == previous_end_id: # if there is a gap between previous segment's end and current start
                start_id -= 1 # shift current sart to the left to eliminate the gap
            end_id = min(tree_layer_width, start_id + n_decorations)
            decoration_positions = range(start_id, end_id)
            previous_end_id = end_id
        # save decorations positions modified by indentat size to handle them properly later
        decorations[layer_id] = [indent + pos for pos in decoration_positions]
    return decorations


def add_decorations(tree, decorations, decoration='*'):
    ''' Add decorations to base tree on generated positions '''

    size = len(tree)
    decorated_tree = dict.fromkeys(range(size), '')

    for layer_id in range(size):
        modified_layer = ''
        decoration_positions = decorations[layer_id]
        n_decorations = len(decorations[layer_id])

        if (n_decorations == 0) or (layer_id == 0) or (layer_id == size - 1):
            modified_layer = tree[layer_id]
            decorated_tree[layer_id] = modified_layer
            continue

        from_id = 0
        for i in range(n_decorations):
            decoration_pos = decoration_positions[i]
            modified_layer += tree[layer_id][from_id:decoration_pos] + decoration
            from_id = decoration_pos + 1
            if i == n_decorations - 1:
                modified_layer += tree[layer_id][from_id:]

        decorated_tree[layer_id] = modified_layer
    return decorated_tree


def generate_tree(size, star='☆', needles='#', left_needles=None, right_needles=None, trim_edges=False):
    # top layer size is 1
    # every next layer is bigger by 2 than previous except of the bottom one
    # overall number of tree layer is equel to size

    size = int(size)

    if size < 3:
      raise ValueError('Size of the tree must be equal or greater than 3!')

    max_tree_width = 1 + 2 * (size - 1)
    base_indent_size = int(max_tree_width // 2) # number of white spaces before the middle of the tree

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
            continue

        # add tree trunk at the bottom
        if layer_id == size - 1:
            tree[layer_id] = ' ' * (base_indent_size - 1) + '| |'
            break

        # generate tree base layer (fill with needles only)
        center_needle = random.choice([left_needles, right_needles])
        layer_base = left_needles * tree_side_width + center_needle + right_needles * tree_side_width

        if trim_edges:
            left_trim = random.choice([True, False])
            right_trim = random.choice([True, False])
            layer_base = ' ' * left_trim + layer_base[1 * left_trim : tree_layer_width - 1 * right_trim] + ' ' * right_trim

        tree[layer_id] = ' ' * indent + layer_base
    return tree


def colorize(decorations, background_color=None, base_color='green', star_color='red', trunk_color='black', palette=['red', 'yellow', 'blue', 'magenta', 'cyan', 'white'], colors_choice='random'):
    # colors_choice: ['random', 'full', 'by_layer']
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

    if colors_choice == 'full':
        full_color_code = random.choice(colors_codes)

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
        elif colors_choice == 'full':
            decoration_colors[layer_id] = [full_color_code, ] * len(decors)
        elif colors_choice == 'by_layer':
            decoration_colors[layer_id] = [random.choice(colors_codes), ] * len(decors)

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


def animate(tree, decorations, background_color, base_color, star_color, trunk_color, palette, colors_choice, style, fps=24):
    sleep_time = 1 / fps

    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            decoration_colors, bs_color, bg_color = colorize(decorations, background_color=background_color, base_color=base_color, star_color=star_color, trunk_color=trunk_color, palette=palette, colors_choice=colors_choice)
            print_tree(tree, decorations, decoration_colors, bs_color, style=style, background_color=bg_color)
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        return

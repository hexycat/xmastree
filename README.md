# xmastree
Simple Christmas Tree written in python for terminal.

# Usage
Run __main.py__.

# Options
Parameters of the tree are described in __tree.settings__ file (json):
 * `size` - height of the tree (total number of lines).   
 *Possible values*: any `float` or `int` >= 3  
 *Default value*: 20
 
 * `star` - character that used as star on the top of the tree.  
 *Possible values*: almost any `ASCII` char  
 *Default value*: "\u2606"
 
 * `needles` - character that used as needles for the whole tree. 
 This parameter ignored if `left_needles` or `right_needles` specified.  
 *Possible values*: almost any `ASCII` char  
 *Default value*: "Y"
 
 * `left_needles` - character that used as needles of the left side of the tree. 
 If not specified, `needles` is used instead.  
 *Possible values*: almost any `ASCII` char and null  
 *Default value*: null
 
 * `right_needles` - character that used as needles of the right side of the tree. 
 If not specified, `needles` is used instead.  
 *Possible values*: almost any `ASCII` char and null  
 *Default value*: null
 
 * `trim_edges` - randomly trim one symbol from sides of the tree (for each line except top and bottom one) 
 to emitate not perfect form of a real tree.  
 *Possible values*: true or false  
 *Default value*: true  
 
 * `decoration` -  character that used as tree decoration unit.  
 *Possible values*: almost any `ASCII` char   
 *Default value*: "*"  
 
 * `decoration_choice` - defines rules for choosing decorations positions.  
 *Possible values*:  
 "random" - decorations are placed randomly (total number of decorations per line <= 1/4 of layer size at most);  
 "pattern" - draw garland (total number of decorations per line ~ 1/3 of layer size)  
 *Default value*: "random"
 
 * `background_color` - color of a terminal.  
 *Possible values*: any of "black", red", "green", "yellow", "blue", "magenta", "cyan", "white", null  
 *Default value*: null
 
 * `base_color` - color of the tree.  
 *Possible values*: any of "black", red", "green", "yellow", "blue", "magenta", "cyan", "white"    
 *Default value*: "green"
 
 * `star_color` - color of the star.  
 *Possible values*: any of "black", red", "green", "yellow", "blue", "magenta", "cyan", "white"    
 *Default value*: "red"
 
 * `trunk_color` - color of the tree's trunk.  
 *Possible values*: any of "black", red", "green", "yellow", "blue", "magenta", "cyan", "white"    
 *Default value*: "black"
 
 * `palette` - list of color from which decorations color is choose.  
 *Possible values*: any set of "black", red", "green", "yellow", "blue", "magenta", "cyan", "white"    
 *Default value*: ["red", "yellow", "blue", "magenta", "cyan", "white"]
 
 * `colors_choice` - defines rules for choosing decorations colors (for each decoration unit).  
 *Possible values*:  
 "random" - random color (from palette) for each decoration unit;  
 "full" - random color (from palette) for ALL decorations on the tree;  
 "by_layer" - random color (from palette) for each layer of the tree  
 *Default value*: "random"
 
 * `style` - defines rules for choosing style of printing tree.  
 *Possible values*:  
 "color" - print colorized by color_choice rules tree;  
 "mono" - print tree in default terminal's color scheme  
 *Default value*: "color"  
 
 * `fps` - number of times per second with which tree will be redrawen if animation is choosen.
 Each time tree's decorations print in new colors.  
 *Possible values*: any `float` or `int` value > 0  
 *Default value*: 2
 
 * `animate` - animate tree with fps frequency or print just once.  
 *Possible values*: true or false  
 *Default value*: true  
 
 * `brightness` - brightness of printed image.  
 *Possible values*: "dim" or "normal" or "bright"  
 *Default value*: "bright"

# Requirements
Python 3.5+ and [colorama package](https://pypi.org/project/colorama/).

# Comments
Tested on linux mint 18.1.  
Some `ASCII` characters displayed incorrectly (maybe due to locale or terminal limitations).

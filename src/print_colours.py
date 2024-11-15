from enum import Enum

class debug_colours:

    class Colour(Enum):
        BOLD = '\033[01m'
        FG_BLACK = '\033[30m'
        FG_WHITE = '\033[37m'
        FG_RED = '\033[31m'
        FG_GREEN = '\033[32m'
        FG_ORANGE = '\033[33m'
        FG_BLUE = '\033[34m'
        FG_PURPLE = '\033[35m'
        FG_CYAN = '\033[36m'
        FG_LIGHTGREY = '\033[37m'
        FG_DARKGREY = '\033[90m'
        FG_LIGHTRED = '\033[91m'
        FG_LIGHTGREEN = '\033[92m'
        FG_YELLOW = '\033[93m'
        FG_LIGHTBLUE = '\033[94m'
        FG_PINK = '\033[95m'
        FG_LIGHTCYAN = '\033[96m'
        BG_BLACK = '\033[40m'
        BG_RED = '\033[41m'
        BG_GREEN = '\033[42m'
        BG_ORANGE = '\033[43m'
        BG_BLUE = '\033[44m'
        BG_PURPLE = '\033[45m'
        BG_CYAN = '\033[46m'
        BG_LIGHTGREY = '\033[47m'
        COMBO_OB = FG_ORANGE + BG_BLACK
        COMBO_PiB = FG_PINK + BG_BLACK
        COMBO_GB = FG_GREEN + BG_BLACK
        COMBO_BB = FG_BLUE + BG_BLACK
        COMBO_PuB = FG_PURPLE + BG_BLACK
        COMBO_LGrR = FG_LIGHTGREY + BG_RED + BOLD
        COMBO_NOTICEMESENPAI = FG_WHITE + BG_BLUE + BOLD
        

    '''Colors class:reset all colours with debug_colours.reset; two
    sub classes fg for foreground
    and bg for background; use as debug_colours.subclass.colourname.
    i.e. debug_colours.fg.red or debug_colours.bg.green to use.  
    Also, the generic bold, disable, underline, reverse, strike through,
    and invisible work with the main class i.e. debug_colours.bold'''
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'

    def setc(fg: Colour=Colour.FG_LIGHTGREY, bg: Colour=Colour.BG_BLACK):
        """Set the forground and or background for debug output.
        Due to the way these codes work, different values should be used 
        for FG or BG settings so be sure to use the correct enum value.
        """
        print(f"{bg.value}{fg.value}")
        # print("\033[33m")

    def reset():
        print("\033[0m")

    def d_print(text: str, fg: Colour=Colour.FG_LIGHTGREY, bg:Colour=Colour.BG_BLACK, combo:Colour=None):
        """When you want one colour per chunk of text, you've come to the right place.
        If a combo is passed in it automatically sets both colours to the preset.
        """
        if combo:
            print(combo.value)
        else:
            debug_colours.setc(fg=fg, bg=bg)

        print(text)
        debug_colours.reset()

    # print(debug_colours.bg.green, "SKk", debug_colours.fg.red, "Amartya")
    # print(debug_colours.bg.lightgrey, "SKk", debug_colours.fg.red, "Amartya")

class TextFormat(object):
    """ Convenience class for coloring console text. """
    CSI = "\x1B["

    def __init__(self, allow_color):
        self.allow_color = allow_color

    def color(self, data, *codes):
        """Set the colour for TextFormat"""
        if self.allow_color:
            code_text = ";".join(str(code) for code in codes)
            return "".join((self.CSI, code_text + "m", str(data),
                            self.CSI, "0m"))
        else:
            return str(data)

    def red(self, text):
        """Returns red text"""
        return self.color(text, 1, 31)

    def green(self, text):
        """Returns green text"""
        return self.color(text, 1, 32)

    def yellow(self, text):
        """Returns yellow text"""
        return self.color(text, 1, 33)

    def blue(self, text):
        """Returns blue text"""
        return self.color(text, 1, 34)

    def magenta(self, text):
        """Returns magenta text"""
        return self.color(text, 1, 35)

    def cyan(self, text):
        """Return cyan text"""
        return self.color(text, 1, 36)

    def white(self, text):
        """Return white text"""
        return self.color(text, 1, 37)

def log_error(message):
    FMT = TextFormat(True)
    print FMT.red("[ERROR] ") + message

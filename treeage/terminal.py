# -*- coding: utf-8 -*-

from blessed import Terminal as BlessedTerminal


class Terminal(BlessedTerminal):
    @property
    def clear_last(self):
        return self.clear_eol + self.move_up + self.move_x(0)


term = Terminal()

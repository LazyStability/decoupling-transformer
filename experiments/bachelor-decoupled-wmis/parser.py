#! /usr/bin/env python

import re

from lab.parser import Parser

class MwisParser(Parser):
    def __init__(self):
        Parser.__init__(self)
        self.add_pattern('number_leaf_factors', 'Number leaf factors: (.+)', required=False, type=int)
        self.add_pattern('mwis_weight', 'Weight of computed independent set: (.+)',required=False, type=int)

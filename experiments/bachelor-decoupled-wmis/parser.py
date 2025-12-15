#! /usr/bin/env python

import re

from lab.parser import Parser

def number_of_leaves(content, props):
    props[""]
    if re.search("Number final leaf candidates: (.+)")
def chils_edges(content, props):
    matches = re.findall(r"chils add (?:outside precondition|leaf intersection) edge between: (.+)", content)
    props["All edges"] = [(int(s) for s in matches)]
class MwisParser(Parser):
    def __init__(self):
        Parser.__init__(self)
        self.add_pattern('number_leaf_factors', 'Number leaf factors: (.+)', required=False, type=int)
        # self.add_pattern('mwis_weight', 'Weight of computed independent set: (.+)',required=False, type=int)
        # self.add_pattern('mwis_size', 'Size of computed independent set: (.+)',required=False, type=int)

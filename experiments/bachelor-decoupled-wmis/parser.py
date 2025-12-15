#! /usr/bin/env python

import re

from lab.parser import Parser
from numpy import array

def chils_edges(content, props):
    matches = re.findall(r"chils add (?:outside precondition|leaf intersection) edge between: (.+)", content)
    props["number_chils_edges"] = array(matches).size

class MwisParser(Parser):
    def __init__(self):
        Parser.__init__(self)
        self.add_pattern('number_leaf_factors', 'Number leaf factors: (.+)', required=False, type=int)
        self.add_pattern('factoring_time', 'Factoring time: (.+)s', required=False, type=float)

        self.add_pattern('ff_simplify_time', 'time to simplify: (.+)s', required=False, type=float)
        self.add_pattern('ff_num_unary_operators', r'unary operators... done! \[(.+) unary operators\]', required=False, type=int)
        
        self.add_pattern('transformation_time', 'Time for decoupled transformation: (.+)s', required=False, type=float)
        self.add_pattern("task_size", "Task size: (.+)", required=False, type=int)
        # self.add_pattern("original_task_size", "Original task size: (.+)", required=False, type=int)
        # self.add_pattern('number_variables', 'Number of variables: (.+)', required=False, type=int)
        # self.add_pattern('number_prime_variables', 'Number of primary variables: (.+)', required=False, type=int)
        # self.add_pattern('number_second_variables', 'Number of secondary variables: (.+)', required=False, type=int)
        # self.add_pattern('number_operators', 'Number of operators: (.+)', required=False, type=int)
        # self.add_pattern('number_axioms', 'Number of axioms: (.+)', required=False, type=int)

        # self.add_pattern('number_conclusive_leaves', "Number of conclusive leaves: (.+)", required=False, type=int)
        self.add_pattern('number_normal_leaves', "Number of normal leaves: (.+)", required=False, type=int)

        self.add_pattern('number_pruned_operators', "Number of pruned operators: (.+)", required=False, type=int)
        
        self.add_pattern('number_wmis_leaf_candidates', "Number final leaf candidates: (.+)", required=False, type=int)

        # Chils parsing
        self.add_pattern('mwis_weight', 'Weight of computed independent set: (.+)',required=False, type=int)
        self.add_pattern('mwis_size', 'Size of computed independent set: (.+)',required=False, type=int)
        self.add_function(chils_edges)

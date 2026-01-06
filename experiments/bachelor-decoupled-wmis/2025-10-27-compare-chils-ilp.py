#! /usr/bin/env python
import os
import os.path
import platform
import re
from collections import defaultdict
from pathlib import Path
from subprocess import call


import parser
import common_setup

from downward.experiment import FastDownwardExperiment
from downward.reports.absolute import AbsoluteReport
from downward.reports.compare import ComparativeReport
from downward.reports.scatter import ScatterPlotReport
from downward.reports.taskwise import TaskwiseReport
from lab import reports
from lab.environments import SlurmEnvironment, LocalEnvironment
from lab.reports import Attribute
from lab.reports.filter import FilterReport

##################################
## Helper Classes and Functions ##
##################################
class BWUniEnvironment(SlurmEnvironment):
    """Environment for the BWUni cluster in Baden-Württemberg."""

    DEFAULT_PARTITION = "cpu"
    DEFAULT_QOS = "normal"
    DEFAULT_TIME_LIMIT_PER_TASK = "18:00:00"
    # 64 cores on cpu nodes, 236G usable memory
    DEFAULT_MEMORY_PER_CPU = "3600M"
    # See slurm.conf
    MAX_TASKS = 1000

    @classmethod
    def is_present(cls):
        node = platform.node()
        return bool(re.match(r"uc3n(991|990)", node))

##########
## Code ##
##########
 
repo = os.environ["DOWNWARD_REPO"]
benchmarks_dir = os.environ["DOWNWARD_BENCHMARKS"]

print("Is this the bwCluster? Answer: ",BWUniEnvironment.is_present())
if BWUniEnvironment.is_present():
    SUITE = common_setup.DEFAULT_SATISFICING_SUITE
    ENVIRONMENT = BWUniEnvironment(
        email="qf226@stud.uni-heidelberg.de",
        memory_per_cpu="3500M", # adapt according to needs, this is per run and should be 100MB larger than the memory limit of the solver(s)
    )

else: 
    ENVIRONMENT=LocalEnvironment(processes=7)
    SUITE = [
        "depot:p01.pddl",
        "driverlog:p01.pddl",
        "elevators-opt08-strips:p01.pddl",
        "elevators-opt11-strips:p01.pddl",
        "elevators-sat08-strips:p01.pddl",
        "logistics00:probLOGISTICS-10-0.pddl",
        "miconic:s1-0.pddl",
        "nomystery-opt11-strips:p01.pddl",
        "nomystery-sat11-strips:p01.pddl",
        "openstacks-opt08-strips:p01.pddl",
        "openstacks-opt11-strips:p01.pddl",
        # "openstacks-opt14-strips:p01.pddl",
        "openstacks-sat08-strips:p01.pddl",
        "openstacks-sat11-strips:p01.pddl",
        # "openstacks-sat14-strips:p01.pddl",
        "transport-opt08-strips:p01.pddl",
        "transport-opt11-strips:p01.pddl",
        "transport-opt14-strips:p01.pddl",
        "transport-sat08-strips:p01.pddl",
        "transport-sat14-strips:p01.pddl",
        "zenotravel:p01.pddl",

        # Take longer
        "elevators-sat11-strips:p01.pddl",
        "transport-sat11-strips:p01.pddl",
    ]

ATTRIBUTES = common_setup.ATTRIBUTES
COMPONONENT_OPTION = {"ff":['--evaluator', 'hff=ff(transform=adapt_costs(one))',  '--search', 'lazy_greedy([hff], preferred=[hff], cost_type=one)'],
                      "blind":['--search', 'astar(blind())']}
DRIVER_OPTIONS= ["--overall-memory-limit", "3G", "--overall-time-limit", "30m"]

REV_NICKS = [
    ("decoupling", "wmis", "chils_local_run=true,"),
    # ("decoupling", "lp", ""),
]
STRATEGIES=[
    "MML", # maximize mobile leaves
    "MMAS", # maximize mobile action schemas
    "MM_OPT", # maximize mobility
    "MFA", # maximize mobile facts
    "MM", # maximize mobility (sum)
]
LP_STRATEGIES = [
    "L", #mml
    "AS", #mas
    "Mo", #mmopt
    "F", #mfa
    "M" # maximize mobility (sum) MM
]

exp = FastDownwardExperiment(environment=ENVIRONMENT)

exp.add_step("build", exp.build)
exp.add_step("start", exp.start_runs)
exp.add_step("parse", exp.parse)
exp.add_fetcher(name="mwis-fetcher")
# Externally run lp experiment
exp.add_fetcher(name='2-lp-fetcher',src=repo+'/experiments/bachelor-decoupled-wmis/lp-data/2s-lp-eval/properties')
exp.add_fetcher(name='30-lp-fetcher',src=repo+'/experiments/bachelor-decoupled-wmis/lp-data/30s-lp-eval/properties')

exp.add_parser(exp.EXITCODE_PARSER)
exp.add_parser(parser.MwisParser())
exp.add_parser(exp.TRANSLATOR_PARSER)
exp.add_parser(exp.ANYTIME_SEARCH_PARSER)
exp.add_parser(exp.PLANNER_PARSER)


for rev,rev_nick,extra_options in REV_NICKS:
    for component_name in COMPONONENT_OPTION:
        for strategy in STRATEGIES:
            algo_name = f"{component_name}-{rev_nick}-{strategy}" if rev_nick else strategy
            algo_options = f"decoupled({rev_nick}({extra_options}min_number_leaves=1,factoring_time_limit=5,strategy={strategy}))"

            exp.add_algorithm(algo_name, repo, rev , [
                "--root-task-transform", algo_options 
            ]+ COMPONONENT_OPTION[component_name],driver_options=DRIVER_OPTIONS )
exp.add_suite(benchmarks_dir, SUITE)

# exp.add_report(ComparativeReport(attributes=ATTRIBUTES, algorithm_pairs=[(f"inf-LP-{x}", f"inf-WMIS-{x}") for x in STRATEGIES]), outfile="LP-WMIS-compare.html")
for component_name in COMPONONENT_OPTION:
    for i in range(0,5):
        exp.add_report(ComparativeReport(
            attributes=[ "task_size","transformation_time" ],
            algorithm_pairs=[(f"{component_name}-CPLEX-{LP_STRATEGIES[i]}0.2s1M-2",f"{component_name}-wmis-{STRATEGIES[i]}")],
            ),
        outfile=f"{component_name}-LP-WMIS-compare{STRATEGIES[i]}.html",
        )

#
exp.add_report(
    ScatterPlotReport(
        attributes=["task_size"],
        filter_algorithm=[
            f"blind-CPLEX-{LP_STRATEGIES[1]}0.2s1M-2",
            f"blind-wmis-{STRATEGIES[1]}"
        ],
        format="png",
    ),
    name=f"Comparison-lp-wmis-task_size-ff-{STRATEGIES[1]}",
)
for component_name in COMPONONENT_OPTION:
    for i in range(0,5):
        #"transformation_time",
        for attr in [ "task_size"]:
            exp.add_report(
                ScatterPlotReport(
                    # scale ="linear",
                    # scale = "symlog",
                    scale = "log",
                    attributes=[attr],
                    filter_algorithm=[
                        f"{component_name}-CPLEX-{LP_STRATEGIES[i]}0.2s1M-2",
                        f"{component_name}-wmis-{STRATEGIES[i]}"
                    ],
                    format="png",
                ),
                name=f"Scatterplot-lp-wmis-{attr}-{component_name}-{STRATEGIES[i]}",
            )
exp.add_report(AbsoluteReport(attributes=ATTRIBUTES), outfile=f"test-all.html")
exp.run_steps()

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
    DEFAULT_TIME_LIMIT_PER_TASK = "12:00:00"
    # 64 cores on cpu nodes, 236G usable memory
    DEFAULT_MEMORY_PER_CPU = "3600M"
    # See slurm.conf
    MAX_TASKS = 1000

    @classmethod
    def is_present(cls):
        node = platform.node()
        return bool(re.match(r"uc3n990", node))

##########
## Code ##
##########
 
repo = os.environ["DOWNWARD_REPO"]
benchmarks_dir = os.environ["DOWNWARD_BENCHMARKS"]
rev = "decoupling"
ATTRIBUTES = [
    "error",
    "plan",
    "times"
]
print("Is this the bwCluster? Answer: ",BWUniEnvironment.is_present())
if BWUniEnvironment.is_present():
    # Satisficing
    SUITE = [
        "agricola-sat18-strips", "airport", "assembly", "barman-sat11-strips",
        "barman-sat14-strips", "blocks", "caldera-sat18-adl",
        "caldera-split-sat18-adl", "cavediving-14-adl", "childsnack-sat14-strips",
        "citycar-sat14-adl", "data-network-sat18-strips", "depot", "driverlog",
        "elevators-sat08-strips", "elevators-sat11-strips", "flashfill-sat18-adl",
        "floortile-sat11-strips", "floortile-sat14-strips", "freecell",
        "ged-sat14-strips", "grid", "gripper", "hiking-sat14-strips",
        "logistics00", "logistics98", "maintenance-sat14-adl", "miconic",
        "miconic-fulladl", "miconic-simpleadl", "movie", "mprime", "mystery",
        "nomystery-sat11-strips", "nurikabe-sat18-adl", "openstacks",
        "openstacks-sat08-adl", "openstacks-sat08-strips",
        "openstacks-sat11-strips", "openstacks-sat14-strips", "openstacks-strips",
        "optical-telegraphs", "organic-synthesis-sat18-strips",
        "organic-synthesis-split-sat18-strips", "parcprinter-08-strips",
        "parcprinter-sat11-strips", "parking-sat11-strips", "parking-sat14-strips",
        "pathways", "pegsol-08-strips", "pegsol-sat11-strips", "philosophers",
        "pipesworld-notankage", "pipesworld-tankage", "psr-large", "psr-middle",
        "psr-small", "rovers", "satellite", "scanalyzer-08-strips",
        "scanalyzer-sat11-strips", "schedule", "settlers-sat18-adl",
        "snake-sat18-strips", "sokoban-sat08-strips", "sokoban-sat11-strips",
        "spider-sat18-strips", "storage", "termes-sat18-strips",
        "tetris-sat14-strips", "thoughtful-sat14-strips", "tidybot-sat11-strips",
        "tpp", "transport-sat08-strips", "transport-sat11-strips",
        "transport-sat14-strips", "trucks", "trucks-strips",
        "visitall-sat11-strips", "visitall-sat14-strips",
        "woodworking-sat08-strips", "woodworking-sat11-strips", "zenotravel",
    ]
    ENVIRONMENT = BWUniEnvironment(
        email="qf226@stud.uni-heidelberg.de",
        memory_per_cpu="3500M", # adapt according to needs, this is per run and should be 100MB larger than the memory limit of the solver(s)
    )

else: 
    ENVIRONMENT=LocalEnvironment(processes=2)
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

exp = FastDownwardExperiment(environment=ENVIRONMENT)

exp.add_step("build", exp.build)
exp.add_step("start", exp.start_runs)
exp.add_step("parse", exp.parse)
exp.add_fetcher(name="fetch")

exp.add_parser(exp.EXITCODE_PARSER)
exp.add_parser(parser.DecouplingParser())
exp.add_parser(exp.TRANSLATOR_PARSER)
exp.add_parser(exp.ANYTIME_SEARCH_PARSER)
exp.add_parser(exp.PLANNER_PARSER)

exp.add_algorithm("decoupled-new", repo, rev, [
    "--search", "astar(blind())",
    "--root-task-transform", "decoupled(factoring=wmis())" 
])
exp.add_suite(benchmarks_dir, SUITE)

attributes = common_setup.ATTRIBUTES

exp.add_report(AbsoluteReport(attributes=attributes), outfile=f"test-all.html")

exp.run_steps()

#! /usr/bin/env python
import os
import os.path
import decoupling_parser
import common_setup
from collections import defaultdict
from pathlib import Path
from subprocess import call

from downward.experiment import FastDownwardExperiment
from downward.reports.absolute import AbsoluteReport
from downward.reports.compare import ComparativeReport
from downward.reports.scatter import ScatterPlotReport
from downward.reports.taskwise import TaskwiseReport
from lab import reports
from lab.environments import BaselSlurmEnvironment, LocalEnvironment
from lab.reports import Attribute
from lab.reports.filter import FilterReport

repo = os.environ["DOWNWARD_REPO"]
benchmarks_dir = os.environ["DOWNWARD_BENCHMARKS"]
rev = "decoupling"
ATTRIBUTES = [
    "error",
    # "plan",
    # "times"
]
ENVIRONMENT=LocalEnvironment(processes=2)
SUITE = [
    "depot:p01.pddl",
    "driverlog:p01.pddl",
    # "elevators-*",
    # "logistics00",
    # "miconic",
    # "nomystery-*",
    # "openstacks-{opt/sat}XY-strips",
    # "*transport-*",
    # "zenotravel"
]

exp = FastDownwardExperiment(environment=ENVIRONMENT)

exp.add_step("build", exp.build)
exp.add_step("start", exp.start_runs)
exp.add_step("parse", exp.parse)
exp.add_fetcher(name="fetch")

exp.add_parser(exp.EXITCODE_PARSER)
exp.add_parser(decoupling_parser.DecouplingParser())
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

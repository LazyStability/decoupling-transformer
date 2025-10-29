#! /usr/bin/env python
import os
import os.path
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
    "plan",
    "times"
]

exp = FastDownwardExperiment()

exp.add_step("build", exp.build)
exp.add_step("start", exp.start_runs)
exp.add_step("parse", exp.parse)
exp.add_fetcher(name="fetch")

exp.add_parser(exp.EXITCODE_PARSER)
exp.add_parser(exp.TRANSLATOR_PARSER)
exp.add_parser(exp.ANYTIME_SEARCH_PARSER)
exp.add_parser(exp.PLANNER_PARSER)

exp.add_algorithm("decoupled-new", repo, rev, [
    "--search", "astar(blind())"
    "--root-task-transform" "decoupled(factoring=wmis())" 
])
exp.add_suite(benchmarks_dir, [
                               "depot",
                               "driverlog",
                               "elevators-*",
                               "logistics00",
                               "miconic",
                               "nomystery-*",
                               "openstacks-{opt/sat}XY-strips",
                               "*transport-*",
                               "zenotravel"
                               ])

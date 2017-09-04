import subprocess
import copy
from pathlib import Path
from itertools import product
import random
from bac.simulate.coding import Encoder
from bac.simulate.basesimulation import BaseSimulation

from typing import List


class Workflow:
    """

    Attributes
    ----------
    simulations: list
        The list of simulations in the workflow. This is generic and not dependent
        on the ensembles. The actual simulation list, which is for all ensembles
        is generated at `execute` time.
    ensembles: list
        A list of ensemble mechanism used to duplicated the simulations.
    """

    def __init__(self, resource, name):
        """

        Parameters
        ----------
        resource: str
            The supercomputer the workflow will run on.
        name: str
            The name of the simulation. This will be the master folder name too.

        Methods
        -------


        """

        self.resource = resource
        self.path = Path(name + '_' + str(random.randint(1000, 9999)))

        self.simulations: List[BaseSimulation] = []
        self._simulations: List[BaseSimulation] = []
        self.ensembles = []

    def add_simulation(self, simulation: BaseSimulation):
        """

        Parameters
        ----------
        simulation: BaseSimulation

        Returns
        -------

        """
        self.simulations.append(simulation)

    def execute(self):

        self.preprocess_simulations()

        while len(self):
            sim = next(sim for sim in self._simulations if sim.is_ready)

            subprocess.run(sim.executable)

        print('Executing on {}'.format(self.resource))

    def preprocess_simulations(self, execute=True):
        """Run pre-processing tasks for the simulations.

        Parameters
        ----------
        execute: bool
            Execute the preprocessing step on the shell. If `False` then the
            executable is printed to stdout.

        """
        for *ensembles, simulation in product(*self.ensembles, self.simulations):

            sim = copy.deepcopy(simulation)
            self._simulations.append(sim)

            for ensemble in ensembles:
                ensemble.modifier(sim)

            prefix = Path(*(ens.name for ens in ensembles))
            self.path.joinpath(prefix).mkdir(parents=True, exist_ok=True)

            sim.restructure_paths_with_prefix(prefix=prefix)

            Encoder.encode(sim, self.path)

            if execute:
                subprocess.run(sim.preprocess_executable, shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, cwd=self.path)
            else:
                print(sim.preprocess_executable)

    def __len__(self):
        return sum(1 if not x.is_finished else 0 for x in self._simulations)




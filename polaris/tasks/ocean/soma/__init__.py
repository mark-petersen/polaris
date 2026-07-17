import os

from polaris.config import PolarisConfigParser as PolarisConfigParser
from polaris.resolution import resolution_to_string
from polaris.tasks.ocean.soma.default import Default as Default
from polaris.tasks.ocean.soma.init import Init as Init


def add_soma_tasks(component):
    """
    Add tasks for different SOMA tests to the ocean component

    component : polaris.tasks.ocean.Ocean
        the ocean component that the tasks will be added to
    """
    for resolution in [32.0, 16.0, 8.0, 4.0]:
        resdir = resolution_to_string(resolution)
        resdir = f'spherical/soma/{resdir}'

        config_filename = 'soma.cfg'
        config = PolarisConfigParser(
            filepath=os.path.join(component.name, resdir, config_filename)
        )
        config.add_from_package('polaris.ocean.eos', 'linear.cfg')
        config.add_from_package('polaris.tasks.ocean.soma', 'soma.cfg')

        init = Init(component=component, resolution=resolution, indir=resdir)
        init.set_shared_config(config, link=config_filename)

        default = Default(
            component=component, resolution=resolution, indir=resdir, init=init
        )
        default.set_shared_config(config, link=config_filename)
        component.add_task(default)


# delete soon mrp
#        if resolution == 32.0:
#            decomp = Decomp(
#                component=component,
#                resolution=resolution,
#                indir=resdir,
#                init=init,
#            )
#            decomp.set_shared_config(config, link=config_filename)
#            component.add_task(decomp)
#
#            restart = Restart(
#                component=component,
#                resolution=resolution,
#                indir=resdir,
#                init=init,
#            )
#            restart.set_shared_config(config, link=config_filename)
#            component.add_task(restart)
#
#            threads = Threads(
#                component=component,
#                resolution=resolution,
#                indir=resdir,
#                init=init,
#            )
#            threads.set_shared_config(config, link=config_filename)
#            component.add_task(threads)

from test_utils.RunSpecs import RunSpecs
from test_utils.RunExecutor import RunExecutor

from test_utils.common import find_file_in_dir
from os.path import *
import shutil

l = ['/Users/m/Demo/CC3D_3.7.6/cc3d_test.command','/Users/m/Demo/CC3D_3.7.6/Demos/Models/cellsort/cellsort_2D/cellsort_2D.cc3d']
common_pref =  commonprefix(l)

for p in l:
    print relpath(p,common_pref)

cc3d_projects = find_file_in_dir('/Users/m/Demo/CC3D_3.7.6/Demos','*.cc3d')
cc3d_projects_common_prefix = commonprefix(cc3d_projects)

rs = RunSpecs()

rs.run_command = '/Users/m/Demo/CC3D_3.7.6/cc3d_test.command'
rs.cc3d_project = ''
rs.num_steps = 100
rs.test_output_root = '/Users/m/cc3d_tests'
rs.test_output_dir = ''

# clean test_output_dir
try:
    shutil.rmtree(rs.test_output_root)
except OSError:
    pass

error_runs = []

for i, cc3d_project in enumerate(cc3d_projects):

    rs.cc3d_project = cc3d_project
    rs.test_output_dir = relpath(cc3d_project, cc3d_projects_common_prefix)
    run_executor = RunExecutor(run_specs=rs)
    run_executor.run()
    run_status = run_executor.get_run_status()
    if run_status:
        error_runs.append((rs.cc3d_project,run_status))

    if i > 10:
        break

    # break

if not len(error_runs):
    print()
    print('-----------------ALL SIMULATIONS RUN SUCCESSFULLY----------------------')
    print()

else:
    print()
    print('-----------------THERE WERE ERRORS IN THE SIMULATIONS----------------------')
    print()

    for error_run in error_runs:
        print (error_run)

# run_executor = RunExecutor(run_specs=rs)
# run_executor.run()

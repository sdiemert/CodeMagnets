from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [], include_files=['data.csv', 'color_data.csv'])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('app.py', base=base, targetName = 'CodeMagnets')
]

setup(name='CodeMagnets',
      version = '1.0',
      description = '',
      options = dict(build_exe = buildOptions),
      executables = executables)

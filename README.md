# CodeMagnets

A fun project.

# Creating Executable

To create an executable version of application use cx\_freeze, a utility for packaging python applications as standalones executables.

1. `cd src`
2. `rm -rf build/ dist/` 
3. `cxfreeze-quickstart`
4. Follow prompts
5. `python setup.py bdist_mac` to build a mac OSX application, `python setup.py build` otherwise
6. The executable will be placed in: `./build/exec-<somestuff>/APPLICATION_NAME

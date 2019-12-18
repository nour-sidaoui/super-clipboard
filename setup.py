from setuptools import setup

APP = ['sc.py']
DATA_FILES = ['supercb_logo.icns']
OPTIONS = {'argv_emulation': False,
           'iconfile': 'supercb_logo.icns'}

setup(
    app=APP,
    name='Super Clipboard',
    version='0.2',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    license='Open source',
    author='Nour SIDAOUI',
    author_email='nour.sidaoui@gmail.com',
    setup_requires=['py2app'],
    install_requires=['pyperclip']
)

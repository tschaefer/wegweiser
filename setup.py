import os
import sys

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

if sys.argv[-1] == 'test':
	os.system('python tests.py')
	sys.exit()

setup(
	name = "wegweiser",
	version = "1.0.0",
	include_package_data = True,
	packages = ['wegweiser'],
	entry_points = {'console_scripts': ['wegweiser = wegweiser.__wegweiser__:main']},
	install_requires = ['simplekml >= 1.1', 'motionless >= 1.1' ],
	author = "Tobias Schäfer",
	author_email = "Tobias.Schaefer@blackox.org",
	url = "https://github.com/tschaefer/wegweiser/",
	description = "A pythonic geographic wikipedia spot scraper.",
	license = "BSD",
)

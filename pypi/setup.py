import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
  name = 'event-notifier',         # How you named your package folder (MyLib)
  packages=setuptools.find_packages(),
  version = '0.1.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Event notifier with many subscribers support',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Vitalij Gotovskij',               # Type in your name
  author_email = 'vitalij@cdeveloper.eu',     # Type in your E-Mail
  url = 'https://github.com/vitalij555/event-notifier',   # Provide either the link to your github or to your website
  # download_url = 'https://github.com/vitalij555/event-notifier/archive/v_0_1_1.tar.gz',
  keywords = ['EVENT', 'NOTIFY', 'SUBSCRIBE', "OBSERVER"],   # Keywords that define your package best
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
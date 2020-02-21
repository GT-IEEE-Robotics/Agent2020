from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "agent2020",
    version = "1.0.0",
    author = "GT IEEE Robotics",
    author_email = "ieee_president@gmail.com",
    description = ("The agent script to run the robot for the 2020 SoutheastCon robotics competition."),
    url = "https://github.com/GT-IEEE-Robotics/Agent2020",
    py_modules=['agent'],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    python_requires='>=3.5',
    install_requires=['argparse',
                      'pyyaml',
                      'simulator2020',
                      'interfaces2020',
                      'planning2020',
                      'vision2020',
                      'localization2020']
)

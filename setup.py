from setuptools import setup, find_packages
import os
import glob
import simple_notification
            
setup(name='Simple Notification',
      version=simple_notification.__version__,
      description='A simple notification system for Ubuntu-like platforms',
      author='Ryan McGuire',
      author_email='ryan@enigmacurry.com',
      url='http://www.enigmacurry.com',
      license='MIT',
      packages=["simple_notification"],
      package_data = {"simple_notification/icons": ["*"]},
      install_requires =["flask",
                         "argparse"],
      entry_points="""
      [console_scripts]
      simple_notification = simple_notification.main:main
      """
      )

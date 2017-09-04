from setuptools import setup, find_packages

version = '1.0.0'

setup(
    name="helga-repost",
    version=version,
    description=('tracks links and alerts if reposted'),
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='irc bot repost',
    author='Justin Caratzas',
    author_email='bigjust@lambdaphil.es',
    license='LICENSE',
    packages=find_packages(),
    include_package_data=True,
    py_modules=['helga_repost'],
    zip_safe=True,
    entry_points = dict(
        helga_plugins = [
            'repost = helga_repost:repost',
        ],
    ),
    install_requires = (
        'humanize',
    ),
)

from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = ''.join(f.readlines())

setup(
        name='twitterjk',
        version='0.4',
        description='Simple Twitter Wall console/web tool for querying tweets through Twitter API',
        long_description=long_description,
        author='Jakub Koza',
        author_email='kozajaku@fit.cvut.cz',
        keywords='twitter,CTU',
        license='Public Domain',
        url='https://github.com/kozajaku/MI-PYT',
        packages=find_packages(),
        include_package_data=True,
        classifiers=[
            'Environment :: Console',
            'Environment :: Web Environment',
            'Framework :: Flask',
            'Intended Audience :: Developers',
            'License :: Public Domain',
            'Operating System :: POSIX :: Linux',
            'Natural Language :: English',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3 :: Only',
            'Topic :: Internet :: WWW/HTTP :: WSGI'
        ],
        entry_points={
            'console_scripts': [
                'twitterjk = twitterjk.twitter:main',
            ],
        },
        install_requires=['Flask', 'click>=6', 'Jinja2', 'requests'],
        setup_requires=['pytest-runner'],
        tests_require=['pytest', 'flexmock', 'betamax'],
)

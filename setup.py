from setuptools import find_packages, setup

INSTALL_REQUIRES = [
    'flask==1.1.2',

    'flask-sqlalchemy==2.4.3',
    'sqlalchemy==1.3.7',

    'click==7.1.2',

    'markdown==2.6.9',
    'mdx-linkify==1.0',
]


if __name__ == '__main__':
    setup(
        version='0.1',
        name='MiniWiki',
        author='Nick, Oxygem',
        author_email='hello@oxygem.com',
        license='MIT',
        packages=find_packages(exclude=['tests']),
        entry_points={
            'console_scripts': (
                'miniwiki=miniwiki.__main__:start_miniwiki',
            ),
        },
        install_requires=INSTALL_REQUIRES,
        include_package_data=True,
    )

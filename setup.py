from setuptools import find_packages, setup

INSTALL_REQUIRES = [
    'cheroot==8.3.0',

    'flask==1.1.2',

    'flask-sqlalchemy==2.4.3',
    'sqlalchemy==1.3.7',

    'bcrypt==3.1.7',

    'click==7.1.2',

    'markdown==2.6.9',
    'mdx-linkify==1.0',
]

DEV_REQUIRES = [
    'wheel',
    'twine',
]


if __name__ == '__main__':
    setup(
        version='0.4',
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
        python_requires='>=3.6',
        install_requires=INSTALL_REQUIRES,
        extras_require={
            'dev': DEV_REQUIRES,
        },
        include_package_data=True,
    )

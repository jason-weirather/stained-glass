from setuptools import setup

setup(
    name="stained-glass",
    version="0.1.0",
    install_requires=[
        "Flask==1.1.4",
        "requests==2.26.0"
    ],
    packages=["stained_glass"],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'stained-glass=app:main',
        ],
    },
)


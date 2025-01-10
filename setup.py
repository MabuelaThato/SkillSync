from setuptools import setup

setup(
    name="skill_sync",
    version="1.0.0",
    py_modules=["skill_sync"],
    entry_points={
        "console_scripts": [
            "skill-sync=skill_sync:cli",
        ],
    },
)
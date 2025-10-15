from setuptools import setup, find_packages

setup(
    name="auto-deploy-agent-cli",
    version="1.0.0",
    description="A CLI tool to automatically detect, build, and deploy web projects",
    author="Auto Deploy Team",
    packages=find_packages(),
    install_requires=[
        # Add any required packages here
    ],
    entry_points={
        'console_scripts': [
            'deploy-agent=deploy_agent:main',
        ],
    },
    python_requires='>=3.6',
)
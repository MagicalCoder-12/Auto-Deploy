from setuptools import setup, find_packages

setup(
    name="auto-deploy-agent-cli",
    version="1.0.0",
    description="A CLI tool to automatically detect, build, and deploy web projects using AI recommendations",
    author="Auto Deploy Team",
    packages=find_packages(),
    install_requires=[
        "ollama>=0.1.0",
    ],
    entry_points={
        'console_scripts': [
            'deploy-agent=auto_deploy_agent_cli.deploy_agent:main',
        ],
    },
    python_requires='>=3.6',
)
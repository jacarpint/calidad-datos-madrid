import os
from setuptools import find_packages, setup

setup(
    name="madrid-opendata-connector",
    version="0.1.0",
    description="Custom connector for Madrid Open Data Portal integration with OpenMetadata",
    author="Javier Carpintero",
    author_email="jacarpint@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "frictionless>=5.0.0",
        "pydantic>=1.10.0",
    ],
    entry_points={
        "metadata.ingestion.source": [
            "connector = connector.madrid_connector:MadridOpenDataConnector",
        ],
    },    
    python_requires=">=3.8"
)

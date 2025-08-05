from setuptools import setup, find_packages

setup(
    name="numbers-backend",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.0",
        "uvicorn[standard]==0.24.0",
        "sqlalchemy==2.0.23",
        "pydantic==2.5.0",
        "passlib[bcrypt]==1.7.4",
        "python-jose[cryptography]==3.3.0",
        "python-multipart==0.0.6",
        "python-dotenv==1.0.0",
    ],
) 
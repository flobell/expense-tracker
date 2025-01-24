from setuptools import setup, find_packages

setup(
    name="expense-tracker",
    version="1.0.0",
    description="A simple expense tracker CLI "
    "application to manage your finances.",
    packages=find_packages(),
    install_requires=None,
    author="Pedro Flores",
    author_email="manuelflores1795@gmail.com",
    url="https://github.com/flobell/expense-tracker.git",
    py_modules=["src"],
    entry_points={
        'console_scripts': [
            'expense-tracker=main:main',
        ],
    },
    tests_require=[
        "unittest",
    ],
    python_requires=">=3.9",
)

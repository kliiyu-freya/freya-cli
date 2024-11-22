from setuptools import setup, find_packages

setup(
    name='freya-cli',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click>=8.1.7',  # CLI framework
    ],
    entry_points={
        'console_scripts': [
            'freya=freya_cli.cli:cli',
        ],
    },
    author='Kliiyu',
    author_email='kliiyu@example.com',
    description='CLI tool for Freya home automation system',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kliiyu-freya/cli',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='mkdocs-pyscript',
    version='0.0.1',
    description='Add PyScript to your mkdocs site',
    long_description= long_description,
    long_description_content_type='text/markdown',
    keywords=['mkdocs', 'pyscript'],
    url='https://github.com/jeffersglass/mkdocs-pyscript',
    author='Jeff Glass',
    author_email='mail@jeff.glass',
    license='APACHE',
    python_requires='>=3.8',
    install_requires=[
        'mkdocs>=1.4.0',
        'beautifulsoup4>=4.1',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'mkdocs-pyscript = mkdocs_pyscript.plugin:Plugin'
        ]
    },
    include_package_data=True,
)
from setuptools import setup, find_packages

setup(
    name='mkdocs-pyscript',
    version='0.1.0',
    description='Add PyScript to your mkdocs site',
    long_description='',
    keywords='mkdocs','pyscript'
    url='https://github.com/jeffersglass/mkdocs-pyscript',
    author='Jeff Glass',
    author_email='mail@jeff.glass',
    license='APACHE',
    python_requires='>=3.7',
    install_requires=[
        'mkdocs>=1.0.4'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8'
        'Programming Language :: Python :: 3.9'
        'Programming Language :: Python :: 3.10'
        'Programming Language :: Python :: 3.11'
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'mkdocs-pyscript = mkdocs-pyscript.plugin:YourPlugin'
        ]
    }
)
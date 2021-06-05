import setuptools


setuptools.setup(
    name='cotrace',
    version='1.0.0',
    author='RimoChan',
    author_email='the@librian.net',
    description='cotrace',
    long_description=open('readme.md', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/RimoChan/cotrace',
    packages=['cotrace'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

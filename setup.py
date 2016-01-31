from setuptools import setup

setup(name='facade',
      version='0.1.1',
      description='Meta loaders for fun and profit',
      url='http://github.com/oakfang/facade',
      author='Alon Niv',
      install_requires=[
        'jiphy==1.2.1',
        'PyYAML==3.11'
      ],
      author_email='oakfang@gmail.com',
      license='MIT',
      packages=['facade'],
      zip_safe=False)
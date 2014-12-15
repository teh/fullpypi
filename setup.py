from setuptools import setup, find_packages


if __name__ == '__main__':
    setup(
        name='fullpypi',
        version='0.1',
        description='build all of pypi',
        keywords='pypi',
        author='Tom',
        author_email='tehunger@gmail.com',
        url='https://github.com/teh',
        license='BSD',
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        scripts=[
            'dep_extraction/extract_imports.py'
        ],
    )

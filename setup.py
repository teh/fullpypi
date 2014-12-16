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
            'dep_extraction/extract_imports.py',
            'dep_extraction/prefetch_all.py',
            'dep_extraction/fullpypi_dump_meta.py',
            'nix_writer/write_extractor_builder.py',
        ],
        package_data={
            'dep_extraction': ['known_names.protobuf',
                               'pypi-sdists-2014-12-14.h5'],
        },
        data_files=[
            ('nix', ['nix_writer/extract_imports_expression.nix']),
        ]
    )

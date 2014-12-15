"""
Exract a list of all known pypi names and store in a proto.
"""
import pandas
import dep_meta_pb2

if __name__ == '__main__':
    s = pandas.HDFStore('/tmp/pypi-2014-12-14.h5')
    names = dep_meta_pb2.KnownNames(
        names=sorted(set(s['package_df'].pypi_name) | set(s['package_df'].name))
    )
    with open('./dep_extraction/known_names.protobuf', 'w') as f:
        f.write(names.SerializeToString())

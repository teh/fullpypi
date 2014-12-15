"""
Exract a list of all known pypi names and store in a proto.
"""
import pandas
import dep_meta_pb2
import subprocess

if __name__ == '__main__':
    # All known names in pypi.
    s = pandas.HDFStore('/tmp/pypi-2014-12-14.h5')
    names = dep_meta_pb2.KnownNames(
        names=sorted(set(s['package_df'].pypi_name) | set(s['package_df'].name))
    )
    with open('./dep_extraction/known_names.protobuf', 'w') as f:
        f.write(names.SerializeToString())

    # What versions shall we download / build?
    version_df = s['version_df']
    sdist_df = version_df[version_df.packagetype == 'sdist'].groupby(
        ['pypi_name', 'version']).max().reset_index()

    s_out = pandas.HDFStore('dep_extraction/pypi-sdists-2014-12-14.h5', mode='w')
    s_out.put('sdist_df', sdist_df, compression='zlib')
    s_out.close()

with import <nixpkgs> {};
with pythonPackages;

buildPythonPackage {
  name = "fullpyi";
  propagatedBuildInputs = [
    setuptools
    protobuf
    nose
  ];
}

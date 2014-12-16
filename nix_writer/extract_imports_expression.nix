with import <nixpkgs> {};
let
extractImports = { sha256, url, name } : stdenv.mkDerivation {
  name = name;
  buildInputs = [ pkgs.unzip ];
  srcs = pkgs.fetchurl {
    url = url;
    sha256 = sha256;
  };
  phases = "unpackPhase buildPhase";
  buildPhase = ''
    mkdir $out
    # sourcing required because fullpypi (which provides
    # extract_imports.py) gets installed as a system package:
    source /etc/profile
    extract_imports.py . $out/import_meta.protobuf
  '';
};

in
builtins.derivation {
  name = "tld";
  pkgs = import ./extract.nix { inherit extractImports; };
}

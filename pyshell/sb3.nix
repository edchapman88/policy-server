# toolz.nix
{
  lib,
  buildPythonPackage,
  fetchPypi,
  setuptools,
  wheel,
  numpy,
  gymnasium,
  torch,
  cloudpickle,
  pandas,
  matplotlib,
}:

buildPythonPackage rec {
  pname = "stable_baselines3";
  version = "2.6.0";

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-ly71N6mo8rneBs3Kh+8fM99fyCOc/mT+2Il218eZwvc=";
  };

  # do not run tests
  doCheck = false;

  # specific to buildPythonPackage, see its reference
  pyproject = true;
  build-system = [
    setuptools
    wheel
  ];

  dependencies = [
    numpy
    gymnasium
    torch
    cloudpickle
    pandas
    matplotlib
  ];
}

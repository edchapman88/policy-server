# shell.nix
let
  pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/3a993d32444337caa4db6b85580d83825d6f596b.tar.gz") {};

  python = pkgs.python3.override {
    self = python;
    packageOverrides = pyfinal: pyprev: {
      stable-baselines3 = pyfinal.callPackage ./sb3.nix { };
    };
  };

in pkgs.mkShell {
  packages = [
    (python.withPackages (python-pkgs: [
      # select Python packages here
      python-pkgs.gymnasium
      python-pkgs.numpy
      python-pkgs.stable-baselines3
    ]))
  ];
}

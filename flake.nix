{
  description = "Fast downwards for planning research";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    inputs:
    let
      supportedSystems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      forEachSupportedSystem =
        f:
        inputs.nixpkgs.lib.genAttrs supportedSystems (
          system:
          f {
            pkgs = import inputs.nixpkgs {
              inherit system;
              config.allowUnfree = true;
            };
          }
        );
    in
    {
      devShells = forEachSupportedSystem (
        { pkgs }:
        {
          default =
            pkgs.mkShell.override
              {
                # Override stdenv in order to change compiler:
                # stdenv = pkgs.clangStdenv;
              }
              {

                inputsFrom = [ (pkgs.callPackage ./default.nix { }) ];
                packages =
                  with pkgs;
                  [
                    # (callPackage ./default.nix { })
                    clang-tools
                    cmake
                    cppcheck
                    uncrustify
                    mprocs
                    entr
                    # codespell
                    # gtest
                    # lcov
                    # vcpkg
                    # vcpkg-tool

                    python3
                    uv
                    gmp
                    soplex
                    # cplex
                  ]
                  ++ (if system == "aarch64-darwin" then [ ] else [ gdb ]);
                env = {
                  DOWNWARD_REPO = "/data/Software/bachelor-fast-downwards/decoupling";
                  DOWNWARD_BENCHMARKS = "/data/Software/bachelor-benchmarks"; # Adapt path

                  UV_PYTHON_DOWNLOADS = "never";
                  UV_PYTHON = pkgs.python3.interpreter;
                  LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath pkgs.pythonManylinuxPackages.manylinux1;
                };

                shellHook = ''
                  unset PYTHONPATH
                  export PATH=$PATH:/data/Software/bachelor-plan-validator/validate
                '';

              };
        }
      );

      # packages = forEachSupportedSystem (
      #   { pkgs }:
      #   {
      #     default = pkgs.callPackage ./package.nix { };
      #     clang = pkgs.callPackage ./package.nix { stdenv = pkgs.clangStdenv; };
      #   }
      #   // pkgs.lib.optionalAttrs (system != "x86_64-linux") {
      #     crossIntel = pkgs.pkgsCross.gnu64.callPackage ./package.nix {
      #       enableTests = false;
      #     };
      #   }
      #   // pkgs.lib.optionalAttrs (system != "aarch64-linux") {
      #     crossAarch64 = pkgs.pkgsCross.aarch64-multiplatform.callPackage ./package.nix {
      #       enableTests = false;
      #     };
      #   }
      # );
      #
      #       checks = config.packages // {
      #         clang = config.packages.default.override {
      #           stdenv = pkgs.clangStdenv;
      #         };
      #       };
      #     };
      # };
    };
}

{
  lib,
  stdenv,
  fetchFromGitHub,
  cmake,
  python3,
  bear,
  gnumake,
  gcc_multi,
  nix-update-script,
}:

stdenv.mkDerivation (finalAtrs: {
  pname = "val";
  version = "unstable-2021-10-18";

  src = fetchFromGitHub {
    owner = "KCL-Planning";
    repo = "VAL";
    rev = "3c7a1f330bdab0ba28a4762bb45c3f06c27fb6d4";
    hash = "sha256-23+N7FbAKH2Bd3SUm4SKtj0lJBs1tmjsZ1KchAkjv4M=";
  };

  buildInputs = [
    python3
    bear
    gnumake
  ];
  nativeBuildInputs = [
    cmake
    bear
    gcc_multi
    gnumake
    python3
  ];

  passthru.updateScript = nix-update-script { };

  meta = {
    description = "The plan validation system";
    homepage = "https://github.com/KCL-Planning/VAL";
    license = lib.licenses.bsd3;
    maintainers = with lib.maintainers; [ LazilyStableProton ];
    mainProgram = "val";
    platforms = lib.platforms.all;
  };
})

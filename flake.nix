# Copyright © 2026 Mindclade, LLC. All Rights Reserved.
# Mindclade Proprietary and Confidential.
# SPDX-License-Identifier: LicenseRef-Mindclade-Proprietary

{
  description = "Hermetic validation for the mindclade .github-private repository";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs =
    { self, nixpkgs }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "aarch64-darwin"
        "x86_64-darwin"
      ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
      perSystem =
        system:
        let
          pkgs = import nixpkgs { inherit system; };
          validationPackages = with pkgs; [
            actionlint
            gnumake
            python3
            shellcheck
            yamllint
          ];
          ciShell = pkgs.mkShell {
            packages = validationPackages;
          };
          repositoryCheck = pkgs.runCommand "mindclade-github-private-validation" {
            nativeBuildInputs = validationPackages;
            src = self;
          } ''
            cp -R "$src" source
            chmod -R u+w source
            cd source
            make validate
            make lint
            touch "$out"
          '';
        in
        {
          inherit ciShell pkgs repositoryCheck;
        };
    in
    {
      devShells = forAllSystems (system: {
        ci = (perSystem system).ciShell;
        default = (perSystem system).ciShell;
      });

      checks = forAllSystems (system: {
        ci-shell = (perSystem system).ciShell;
        repository = (perSystem system).repositoryCheck;
      });

      formatter = forAllSystems (system: (perSystem system).pkgs.nixfmt);
    };
}

{
  description = "Application packaged using poetry2nix";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.11";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    poetry2nix,
  }: let
    studlanVersion =
      if (self ? shortRev)
      then self.shortRev
      else "dev";
  in
    {
      # Nixpkgs overlay providing the application
      overlay = nixpkgs.lib.composeManyExtensions [
        poetry2nix.overlay
        (final: prev: let
          studlanOverrides = prev.poetry2nix.defaultPoetryOverrides.extend (self: super: {
            django-markdown-deux = super.django-markdown-deux.overridePythonAttrs (
              old: {
                buildInputs = (old.buildInputs or []) ++ [self.setuptools];
              }
            );

            beautifulsoup4 = super.beautifulsoup4.overridePythonAttrs (
              old: {
                buildInputs = (old.buildInputs or []) ++ [self.setuptools];
              }
            );

            pychallonge = super.pychallonge.overridePythonAttrs (
              old: {
                buildInputs = (old.buildInputs or []) ++ [self.setuptools];
              }
            );

            django-postman = super.django-postman.overridePythonAttrs (
              old: {
                buildInputs = (old.buildInputs or []) ++ [self.setuptools];
              }
            );
          });
        in {
          studlan = prev.poetry2nix.mkPoetryApplication {
            projectDir = ./.;
            overrides = studlanOverrides;
          };

          studlanEnv = prev.poetry2nix.mkPoetryEnv {
            projectDir = ./.;
            overrides = studlanOverrides;
          };
        })
      ];
    }
    // (flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {
        inherit system;
        overlays = [self.overlay];
      };

      studlanDocker = pkgs.dockerTools.buildLayeredImage {
        name = "studlan";
        tag = studlanVersion;
        contents = [pkgs.studlan pkgs.uwsgi];
        config.Entrypoint = [(pkgs.studlan + "/bin/studlan")];
      };
    in {
      apps = {
        inherit (pkgs) studlan;
      };

      defaultApp = pkgs.studlan;

      # `nix build`
      packages = with pkgs; {
        inherit studlan;
        inherit studlanDocker;
      };
      defaultPackage = pkgs.studlan;

      devShell = pkgs.mkShell {
        buildInputs = with pkgs; [
          studlanEnv

          (python310.withPackages (ps:
            with ps; [
              poetry
              pylama
              black
              jedi-language-server
              pylsp-mypy
            ]))
        ];
      };
    }));
}

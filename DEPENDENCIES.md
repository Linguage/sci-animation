# Dependencies

This file lists the minimal dependencies needed to run and render this Manim project on another machine.

## Python

- Python >= 3.11
- Project Python packages from [pyproject.toml](pyproject.toml):
  - `manim>=0.19.0`
  - `numpy>=2.0.0`

Install:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
```

## Manim Runtime Tools

Required command-line tools:

- `latex`
- `dvisvgm`
- `ffmpeg`

Manim may also require Cairo and Pango on a fresh system.

## TeX Packages

The current scene uses `MathTex` and `DecimalNumber`, so TeX support is required.

Required TeX packages observed for this project:

- `standalone`
- `preview`

Install small missing TeX packages with user-mode `tlmgr`:

```bash
tlmgr init-usertree
tlmgr --usermode install standalone preview
```

## dvisvgm

On this machine, BasicTeX was already present but `dvisvgm` was missing. To avoid installing a full TeX distribution, the project uses only the TeX Live `dvisvgm` binary package in the local virtual environment:

- `.venv/bin/dvisvgm`
- `.venv/bin/dvisvgm-real`

Equivalent minimal source package:

```text
https://ctan.math.utah.edu/ctan/tex-archive/systems/texlive/tlnet/archive/dvisvgm.universal-darwin.tar.xz
```

For other platforms, use the matching TeX Live archive package for the target architecture, or install `dvisvgm` through the system package manager only if it does not pull a full TeX distribution unexpectedly.

## Verification

```bash
.venv/bin/dvisvgm --version
.venv/bin/manim -ql scenes/crank_rocker.py CrankRockerScene
```

Expected output video:

```text
media/videos/crank_rocker/480p15/CrankRockerScene.mp4
```


from __future__ import annotations

import os
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]


def require_tex_toolchain() -> None:
    local_bin_paths = [ROOT / ".venv" / "bin", ROOT / ".tools" / "bin"]
    path_entries = os.environ.get("PATH", "").split(os.pathsep)
    for path in reversed(local_bin_paths):
        path_text = str(path)
        if path.exists() and path_text not in path_entries:
            os.environ["PATH"] = path_text + os.pathsep + os.environ.get("PATH", "")

    missing = [tool for tool in ("latex", "dvisvgm") if shutil.which(tool) is None]
    if not missing:
        return

    missing_list = ", ".join(missing)
    raise RuntimeError(
        "This scene uses MathTex/DecimalNumber, so Manim needs the TeX toolchain. "
        f"Missing executable(s): {missing_list}. Install or expose them on PATH, "
        "then rerun Manim."
    )


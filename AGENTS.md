# Agent Notes

- This project uses Manim for science and mechanical mechanism animations.
- Treat LaTeX as part of the project runtime. If Manim rendering fails because a small TeX package or class is missing, prefer installing it with `tlmgr --usermode` instead of rewriting the scene to avoid TeX.
- Do not install a full TeX distribution, large Homebrew dependency chain, or heavyweight binary tool such as a Homebrew `texlive` pull without explicit user confirmation. If a missing TeX binary cannot be installed lightly, document the dependency and stop.
- Prefer `MathTex`, `Tex`, and Manim numeric text helpers when they improve the animation's clarity.
- For GitHub-readable reports, prefer tracked GIF previews in `media/previews/*.gif` plus links to the corresponding mp4. Do not rely on inline `<video>` tags in Markdown reports, because GitHub does not reliably render repository mp4 files as embedded players.

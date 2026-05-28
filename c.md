# sci-animation c.md

## 常用运行命令

```bash
source .venv/bin/activate
python -m pip install -e .
manim -ql scenes/crank_rocker.py CrankRockerScene
manim -pqh scenes/crank_rocker.py CrankRockerScene
manim -ql scenes/spring_oscillator.py SpringOscillatorScene
manim -pqh scenes/spring_oscillator.py SpringOscillatorScene
manim -ql scenes/three_story_earthquake.py ThreeStoryEarthquakeScene
manim -pqh scenes/three_story_earthquake.py ThreeStoryEarthquakeScene
manim -ql scenes/replay_time_response.py ReplayTimeResponseScene
manim -ql scenes/monte_carlo_pi.py MonteCarloPiScene
manim -pqh scenes/monte_carlo_pi.py MonteCarloPiScene
manim -ql scenes/galton_board.py GaltonBoardScene
manim -pqh scenes/galton_board.py GaltonBoardScene
```

## 依赖检查

```bash
.venv/bin/dvisvgm --version
latex --version
ffmpeg -version
```

## Replay 示例检查

```bash
PYTHONPATH=src .venv/bin/python - <<'PY'
from sci_animation.replay import read_time_response_csv
response = read_time_response_csv(
    "examples/replay/three_story_sample.csv",
    units={"u1": "m", "u2": "m", "u3": "m"},
)
print(response.duration(), sorted(response.values))
PY
```

## 结果路径

- 低质量视频：`media/videos/crank_rocker/480p15/CrankRockerScene.mp4`
- 弹簧振子低质量视频：`media/videos/spring_oscillator/480p15/SpringOscillatorScene.mp4`
- 三层楼地震响应低质量视频：`media/videos/three_story_earthquake/480p15/ThreeStoryEarthquakeScene.mp4`
- CSV replay 低质量视频：`media/videos/replay_time_response/480p15/ReplayTimeResponseScene.mp4`
- 蒙特卡罗估计 pi 低质量视频：`media/videos/monte_carlo_pi/480p15/MonteCarloPiScene.mp4`
- 高尔顿板低质量视频：`media/videos/galton_board/480p15/GaltonBoardScene.mp4`
- Manim 缓存：`media/`

## 常看目录

- `scenes/`：Manim 动画场景。
- `src/mechanisms/`：机构几何求解。
- `docs/specs/`：蓝图、架构、路线图。
- `DEPENDENCIES.md`：跨设备依赖清单。

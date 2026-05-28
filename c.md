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
```

## 依赖检查

```bash
.venv/bin/dvisvgm --version
latex --version
ffmpeg -version
```

## 结果路径

- 低质量视频：`media/videos/crank_rocker/480p15/CrankRockerScene.mp4`
- 弹簧振子低质量视频：`media/videos/spring_oscillator/480p15/SpringOscillatorScene.mp4`
- 三层楼地震响应低质量视频：`media/videos/three_story_earthquake/480p15/ThreeStoryEarthquakeScene.mp4`
- Manim 缓存：`media/`

## 常看目录

- `scenes/`：Manim 动画场景。
- `src/mechanisms/`：机构几何求解。
- `docs/specs/`：蓝图、架构、路线图。
- `DEPENDENCIES.md`：跨设备依赖清单。

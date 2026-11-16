#!/usr/bin/env python3
"""Static delivery audit for a generated Remotion video project."""

from __future__ import annotations

import argparse
import json
import wave
from pathlib import Path


REQUIRED_FILES = (
    "package.json",
    "README.md",
    "tools/make_audio.py",
    "public/soundtrack.wav",
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def audit(project: Path) -> list[str]:
    errors: list[str] = []
    warnings: list[str] = []

    for relative in REQUIRED_FILES:
        if not (project / relative).is_file():
            fail(errors, f"missing required file: {relative}")

    package_path = project / "package.json"
    if package_path.is_file():
        try:
            package = json.loads(package_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            fail(errors, f"cannot read package.json: {exc}")
        else:
            scripts = package.get("scripts", {})
            for name in ("dev", "build"):
                if name not in scripts:
                    fail(errors, f"package.json missing npm script: {name}")

            dependencies = package.get("dependencies", {})
            dev_dependencies = package.get("devDependencies", {})
            remotion = dependencies.get("remotion") or dev_dependencies.get(
                "remotion"
            )
            if not remotion:
                fail(errors, "package.json has no remotion dependency")
            elif not str(remotion).lstrip("^~>=< ").startswith("4."):
                fail(errors, f"expected Remotion v4, found {remotion!r}")

            engines = package.get("engines", {})
            if "node" not in engines:
                warnings.append("package.json does not declare engines.node >=18")

    audio_path = project / "public/soundtrack.wav"
    if audio_path.is_file():
        try:
            with wave.open(str(audio_path), "rb") as audio:
                channels = audio.getnchannels()
                sample_rate = audio.getframerate()
                sample_width = audio.getsampwidth()
                frames = audio.getnframes()
                seconds = frames / sample_rate if sample_rate else 0
                if channels not in (1, 2):
                    warnings.append(f"unexpected WAV channel count: {channels}")
                if sample_width != 2:
                    warnings.append(
                        f"expected 16-bit PCM WAV, got {sample_width * 8}-bit"
                    )
                if sample_rate < 44_100:
                    warnings.append(
                        f"low sample rate for delivery: {sample_rate} Hz"
                    )
                if seconds <= 0:
                    fail(errors, "soundtrack.wav has no audio frames")
        except (wave.Error, OSError) as exc:
            fail(errors, f"cannot inspect soundtrack.wav: {exc}")

    make_audio = project / "tools/make_audio.py"
    if make_audio.is_file():
        source = make_audio.read_text(encoding="utf-8", errors="replace")
        if "numpy" not in source:
            warnings.append("tools/make_audio.py does not appear to use NumPy")
        if "soundtrack.wav" not in source:
            warnings.append("tools/make_audio.py does not mention soundtrack.wav")

    readme = project / "README.md"
    if readme.is_file():
        text = readme.read_text(encoding="utf-8", errors="replace")
        for term, label in (
            ("make_audio.py", "audio regeneration command"),
            ("public/soundtrack.wav", "WAV output path"),
            ("文案", "copy editing instructions"),
        ):
            if term not in text:
                warnings.append(f"README does not mention {label}")

    cache_dirs = [
        path
        for path in project.rglob("*")
        if path.is_dir() and path.name in {"node_modules", ".remotion"}
    ]
    if cache_dirs:
        warnings.append("project contains install or render caches; exclude them from zip")

    print(f"Project: {project}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARN: {message}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="Generated Remotion project root")
    args = parser.parse_args()
    project = args.project.resolve()
    if not project.is_dir():
        parser.error(f"not a directory: {project}")
    return 1 if audit(project) else 0


if __name__ == "__main__":
    raise SystemExit(main())

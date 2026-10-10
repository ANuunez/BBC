# Building BBC from source

This document is for developers and contributors. **End users should download `BBC.exe` from a GitHub Release instead.**

## Requirements

- Windows 10/11 64-bit
- Python 3.12 or compatible supported version
- Internet access for downloading build dependencies

These requirements apply only to the machine that builds BBC. They are **not required by people who download the finished `BBC.exe`**.

## Local build

From the repository root, run:

```bat
build.bat
```

The resulting executable is:

```text
dist\BBC.exe
```

The build uses PyInstaller to bundle the Python interpreter and required libraries into the executable.

## GitHub Actions

The repository includes `.github/workflows/build.yml`. GitHub Actions runs the build on a Windows runner and produces `BBC.exe` as an artifact. When a GitHub Release is published, the workflow also attaches the executable to that release.

## Important

Do not commit build output such as `dist/`, `build/`, or local Python caches. The repository's `.gitignore` already excludes these files.

# Best BongoCat Clicker (BBC)

A lightweight Windows macro utility designed for **BongoCat**. BBC automates configurable keyboard and mouse actions while keeping a safety check on the selected BongoCat window.

> **Status:** Early development / testing. The project may change between releases.

## Download

Download **`BBC.exe`** from the latest [GitHub Release](../../releases).

BBC is distributed as a standalone Windows executable. **End users do not need to install Python or any Python libraries.**

### Windows SmartScreen

Because community-built releases may not have a commercial code-signing certificate, Windows can sometimes show a SmartScreen warning. If this happens, verify that you downloaded `BBC.exe` from the project's official GitHub Release and inspect the source code before choosing to run it.

## What BBC does

- Automates keyboard keys such as `A`, `S`, and `D`.
- Supports mouse actions such as `LEFT_CLICK` and `RIGHT_CLICK`.
- Uses configurable delays and key/click hold times in milliseconds.
- Uses `F8` as the default toggle key.
- Lets you choose the BongoCat target window.
- Can stop automatically when the target window loses focus.
- Saves your settings between launches.
- Supports automatic Windows language detection.
- Supports English, Portuguese, Spanish, French, German, Simplified Chinese, Japanese, Korean, Italian, Dutch, Polish, and Russian.
- Supports automatic, dark, and light themes.
- Uses a custom Windows application icon.

## Quick start

1. Download `BBC.exe` from **Releases**.
2. Put it somewhere convenient, such as your Desktop or a dedicated `BBC` folder.
3. Start **BongoCat**.
4. Open `BBC.exe`.
5. Check the target window in **Settings**. It should normally be `BongoCat`.
6. Leave **Stop if BongoCat loses focus** enabled for the safest default behaviour.
7. Press **Start** in BBC, or press the configured toggle key (`F8` by default).
8. Keep the BongoCat window active while the macro is running.
9. Press `F8` again, or use **Stop**, to stop the macro.

## Configuration

Open **Settings** to configure BBC.

### Language

Choose a language manually or use **Automatic (PC)**. Automatic mode reads the Windows user locale and selects a supported language when possible.

### Theme

- **Automatic (PC):** follows the Windows app theme.
- **Dark:** dark interface.
- **Light:** light interface.

### Toggle key

The default toggle key is `F8`. Change it if another application already uses that key.

### Target window

BBC should target the actual **BongoCat** window, not the BBC application window. If BongoCat uses a different title, use **Select window** or enter its exact window title.

BBC's own executable is called `BBC.exe`; that name does not need to match BongoCat's window title.

### Actions

Enter actions separated by commas. For example:

```text
a, s, d
```

Mouse actions are also supported:

```text
LEFT_CLICK, RIGHT_CLICK
```

You can combine them, for example:

```text
a, s, d, LEFT_CLICK
```

### Timing

BBC uses a random value between the configured minimum and maximum for each delay. This allows you to avoid having every action occur at exactly the same interval.

- **Delay between actions:** time before the next action.
- **Key/click hold time:** how long a key or mouse button is held.

Values are measured in milliseconds (`ms`).

### Focus safety

When **Stop if BongoCat loses focus** is enabled, BBC checks that the selected BongoCat window is the active foreground window before sending an action. If you switch to another application, BBC stops instead of continuing to send the macro to that application.

This is enabled by default and is recommended.

## Where settings are stored

BBC stores its user configuration in:

```text
%APPDATA%\BBC\config.json
```

Deleting that file resets BBC's saved settings to their defaults.

## Troubleshooting

### BBC says that BongoCat was not found

- Make sure BongoCat is running.
- Check the target window title in **Settings**.
- Use **Select window** to choose the correct visible window.

### The macro stops immediately

Make sure BongoCat is the active window. If focus safety is enabled, BBC intentionally stops when another application becomes active.

### The toggle key does not work

Choose another key in Settings. Another application may already be using the selected global hotkey.

### Windows displays a security warning

Only download BBC from the project's official GitHub Releases page. Unsigned community executables can receive reputation-based warnings from Windows even when their source code is publicly available.

### Something does not work

Before opening an issue, check the project's existing Issues and make sure you are using the latest release. When reporting a bug, include:

- BBC version;
- Windows version;
- what you expected to happen;
- what actually happened;
- your relevant settings;
- steps to reproduce the problem.

Do not post passwords, tokens, private files, or other sensitive information in an issue.

## Open source

BBC is open source. The source code is available in this repository so users can inspect how the application works and contributors can propose improvements.

Pull requests, bug reports, translations, documentation improvements, and other constructive contributions are welcome.

## Building from source

Building the project yourself is intended for developers and contributors. The normal end-user download does **not** require Python.

See [`BUILDING.md`](BUILDING.md) for developer build instructions.

## License

BBC is released under the **MIT License**. See [`LICENSE`](LICENSE) for the full text.

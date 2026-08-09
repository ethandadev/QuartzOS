<h1 align="center">Quartz OS</h1>

<p align="center">
  <a href="https://github.com/ethandadev/QuartzOS" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white" alt="GitHub">
  </a>
  <a href="https://www.youtube.com/@ethandadev" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/YouTube-FF0000?logo=youtube&logoColor=white" alt="YouTube">
  </a>
  <a href="https://buymeacoffee.com/ethandadev" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?logo=buymeacoffee&logoColor=black" alt="Buy Me a Coffee">
  </a>
  <a href="https://ethandadev.com" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/Website-4285F4?logo=googlechrome&logoColor=white" alt="Website">
  </a>
  <br>
  <a href="./LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-4CAF50?logo=opensourceinitiative&logoColor=white" alt="MIT License">
  </a>
  <img src="https://img.shields.io/badge/Platform-macOS-000000?logo=apple&logoColor=white" alt="macOS">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white" alt="Python">
  <br>
  <a href="https://github.com/ethandadev/QuartzOS">
    <img src="https://img.shields.io/github/stars/ethandadev/QuartzOS?style=flat&logo=github" alt="GitHub stars">
  </a>
</p>

> macOS, but make it weird.

Quartz is a custom desktop environment built in Python with Pygame and PyObjC.
It takes real macOS application windows, pulls them into its own interface,
and lets you interact with them as if they were running inside a completely
different operating system.

Under the hood, Quartz uses Apple's ScreenCaptureKit to capture windows and
forwards your mouse clicks and keyboard input back to the real applications.
So while the desktop looks and feels different, your macOS apps keep working
normally.

I started Quartz because I was bored of the usual macOS desktop and wanted to
see how far I could push the idea of building a second desktop on top of the
first one. It is part experiment, part game, and part “what if macOS worked
like this instead?”

Built by [@ethandadev](https://github.com/ethandadev).

## What is Quartz?

- A custom desktop environment layered on top of macOS.
- Written in Python.
- Rendered with Pygame.
- Connected to macOS through PyObjC.
- Powered by real macOS application windows.
- Still very much a work in progress.

> [!NOTE]
> Quartz is experimental software. Expect bugs, strange behavior, unfinished
> features, and possibly a desktop that does something you definitely did not
> ask it to do.

## Legal Notice
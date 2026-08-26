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
  <a href="./LICENSE.md">
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


Quartz OS is a custom desktop enviorment built in Python with Pygame and PyObjC. It can take a real macOS app window, put it into our own interface, then lets you still interact with the application as if you were in a whole different operating system. This also has added benefits such as having more customizability, being able to build your own "Settings" app or whatever.


Under the hood, Quartz OS uses Apple's own ScreenCaptureKit api to capture windows and forwards your mouse and keyboard inputs back to the real applications. So while the desktop looks and feels different, your macOS apps keep working normally.


I started Quartz OS because I became bored of the usual macOS desktop and I had an itch on working on a big project, so then I started planning and I came up with this idea. I decided to use Python and Pygame as I have alot of experience with them but to keep it still very smooth and optimized, most of the heavy lifting is done through C-backed framework calls.

Built by [@ethandadev](https://github.com/ethandadev).

## What is Quartz?

- A custom desktop environment layered on top of macOS.
- Written in Python.
- Rendered with Pygame.
- Connected to macOS through PyObjC.
- Powered by real macOS application windows.
- Still very much a work in progress.

> [!NOTE]
> Quartz OS is experimental software. Expect bugs, strange behavior, unfinished
> features, and possibly a desktop that does something you definitely did not
> ask it to do. 
> Quartz is also my own personal project, don't ask me to keep consistently updating,
> maintaining and fixing bugs for Quartz OS.

## How to use
> [!NOTE]
> As this is my personal project, I won't really provide in-depth documentation on how to use and troubleshoot Quartz OS, though I will be providing a simple how to get Quartz OS running.

As any other project, first download the source files as a zip onto your Desktop.

Then extract the contents of the zip and open a fresh terminal tab inside this new folder.

Execute this command in your terminal to install the required dependencies for this project.
`python3 -m venv venv && source venv/bin/activate && pip3 install -r requirements.txt`

Quartz also uses a small native Swift helper (`native/capture_helper.swift`) to work around a
confirmed pyobjc/ScreenCaptureKit bug (see comments in `core/capture_engine.py` for details).
Build it from source before running Quartz -- review the source first, then run:
`chmod +x native/build.sh && ./native/build.sh`

Finally to start the os execute this command `python3 start.py`

##### Enjoy!

---

## Legal Notice

> [!WARNING]
> Quartz OS requires macOS Screen Recording and Accessibility permissions. It
> captures application windows and forwards mouse and keyboard input to them.
> Review the source code carefully before granting these permissions.

Quartz is an independent, open-source project. It is not affiliated with,
endorsed by, or sponsored by Apple Inc. “Apple,” “macOS,” “ScreenCaptureKit,”
and other Apple product or service names are trademarks of Apple Inc.

Quartz is intended to be used only with applications, accounts, content, and
data that you own or are authorized to access. Do not use Quartz to monitor,
record, control, or interact with another person's device or data without
permission.

The software is provided “as is,” without warranties of any kind. To the
maximum extent permitted by applicable law, the authors and contributors are
not liable for data loss, privacy incidents, security issues, application
malfunctions, system instability, or other consequences resulting from the use
of Quartz.

This notice is not legal advice. See [`LICENSE`](./LICENSE.md) for the license
governing Quartz itself.

## Third-Party Software

Quartz uses third-party software distributed under its own licenses:

- `glcontext`
- `moderngl`
- `numpy`
- `psutil`
- `pygame-ce` — LGPL-2.1-or-later
- `pyobjc-core`
- `pyobjc-framework-Cocoa`
- `pyobjc-framework-CoreMedia`
- `pyobjc-framework-Quartz`
- `pyobjc-framework-ScreenCaptureKit`

See [`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md) for dependency
licenses and attribution information. Third-party packages, names, and
trademarks remain the property of their respective owners.

## License

Quartz is licensed under the [MIT License](./LICENSE.md).
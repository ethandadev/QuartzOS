# Third-Party Notices

Quartz includes or depends on the following third-party software. Each
dependency remains subject to its own license. The MIT License for Quartz does
not replace or modify these licenses.

## Runtime dependencies

| Package | Version | License | Project |
|---|---:|---|---|
| `glcontext` | 3.0.0 | MIT | [PyPI](https://pypi.org/project/glcontext/) |
| `moderngl` | 5.12.0 | MIT | [PyPI](https://pypi.org/project/moderngl/) |
| `numpy` | 2.5.2 | Verify package metadata | [PyPI](https://pypi.org/project/numpy/) |
| `psutil` | 7.2.2 | Verify package metadata | [PyPI](https://pypi.org/project/psutil/) |
| `pygame-ce` | 2.5.8 | LGPL-2.1-or-later | [PyPI](https://pypi.org/project/pygame-ce/) |
| `pyobjc-core` | 12.2.1 | MIT | [PyPI](https://pypi.org/project/pyobjc-core/) |
| `pyobjc-framework-Cocoa` | 12.2.1 | MIT | [PyPI](https://pypi.org/project/pyobjc-framework-Cocoa/) |
| `pyobjc-framework-CoreMedia` | 12.2.1 | MIT | [PyPI](https://pypi.org/project/pyobjc-framework-CoreMedia/) |
| `pyobjc-framework-Quartz` | 12.2.1 | MIT | [PyPI](https://pypi.org/project/pyobjc-framework-Quartz/) |
| `pyobjc-framework-ScreenCaptureKit` | 12.2.1 | MIT | [PyPI](https://pypi.org/project/pyobjc-framework-ScreenCaptureKit/) |

`glcontext` and ModernGL identify themselves as MIT-licensed, while
`pygame-ce` identifies itself as LGPL-2.1-or-later. [69][72][28]
The PyObjC ScreenCaptureKit package also identifies its metadata as MIT. [68]

## License information

The license terms for each dependency are available from the linked project
pages. When distributing a packaged version of Quartz, include the applicable
license texts and copyright notices with the distribution.

Third-party package names, trademarks, and copyrights belong to their
respective owners.

## Apple frameworks

Quartz uses macOS system frameworks, including:

- ScreenCaptureKit
- CoreMedia
- Quartz
- Cocoa

These frameworks are provided by Apple and are not included in Quartz's MIT
license. Quartz is not affiliated with, endorsed by, or sponsored by Apple Inc.
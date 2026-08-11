"""
core/permission_checks.py

Checks for the two macOS permissions Quartz needs:
  - Screen Recording (for ScreenCaptureKit)
  - Accessibility (for CGEventPost / CGEventTapCreate)

Both fail SILENTLY on macOS if not granted — no exception is raised.
That's why these checks exist: to turn "nothing happens, no error" into
a clear message you can actually act on.
"""

from ScreenCaptureKit import SCShareableContent
from ApplicationServices import AXIsProcessTrusted


def check_screen_recording_permission(callback):
    """
    Async check — hands (granted: bool, error_message: str | None) to callback.
    """
    def handler(content, error):
        if error is not None:
            callback(False, str(error))
        else:
            callback(True, None)

    SCShareableContent.getShareableContentWithCompletionHandler_(handler)


def check_accessibility_permission() -> bool:
    """
    Synchronous check — returns True/False immediately.

    AXIsProcessTrusted() is Apple's own direct answer to "does this
    process currently have Accessibility permission"
    """
    return bool(AXIsProcessTrusted())


def check_permissions_or_explain() -> bool:
    """
    The one function main.py should actually call. Prints clear,
    actionable instructions if either permission is missing.
    """
    accessibility_ok = check_accessibility_permission()

    # Screen Recording is async, so we need to run a tiny run loop to
    # actually get the callback's result before continuing.
    result = {"granted": None, "message": None}

    def on_result(granted, message):
        result["granted"] = granted
        result["message"] = message

    check_screen_recording_permission(on_result)

    from Quartz import CFRunLoopRunInMode, kCFRunLoopDefaultMode
    waited = 0.0
    while result["granted"] is None and waited < 3.0:
        CFRunLoopRunInMode(kCFRunLoopDefaultMode, 0.1, False)
        waited += 0.1

    screen_ok = bool(result["granted"])

    if screen_ok and accessibility_ok:
        return True

    print("Quartz needs two permissions to run:")
    if not screen_ok:
        print("  - Screen Recording: System Settings > Privacy & Security")
        print("    > Screen Recording > enable your terminal app (or PyCharm).")
    if not accessibility_ok:
        print("  - Accessibility: System Settings > Privacy & Security")
        print("    > Accessibility > enable your terminal app (or PyCharm).")
    print("After granting these, restart Quartz.")
    return False
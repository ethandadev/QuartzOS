import ScreenCaptureKit

let content = try await SCShareableContent.current
let targetAppName = "PyCharm"
var targetAppWindow: SCWindow? = nil


for win in content.windows {
    if let app = win.owningApplication{
        if win.isOnScreen && win.frame.width > 10 && win.frame.height > 10 && app.applicationName == targetAppName{
            targetAppWindow = win
            print("[Capture Helper] success :D")
            break
        }
    } else {
    print("[Capture Helper] Could not find " + targetAppName)

    }
}

import ScreenCaptureKit
import Foundation
import AppKit
import CoreVideo

_ = NSApplication.shared


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
    }
}

guard let window = targetAppWindow else {
    print("[Capture Helper] Could not find " + targetAppName)
    exit(1)
}

let contentFilter = SCContentFilter(desktopIndependentWindow: window)
let streamConfig = SCStreamConfiguration()
let backingScaleFactor = NSScreen.main?.backingScaleFactor ?? 1.0

streamConfig.width = Int(window.frame.size.width * backingScaleFactor)
streamConfig.height = Int(window.frame.size.height * backingScaleFactor)
streamConfig.pixelFormat = kCVPixelFormatType_32BGRA

class OutputHandler: NSObject, SCStreamOutput {
    func stream(_ stream: SCStream, didOutputSampleBuffer sampleBuffer: CMSampleBuffer, of type: SCStreamOutputType) {
        guard let pixelBuffer = sampleBuffer.imageBuffer else { return }

        CVPixelBufferLockBaseAddress(pixelBuffer, .readOnly)
        defer { CVPixelBufferUnlockBaseAddress(pixelBuffer, .readOnly) }

        let width = CVPixelBufferGetWidth(pixelBuffer)
        let height = CVPixelBufferGetHeight(pixelBuffer)
        let stride = CVPixelBufferGetBytesPerRow(pixelBuffer)
        guard let pixelDataPointer = CVPixelBufferGetBaseAddress(pixelBuffer) else { return }
        var frameData = Data()
        for row in 0..<height {
            let rowStart = pixelDataPointer + row * stride
            frameData.append(Data(bytes: rowStart, count: width * 4))
        }
        var header = Data()
        header.append(contentsOf: withUnsafeBytes(of: UInt32(width)) { Array($0) })
        header.append(contentsOf: withUnsafeBytes(of: UInt32(height)) { Array($0) })
        FileHandle.standardOutput.write(header)
        FileHandle.standardOutput.write(frameData)
    }
}

let outputHandler = OutputHandler()
let stream = SCStream(filter: contentFilter, configuration: streamConfig, delegate: nil)

try stream.addStreamOutput(outputHandler, type: .screen, sampleHandlerQueue:nil)

try await stream.startCapture()

while true {
    try await Task.sleep(for: .seconds(60))
}
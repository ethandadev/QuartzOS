import ScreenCaptureKit
import Foundation
import AppKit
import CoreVideo

_ = NSApplication.shared

func findTargetWindow(named targetAppName: String, in content: SCShareableContent) -> SCWindow? {
    for win in content.windows {
        if let app = win.owningApplication {
            if win.isOnScreen && win.frame.width > 10 && win.frame.height > 10 && app.applicationName == targetAppName {
                return win
            }
        }
    }
    return nil
}

func eprint(_ message: String) {
    FileHandle.standardError.write((message + "\n").data(using: .utf8)!)
}

let content = try await SCShareableContent.current
guard CommandLine.arguments.count > 1 else {
    eprint("[Capture Helper] Usage: capture_helper <app name>")
    exit(1)
}
let targetAppName = CommandLine.arguments[1]
let targetAppWindow = findTargetWindow(named: targetAppName, in: content)

guard let window = targetAppWindow else {
    eprint("[Capture Helper] Could not find " + targetAppName)
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
    try await Task.sleep(for: .seconds(1))

    let freshContent = try await SCShareableContent.current
    guard let freshWindow = freshContent.windows.first(where: { $0.windowID == window.windowID }) else { continue }

    let newWidth = Int(freshWindow.frame.size.width * backingScaleFactor)
    let newHeight = Int(freshWindow.frame.size.height * backingScaleFactor)

    if newWidth != streamConfig.width || newHeight != streamConfig.height {
        streamConfig.width = newWidth
        streamConfig.height = newHeight
        try await stream.updateConfiguration(streamConfig)
        eprint("[Capture Helper] Resized to \(newWidth)x\(newHeight)")
    }
}
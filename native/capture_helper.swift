//
//  native/capture_helper.swift
//
//  Standalone ScreenCaptureKit helper for Quartz OS.
//
//  Captures a single application window and streams it to stdout as raw
//  frames: an 8-byte little-endian header (UInt32 width, UInt32 height)
//  followed by width * height * 4 bytes of BGRA pixel data, with row
//  padding already stripped. Diagnostics go to stderr so they can never
//  corrupt the frame stream on stdout.
//
//  This exists because the equivalent PyObjC path is blocked by an upstream
//  ScreenCaptureKit completion-handler bug -- see core/capture_engine.py.
//  core/capture_engine.py's NativeCaptureManager is the consumer.
//
//  Usage: capture_helper <application name>
//

import ScreenCaptureKit
import Foundation
import AppKit
import CoreVideo

_ = NSApplication.shared

/// Returns the first on-screen window belonging to `targetAppName`.
///
/// Windows smaller than 10x10 are skipped -- apps keep tiny offscreen
/// helper windows around that would otherwise match first.
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

/// Writes a diagnostic line to stderr, keeping stdout clean for frame data.
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

/// Receives frames from the stream and writes them to stdout.
class OutputHandler: NSObject, SCStreamOutput {
    /// Called once per captured frame.
    ///
    /// Copies each row out of the pixel buffer while it is locked, dropping
    /// the row padding so the consumer receives a tightly packed image, then
    /// writes the size header followed by the pixel data.
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
        header.append(frameData)
        FileHandle.standardOutput.write(header)
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
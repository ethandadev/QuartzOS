import objc
from Foundation import NSObject
from ScreenCaptureKit import SCStreamOutputTypeScreen, SCShareableContent, SCContentFilter, SCStreamConfiguration, SCStream
from Quartz import CVPixelBufferLockBaseAddress, CVPixelBufferUnlockBaseAddress, kCVPixelBufferLock_ReadOnly, CVPixelBufferGetHeight, CVPixelBufferGetWidth, CVPixelBufferGetBytesPerRow, CVPixelBufferGetBaseAddress, kCVPixelFormatType_32BGRA
from core.display_utils import get_backing_scale_factor
import numpy as np
import struct
import subprocess
import threading
import pygame

# NOTE: Part of the PyObjC pipeline, currently blocked (see WindowCaptureManager
# below for details). The stride-padding math here (stride vs width*4) is a
# SEPARATE, independent copy of the same problem native/capture_helper.swift
# already solves on its own -- they each strip padding from their own raw
# buffer before it goes anywhere else. If you're working on the Swift/
# NativeCaptureManager pipeline, this class is NOT what you need to touch --
# go to NativeCaptureManager instead. This class only matters again once the
# pyobjc bug is fixed and WindowCaptureManager is back in use.

class StreamOutputHandler(NSObject, protocols=[objc.protocolNamed('SCStreamOutput')]):
    def init(self):
        self = objc.super(StreamOutputHandler, self).init()
        if self is None:
            return None
        self.latest_frame = None
        return self

    def stream_didOutputSampleBuffer_ofType_(self, stream, sampleBuffer, streamType):
        if streamType != SCStreamOutputTypeScreen:
            return
        image_buffer =  sampleBuffer.imageBuffer()
        if not image_buffer:
            return
        CVPixelBufferLockBaseAddress(image_buffer, kCVPixelBufferLock_ReadOnly)
        try:
            width = CVPixelBufferGetWidth(image_buffer)
            height = CVPixelBufferGetHeight(image_buffer)
            stride = CVPixelBufferGetBytesPerRow(image_buffer)
            pixel_bytes = CVPixelBufferGetBaseAddress(image_buffer)
            buf = np.frombuffer(pixel_bytes, dtype=np.uint8, count=stride * height)
            arr = buf.reshape((height, stride))
            visible = arr[:, : width * 4].reshape((height, width, 4))
            self.latest_frame = (visible.tobytes(), width, height)
        finally:
            CVPixelBufferUnlockBaseAddress(image_buffer, kCVPixelBufferLock_ReadOnly)


# NOTE: Blocked by a confirmed pyobjc/ScreenCaptureKit bug where
# SCShareableContent's completion handler crashes with
# "TypeError: Need 4 arguments, got 3" -- reproduced across
# macOS 26.0-26.6.1 and pyobjc 11.1-12.2.1. Fully correct otherwise;
# switch back to this once the upstream bug is fixed.
# See NativeCaptureManager below for the current working replacement.
class WindowCaptureManager:
    def __init__(self, target_app_name: str):
        self.target_app_name = target_app_name
        self.handler = StreamOutputHandler.alloc().init()
        self.stream = None

    def start_capture(self):
        def completion_handler(content, error):
            if error or not content:
                print(f'[Capture Error] {error}')
                return
            target_window = None
            for win in content.windows():
                if win.owningApplication().applicationName() == self.target_app_name and win.isOnScreen() and win.frame().size.width > 10 and win.frame().size.height > 10:
                    target_window = win
                    break

            if not target_window:
                print(f'[Capture]: Window {self.target_app_name} Not Found')
                return
            content_filter = SCContentFilter.alloc().initWithDesktopIndependentWindow_(target_window)
            stream_config = SCStreamConfiguration.alloc().init()
            backing_scale_factor = get_backing_scale_factor()
            stream_config.setWidth_(int(target_window.frame().size.width * backing_scale_factor))
            stream_config.setHeight_(int(target_window.frame().size.height * backing_scale_factor))
            stream_config.setPixelFormat_(kCVPixelFormatType_32BGRA)
            self.stream = SCStream.alloc().initWithFilter_configuration_delegate_(content_filter, stream_config, None)
            success, error = self.stream.addStreamOutput_type_sampleHandlerQueue_error_(self.handler, SCStreamOutputTypeScreen, None)
            if not success:
                print(f'[Capture Error] {error}')
                return

            def start_completion_handler(error):
                if error:
                    print(f'[Capture Error] {error}')
                else:
                    print(f'[Capture] Started capturing {self.target_app_name}')
            self.stream.startCaptureWithCompletionHandler_(start_completion_handler)


        SCShareableContent.getShareableContentExcludingDesktopWindows_onScreenWindowsOnly_completionHandler_(True, True, completion_handler)


class NativeCaptureManager:
    def __init__(self, target_app_name: str, helper_path="native/capture_helper"):
        self.target_app_name = target_app_name
        self.helper_path = helper_path
        self.process = None
        self.latest_frame = None
        self.thread = None
        self.running = False

    def _read_exact(self, n):
        data = b""
        while len(data) < n:
            chunk = self.process.stdout.read(n-len(data))
            if not chunk:
                raise EOFError("Stream closed unexpectedly")
            data += chunk
        return data

    def _read_loop(self):
        while self.running:
            frame_header = self._read_exact(8)
            width, height = struct.unpack("<II", frame_header)

            frame_size = height * width * 4

            self.latest_frame = (self._read_exact(frame_size), width, height)
            print(f"Got frame: {width}x{height}, {len(self.latest_frame[0])} bytes")

    def start_capture(self):
        self.process = subprocess.Popen(
            [self.helper_path, self.target_app_name],
            stdout=subprocess.PIPE
        )
        self.running = True
        self.thread = threading.Thread(target=self._read_loop, daemon=True)
        self.thread.start()

    def get_latest_surface(self):
        if self.latest_frame is None:
            return None
        frame_bytes, width, height = self.latest_frame
        return pygame.image.frombuffer(frame_bytes, (width, height), 'BGRA')




import objc
from Foundation import NSObject
from ScreenCaptureKit import SCStreamOutputTypeScreen, SCShareableContent
from Quartz import CVPixelBufferLockBaseAddress, CVPixelBufferUnlockBaseAddress, kCVPixelBufferLock_ReadOnly, CVPixelBufferGetHeight, CVPixelBufferGetWidth, CVPixelBufferGetBytesPerRow, CVPixelBufferGetBaseAddress
import numpy as np
import pygame

class StreamOutputHandler(NSObject, protocols=[objc.protocolNamed('SCStreamOutput')]):
    def init(self):
        self = objc.super(StreamOutputHandler, self).init()
        if self is None:
            return None
        self.latest_surface = None
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
            surface = pygame.image.frombuffer(visible.tobytes(), (width, height), 'BGRA')
            self.latest_surface = surface
        finally:
            CVPixelBufferUnlockBaseAddress(image_buffer, kCVPixelBufferLock_ReadOnly)

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
                if win.owningApplication().applicationName() == self.target_app_name:
                    target_window = win
                    break

            if not target_window:
                print(f'[Capture]: Window {self.target_app_name}')


        SCShareableContent.getShareableContentWithCompletionHandler_(completion_handler)
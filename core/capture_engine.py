import objc
from Foundation import NSObject
from ScreenCaptureKit import SCStreamOutputTypeScreen, SCShareableContent, SCContentFilter, SCStreamConfiguration, SCStream
from Quartz import CVPixelBufferLockBaseAddress, CVPixelBufferUnlockBaseAddress, kCVPixelBufferLock_ReadOnly, CVPixelBufferGetHeight, CVPixelBufferGetWidth, CVPixelBufferGetBytesPerRow, CVPixelBufferGetBaseAddress, kCVPixelFormatType_32BGRA
from core.display_utils import get_backing_scale_factor
import numpy as np

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
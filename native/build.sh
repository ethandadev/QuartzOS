#!/bin/bash
# Builds the ScreenCaptureKit capture helper from source.
# Run this once after cloning, and again any time capture_helper.swift changes.
set -e
cd "$(dirname "$0")"
swiftc capture_helper.swift -o capture_helper
echo "Built native/capture_helper"

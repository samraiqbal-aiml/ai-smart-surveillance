#!/usr/bin/env python3
"""
Motion Analysis Module
Author: Samra Iqbal
Description: Real-time motion detection and analysis
"""

import cv2
import numpy as np

class MotionAnalyzer:
    def __init__(self):
        print("📊 Motion Analyzer Initialized")
        self.previous_frame = None
        self.motion_threshold = 1000
        self.min_contour_area = 500
    
    def detect_motion(self, frame):
        """Detect motion in the current frame"""
        motion_detected = False
        motion_frame = frame.copy()
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        if self.previous_frame is None:
            self.previous_frame = gray
            return motion_detected, motion_frame
        
        # Compute difference between frames
        frame_diff = cv2.absdiff(self.previous_frame, gray)
        thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Check for significant motion
        for contour in contours:
            if cv2.contourArea(contour) > self.min_contour_area:
                motion_detected = True
                # Draw motion area
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(motion_frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
        
        self.previous_frame = gray
        
        return motion_detected, motion_frame

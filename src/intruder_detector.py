#!/usr/bin/env python3
"""
Intruder Detection Module
Author: Samra Iqbal
Description: AI-powered intruder detection using computer vision
"""

import cv2
import numpy as np

class IntruderDetector:
    def __init__(self):
        print("🔍 Intruder Detector Initialized")
        # Load YOLO model for person detection
        self.setup_detection_model()
    
    def setup_detection_model(self):
        """Setup the object detection model"""
        # For demo purposes, we'll use a simple detection method
        # In production, this would use YOLO or other ML models
        print("✅ Detection model ready (Demo Mode)")
    
    def detect_intruders(self, frame):
        """Detect intruders in the frame"""
        intruders = []
        
        # Convert to grayscale for processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Simple motion-based intruder detection (demo)
        intruder_detected = self.demo_intruder_detection(frame)
        
        if intruder_detected:
            intruders.append({
                'type': 'person',
                'confidence': 0.85,
                'location': self.get_demo_location(),
                'timestamp': cv2.getTickCount() / cv2.getTickFrequency()
            })
        
        # Draw detection results
        detection_frame = self.draw_detections(frame, intruders)
        
        return intruders, detection_frame
    
    def demo_intruder_detection(self, frame):
        """Demo intruder detection logic"""
        # Simple color-based detection for demo
        # Look for red regions (simulating intruder alerts)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Define red color range
        lower_red = np.array([0, 120, 70])
        upper_red = np.array([10, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)
        
        lower_red = np.array([170, 120, 70])
        upper_red = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, lower_red, upper_red)
        
        mask = mask1 + mask2
        
        # If significant red areas detected, consider it an intruder
        if np.sum(mask) > 10000:
            return True
        
        # Random detection for demo variety
        import random
        return random.random() < 0.02  # 2% chance for demo
    
    def get_demo_location(self):
        """Get demo intruder location"""
        return (300, 100, 350, 300)  # x1, y1, x2, y2
    
    def draw_detections(self, frame, intruders):
        """Draw intruder detections on frame"""
        for intruder in intruders:
            x1, y1, x2, y2 = intruder['location']
            
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            
            # Draw label
            label = f"INTRUDER: {intruder['confidence']:.2f}"
            cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        return frame

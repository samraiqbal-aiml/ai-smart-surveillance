#!/usr/bin/env python3
"""
AI Smart Surveillance System
Author: Samra Iqbal
Description: Real-time surveillance with intruder detection and alerts
"""

import cv2
import time
import threading
from intruder_detector import IntruderDetector
from motion_analyzer import MotionAnalyzer
from alert_manager import AlertManager

class SmartSurveillance:
    def __init__(self, config_path="config/settings.yaml"):
        print("🚀 AI Smart Surveillance System Initialized")
        
        # Initialize components
        self.intruder_detector = IntruderDetector()
        self.motion_analyzer = MotionAnalyzer()
        self.alert_manager = AlertManager()
        
        # System state
        self.is_running = False
        self.recording = False
        self.alert_cooldown = 0
        
        # Statistics
        self.stats = {
            'frames_processed': 0,
            'intruders_detected': 0,
            'motion_events': 0,
            'alerts_sent': 0
        }
        
        print("✅ All surveillance components loaded successfully")
    
    def start_surveillance(self, video_source=0):
        """Start the main surveillance loop"""
        print(f"📹 Starting surveillance on video source: {video_source}")
        
        # Open video capture
        self.cap = cv2.VideoCapture(video_source)
        if not self.cap.isOpened():
            print("❌ Error: Could not open video source")
            # Create demo video source
            return self.start_demo_mode()
        
        self.is_running = True
        self.surveillance_loop()
    
    def start_demo_mode(self):
        """Start surveillance with demo video"""
        print("🎥 Starting in DEMO MODE with sample footage")
        self.is_running = True
        self.demo_loop()
    
    def surveillance_loop(self):
        """Main surveillance processing loop"""
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                print("❌ Error reading frame")
                break
            
            # Process frame
            processed_frame, alerts = self.process_frame(frame)
            
            # Display results
            self.display_frame(processed_frame)
            
            # Handle alerts
            if alerts:
                self.handle_alerts(alerts, frame)
            
            # Update statistics
            self.stats['frames_processed'] += 1
            
            # Check for exit command
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cleanup()
    
    def demo_loop(self):
        """Demo loop with simulated surveillance footage"""
        print("🎬 Generating demo surveillance footage...")
        
        frame_count = 0
        while self.is_running and frame_count < 300:  # 10 seconds at 30fps
            # Create simulated camera frame
            frame = self.create_surveillance_frame(frame_count)
            
            # Simulate occasional intruders
            if frame_count % 100 == 50:  # Simulate intruder at frame 50, 150, 250
                frame, intruder_info = self.add_simulated_intruder(frame)
                alerts = ['intruder_detected']
                self.handle_alerts(alerts, frame)
            
            # Process frame
            processed_frame, alerts = self.process_frame(frame)
            
            # Display
            self.display_frame(processed_frame)
            
            frame_count += 1
            self.stats['frames_processed'] += 1
            
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        
        self.cleanup()
    
    def process_frame(self, frame):
        """Process a single frame for surveillance"""
        alerts = []
        
        # Detect motion
        motion_detected, motion_frame = self.motion_analyzer.detect_motion(frame)
        if motion_detected:
            alerts.append('motion_detected')
            self.stats['motion_events'] += 1
        
        # Detect intruders
        intruders, detection_frame = self.intruder_detector.detect_intruders(frame)
        if intruders:
            alerts.append('intruder_detected')
            self.stats['intruders_detected'] += 1
        
        # Combine results
        processed_frame = self.overlay_info(frame, motion_detected, len(intruders))
        
        return processed_frame, alerts
    
    def create_surveillance_frame(self, frame_count):
        """Create simulated surveillance footage"""
        height, width = 480, 640
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Create room background
        cv2.rectangle(frame, (0, 0), (width, height), (30, 30, 30), -1)  # Dark room
        
        # Add some static elements
        cv2.rectangle(frame, (100, 200), (200, 400), (50, 50, 80), -1)   # Cabinet
        cv2.rectangle(frame, (400, 150), (500, 300), (60, 60, 40), -1)   # Table
        
        # Add timestamp
        timestamp = f"Surveillance Demo - Frame: {frame_count}"
        cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return frame
    
    def add_simulated_intruder(self, frame):
        """Add a simulated intruder to the frame"""
        # Add a "person" rectangle
        cv2.rectangle(frame, (300, 100), (350, 300), (0, 0, 255), -1)  # Red intruder
        
        # Add intruder label
        cv2.putText(frame, "INTRUDER", (280, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        intruder_info = {
            'type': 'person',
            'confidence': 0.95,
            'location': (300, 100, 350, 300)
        }
        
        return frame, intruder_info
    
    def overlay_info(self, frame, motion_detected, intruder_count):
        """Overlay surveillance information on frame"""
        # Status overlay
        status = "SECURE"
        color = (0, 255, 0)  # Green
        
        if intruder_count > 0:
            status = f"ALERT: {intruder_count} INTRUDERS"
            color = (0, 0, 255)  # Red
        elif motion_detected:
            status = "MOTION DETECTED"
            color = (0, 255, 255)  # Yellow
        
        # Add status banner
        cv2.rectangle(frame, (0, 0), (640, 40), (0, 0, 0), -1)
        cv2.putText(frame, status, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # Add statistics
        stats_text = f"Frames: {self.stats['frames_processed']} | Intruders: {self.stats['intruders_detected']} | Alerts: {self.stats['alerts_sent']}"
        cv2.putText(frame, stats_text, (10, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame
    
    def handle_alerts(self, alerts, frame):
        """Handle surveillance alerts"""
        for alert in alerts:
            print(f"🚨 ALERT: {alert.upper()}")
            
            if self.alert_cooldown <= 0:
                # Send alert
                self.alert_manager.send_alert(alert, frame)
                self.stats['alerts_sent'] += 1
                self.alert_cooldown = 30  # Cooldown period
        
        if self.alert_cooldown > 0:
            self.alert_cooldown -= 1
    
    def display_frame(self, frame):
        """Display the processed frame"""
        cv2.imshow('AI Smart Surveillance - Samra Iqbal', frame)
    
    def cleanup(self):
        """Cleanup resources"""
        self.is_running = False
        if hasattr(self, 'cap'):
            self.cap.release()
        cv2.destroyAllWindows()
        
        # Print final statistics
        print("\n📊 Surveillance Session Statistics:")
        print(f"   Frames Processed: {self.stats['frames_processed']}")
        print(f"   Intruders Detected: {self.stats['intruders_detected']}")
        print(f"   Motion Events: {self.stats['motion_events']}")
        print(f"   Alerts Sent: {self.stats['alerts_sent']}")
        print("✅ Surveillance system shutdown complete")

def main():
    """Main function to start surveillance system"""
    print("🛡️ AI Smart Surveillance System")
    print("=" * 50)
    
    surveillance = SmartSurveillance()
    
    try:
        # Start surveillance (0 for webcam, or use demo mode)
        surveillance.start_surveillance(video_source=0)
    except Exception as e:
        print(f"❌ Error in surveillance system: {e}")
        surveillance.cleanup()

if __name__ == "__main__":
    import numpy as np
    main()

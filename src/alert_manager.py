#!/usr/bin/env python3
"""
Alert Management Module
Author: Samra Iqbal
Description: Handle surveillance alerts and notifications
"""

import time
import datetime

class AlertManager:
    def __init__(self):
        print("🚨 Alert Manager Initialized")
        self.alert_history = []
    
    def send_alert(self, alert_type, frame):
        """Send surveillance alert"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        alert_data = {
            'type': alert_type,
            'timestamp': timestamp,
            'message': self.get_alert_message(alert_type)
        }
        
        # Add to history
        self.alert_history.append(alert_data)
        
        # Print alert (in real system, this would send email/SMS)
        print(f"🔔 ALERT [{timestamp}]: {alert_data['message']}")
        
        # Save alert snapshot (in real system, this would save image)
        self.save_alert_snapshot(frame, alert_type, timestamp)
    
    def get_alert_message(self, alert_type):
        """Get formatted alert message"""
        messages = {
            'motion_detected': 'Motion detected in surveillance area',
            'intruder_detected': 'INTRUDER DETECTED - Immediate attention required',
            'system_alert': 'Surveillance system alert'
        }
        return messages.get(alert_type, 'Unknown alert type')
    
    def save_alert_snapshot(self, frame, alert_type, timestamp):
        """Save alert snapshot (demo version)"""
        # In a real system, this would save the image to disk
        print(f"📸 Alert snapshot saved for {alert_type} at {timestamp}")
        # cv2.imwrite(f"alerts/alert_{timestamp.replace(':', '-')}.jpg", frame)
    
    def get_alert_history(self):
        """Get alert history"""
        return self.alert_history

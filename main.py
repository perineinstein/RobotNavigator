from kivy.app import App
from kivy.clock import Clock
from libs.gps import GPSReader
from libs.serial_send import SerialController
import math
import pyrebase
import json
import time

# Load Firebase config
with open("firebase_config.json") as f:
    config = json.load(f)

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Initialize GPS and Serial
gps = GPSReader()
serial = SerialController()

class RobotApp(App):
    def build(self):
        Clock.schedule_interval(self.update, 5)  # update every 5 seconds
        return None  # No UI for now

    def update(self, dt):
        lat, lon = gps.get_location()
        if lat and lon:
            print(f"Location: {lat}, {lon}")
            db.child("robot").update({
                "location": {"lat": lat, "lng": lon},
                "timestamp": int(time.time())
            })

            mode = db.child("robot").child("mode").get().val()
            if mode == "auto":
                self.auto_drive(lat, lon)
            elif mode == "manual":
                self.manual_control()

    def calculate_bearing(self, lat1, lon1, lat2, lon2):
        dLon = math.radians(lon2 - lon1)
        y = math.sin(dLon) * math.cos(math.radians(lat2))
        x = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - \
            math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(dLon)
        return (math.degrees(math.atan2(y, x)) + 360) % 360

    def auto_drive(self, lat, lon):
        target = db.child("robot").child("target").get().val()
        if not target:
            print("No target set in Firebase.")
            return

        dest_lat = target.get("lat")
        dest_lon = target.get("lng")
        if dest_lat is None or dest_lon is None:
            print("Invalid target coordinates.")
            return

        bearing = self.calculate_bearing(lat, lon, dest_lat, dest_lon)
        print(f"Bearing to target: {bearing:.2f}")

        # Send direction command to Arduino based on bearing
        if bearing < 45 or bearing >= 315:
            serial.send("F")  # Forward
        elif bearing < 135:
            serial.send("R")  # Right
        elif bearing < 225:
            serial.send("B")  # Back
        else:
            serial.send("L")  # Left

    def manual_control(self):
        command = db.child("robot").child("manual_command").get().val()
        if command:
            print(f"Manual command: {command}")
            serial.send(command)
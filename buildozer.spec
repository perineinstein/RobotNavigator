[app]
title = RobotNavigator
package.name = robotnavigator
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 1.0
requirements = python3,kivy,plyer,pyjnius,requests,pyserial
orientation = portrait
fullscreen = 1
android.permissions = INTERNET,ACCESS_COARSE_LOCATION,ACCESS_FINE_LOCATION
android.api = 33
android.minapi = 21
android.ndk = 23b
android.arch = armeabi-v7a
android.enable_androidx = 1
android.use_android_native_activity = False
android.logcat_filters = *:S python:D
android.allow_backup = True

# (Optional) Hide status bar
android.hide_statusbar = 1

# Include Firebase config
presplash.filename = %(source.dir)s/assets/loading.png
android.add_assets = firebase_config.json

[buildozer]
log_level = 2
warn_on_root = 1
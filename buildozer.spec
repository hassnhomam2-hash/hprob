[app]

# (str) Title of your application
title = Hprob

# (str) Package name
package.name = hprob

# (str) Package domain (needed for android/ios packaging)
package.domain = org.myname

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (leave empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 1.0

# (list) Application requirements
# YOU MUST INCLUDE kivymd HERE
requirements = python3, kivy, kivymd

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.jpg

# (str) Supported orientations (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) Permissions (remove the '#' if your app needs internet access)
#android.permissions = INTERNET

# (int) Target Android API (33 is currently required by Google Play)
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

[app]
title = Hprob
package.name = hprob
package.domain = org.hprob
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,kivymd,numpy,scipy,matplotlib,pillow
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
icon.filename = %(source.dir)s/icon.jpg

[buildozer]
log_level = 2
warn_on_root = 1

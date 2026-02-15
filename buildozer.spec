[app]

# (str) Title of your application
title = File Explorer Remote

# (str) Package name
package.name = fileexplorer

# (str) Package domain (needed for android/ios packaging)
package.domain = com.fileexplorer

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.2.1,flask==2.3.2,flask-cors==4.0.0,werkzeug==2.3.6,requests

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage OR --dir public storage
android.private_storage = False

# (str) Android app theme, default is ok for Kivy-based app
android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a,armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) The Android additional libraries to be loaded
android.add_libs_armeabi = libs/android/*.so
android.add_libs_armeabi_v7a = libs/android-v7/*.so
android.add_libs_arm64_v8a = libs/android-v8/*.so
android.add_libs_x86 = libs/android-x86/*.so
android.add_libs_mips = libs/android-mips/*.so

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The directory in which python-for-android should look for your own build recipes
p4a.local_recipes = ./p4a-recipes

# (str) python-for-android fork to use (default would be upstream)
p4a.fork = kivy

# (str) python-for-android branch to use (default would be master)
p4a.branch = master

# (str) python-for-android specific commit to use (default would be HEAD)
# p4a.commit = HEAD

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
# p4a.source_dir =

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
# bin_dir = ./bin

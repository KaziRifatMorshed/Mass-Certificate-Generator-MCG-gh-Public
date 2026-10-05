[app]

# title of your application
title = MassCertificateGenerator-MCG

# project root directory. default = The parent directory of input_file
project_dir = .

# source file entry point path. default = main.py
input_file = main.py

# directory where the executable output is generated
exec_directory = .

# path to the project file relative to project_dir
project_file = pyproject.toml

# application icon
icon = /home/noobcod3r-rtx/Documents/GitHub/mass-certificate-generator/MassCertificateGenerator-MCG/extra/MCG_logo.png

[python]

# python path
python_path = /mnt/BigBangT/qtForPython/android_build_venv/bin/python3

# python packages to install
packages = Nuitka==2.7.11

# buildozer = for deploying Android application
android_packages = buildozer==1.5.0,cython==0.29.33

[qt]

# paths to required qml files. comma separated
# normally all the qml files required by the project are added automatically
# design studio projects include the qml files using qt resources
qml_files = 

# excluded qml plugin binaries
excluded_qml_plugins = 

# qt modules used. comma separated
modules = Core,DBus,Gui,Network,Pdf,PdfWidgets,Widgets

# qt plugins used by the application. only relevant for desktop deployment
# for qt plugins used in android application see [android][plugins]
plugins = accessiblebridge,egldeviceintegrations,generic,iconengines,imageformats,networkaccess,networkinformation,platforminputcontexts,platforms,platforms/darwin,platformthemes,styles,tls,xcbglintegrations

[android]

# path to pyside wheel
wheel_pyside = /mnt/BigBangT/qtForPython/official_android_wheels/PySide6-6.8.0-6.8.0-cp311-cp311-android_aarch64.whl

# path to shiboken wheel
wheel_shiboken = /mnt/BigBangT/qtForPython/official_android_wheels/shiboken6-6.8.0.2-6.8.0-cp311-cp311-android_aarch64.whl

# plugins to be copied to libs folder of the packaged application. comma separated
plugins = platforms_qtforandroid

[nuitka]

# usage description for permissions requested by the app as found in the info.plist file
# of the app bundle. comma separated
# eg = extra_args = --show-modules --follow-stdlib
macos.permissions = 

# mode of using nuitka. accepts standalone or onefile. default = onefile
mode = onefile

# specify any extra nuitka arguments
extra_args = --quiet --noinclude-qt-translations --include-package=pymupdf --include-package-data=pymupdf --include-package=pandas --include-package-data=pandas --include-package=numpy --include-package-data=numpy --enable-plugin=numpy --nofollow-import-to=*.tests --nofollow-import-to=*.testing --cc-flags="-O0"

[buildozer]

# build mode
# possible values = ["aarch64", "armv7a", "i686", "x86_64"]
# release creates a .aab, while debug creates a .apk
mode = release
orientation = landscape
requirements = python3==3.11.14,pyside6,shiboken6,pandas,pymupdf

# path to pyside6 and shiboken6 recipe dir
recipe_dir = /home/noobcod3r-rtx/Documents/GitHub/mass-certificate-generator/MassCertificateGenerator-MCG/deployment/recipes

# path to extra qt android .jar files to be loaded by the application
jars_dir = /home/noobcod3r-rtx/Documents/GitHub/mass-certificate-generator/MassCertificateGenerator-MCG/deployment/jar/PySide6/jar

# if empty, uses default ndk path downloaded by buildozer
ndk_path = /home/noobcod3r-rtx/.pyside6_android_deploy/android-ndk/android-ndk-r27c

# if empty, uses default sdk path downloaded by buildozer
sdk_path = /home/noobcod3r-rtx/.pyside6_android_deploy/android-sdk

# other libraries to be loaded at app startup. comma separated.
local_libs = plugins_platforms_qtforandroid

# architecture of deployed platform
arch = aarch64


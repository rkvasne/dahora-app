# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('icon.ico', '.')]
binaries = []
hiddenimports = [
    'pystray', 
    'pyperclip', 
    'keyboard', 
    'winotify', 
    'win32api', 
    'win32con', 
    'win32event', 
    'tkinter', 
    'tkinter.ttk',
    'PIL', 
    'PIL.Image', 
    'PIL.ImageDraw', 
    'PIL.ImageFont', 
    'dahora_app', 
    'dahora_app.ui',
    'dahora_app.ui.custom_shortcuts_dialog',
    'dahora_app.ui.search_dialog',
    'dahora_app.ui.settings_dialog',
    'dahora_app.ui.about_dialog',
    'dahora_app.ui.prefix_dialog',
    'dahora_app.ui.menu',
    'dahora_app.hotkeys',
    'dahora_app.settings',
    'dahora_app.clipboard',
    'dahora_app.datetime_formatter',
    'dahora_app.notification',
    'dahora_app.counter',
    'dahora_app.constants',
    'dahora_app.utils',
    'typing'
]

tmp_ret = collect_all('pystray')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('keyboard')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('winotify')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='DahoraApp_v0.2.1',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)

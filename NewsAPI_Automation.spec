# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['gui_app.py'],
    pathex=[],
    binaries=[],
    datas=[('.env', '.')],
    hiddenimports=['PIL._tkinter_finder', 'tkinter', 'tkinter.ttk', 'tkinter.scrolledtext', 'gui_app', 'gui_components', 'gui_styles', 'zai_classifier', 'image_generator', 'zai_prompts', 'tuning_search', 'config'],
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
    name='NewsAPI_Automation',
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
    icon=['C:\\work\\relances\\automation\\icon.ico'],
)

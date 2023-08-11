# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

pathex = [
    'C:/Users/Administrator/PycharmProjects/yolov5'
]

a = Analysis(
    ['export.py'],
    pathex=pathex,
    binaries=[(r'./utils/general.pyc',r'./utils')],
    datas=[(r'./apex_model/1w2/best.pt',r'./apex_model/1w2'),(r'./apex_model/1w2/1w.yaml',r'./apex_model/1w2'),(r'./config/export_config.json',r'./config')],
    hiddenimports=['models.yolo'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='trt',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='./images/ag.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='trt'
)

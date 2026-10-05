# -*- mode: python ; coding: utf-8 -*-


import os

extra_datas = [
    ('extra/MCG_logo.png', 'extra'),
]
if os.path.exists('extra/MCG_logo.ico'):
    extra_datas.append(('extra/MCG_logo.ico', 'extra'))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=extra_datas,
    hiddenimports=['pandas', 'pymupdf', 'fitz', 'version'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PyQt5', 'PyQt6', 'PySide2', 'tkinter', 'matplotlib', 'IPython', 'sphinx',
        'scipy', 'tornado', 'llvmlite', 'numba', 'pyarrow', 'bokeh', 'panel',
        'lief', 'dask', 'sqlalchemy', 'mysql', '_mysql_connector', 'psycopg2',
        'notebook', 'jupyter', 'nbformat', 'nbconvert', 'traitlets', 'astropy',
        'skimage', 'sklearn', 'torch', 'scipy_openblas', 'sympy', 'pytest',
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

icon_target = 'extra/MCG_logo.ico' if os.path.exists('extra/MCG_logo.ico') else 'extra/MCG_logo.png'

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MassCertificateGenerator',
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
    icon=[icon_target],
)

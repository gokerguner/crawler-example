# run.spec

import sys
from PyInstaller.utils.hooks import collect_data_files

a = Analysis(['run.py'],
             pathex=['/app'],
             binaries=[],
             datas=[],
             #hiddenimports=['config.envparams','config.statuslogger','db.mongo'],
             hiddenimports=['config','db','pymongo'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=None,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=None)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='run',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          upx_debug_dlls=False,
          runtime_tmpdir=None,
          console=True)


# -*- mode: python -*-

block_cipher = None


a = Analysis(['IPporEmail.pycls'],
             pathex=['E:\\Marco\\Programas\\IP por E-mail\\python\\win\\recs'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='IPporEmail',
          debug=False,
          strip=False,
          upx=True,
          console=False , version='version.xml', icon='IP_ico.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='IPporEmail')

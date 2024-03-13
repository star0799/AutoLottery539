# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['AutoLottery539.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('log.py', '.'),
        ('ReadFile.py', '.'),
        ('LotteryData.py', '.'),
        ('SeleniumChrome.py', '.'),
        ('WriteFile.py', '.'),
		('UpdateAutoLottery539.py', '.'),
    ],
    hiddenimports=['selenium','selenium.webdriver.common.by','selenium.webdriver.common.keys','selenium.webdriver.common.action_chains','selenium.webdriver.support.ui','selenium.webdriver.support','selenium.webdriver.support.ui','selenium.webdriver.support.expected_conditions','configparser'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AutoLottery539.exe',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

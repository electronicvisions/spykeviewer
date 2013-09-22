# -*- mode: python -*-

import os
import sys
import platform

import guidata
import guiqwt
import spyderlib

import spykeutils
import spykeviewer


module_path = os.path.dirname(spykeviewer.__file__)
viewer_path = os.path.dirname(module_path)


def find_version(path):
    try:
        f = open(os.path.join(path, 'spykeviewer', '__init__.py'), 'r')
        try:
            for line in f:
                if line.startswith('__version__'):
                    rval = line.split()[-1][1:-1]
                    break
        finally:
            f.close()
    except Exception:
        rval = '0'
    return rval


def dir_files(path, rel):
    ret = []
    for p,d,f in os.walk(path):
        relpath = p.replace(path, '')[1:]
        for fname in f:
            ret.append((os.path.join(rel, relpath, fname),
                        os.path.join(p, fname), 'DATA'))
    return ret


a = Analysis([os.path.join(viewer_path, 'bin', 'freeze', 'dependencies.py'),
              os.path.join(viewer_path, 'bin', 'spykeviewer')],
             hiddenimports=[],
             hookspath=None,
             excludes='Tkinter')

if platform.system() == 'Windows':
    exename = os.path.join('build', 'pyi.win32', 'main', 'spykeviewer.exe')
elif platform.system() == 'Darwin':
    exename = os.path.join('build' , 'pyi.darwin', 'main', 'spykeviewer')
elif platform.system() == 'Linux':
    exename = os.path.join('build', 'pyi.linux', 'main', 'spykeviewer')
else:
    print 'Unsupported operating system!'
    sys.exit()

pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, exclude_binaries=1, name=exename, debug=False,
          strip=None, upx=False, console=False,
          icon=os.path.join(viewer_path, 'bin', 'freeze', 'appicon.ico'))

a.datas.extend(dir_files(os.path.join(os.path.dirname(guidata.__file__),
    'images'), os.path.join('guidata', 'images')))
a.datas.extend(dir_files(os.path.join(os.path.dirname(guiqwt.__file__),
    'images'), os.path.join('guiqwt', 'images')))
a.datas.extend(dir_files(os.path.join(os.path.dirname(spyderlib.__file__),
    'images'), os.path.join('spyderlib', 'images')))
a.datas.append(('', os.path.join(os.path.dirname(spykeutils.__file__),
    'plugin', 'startplugin.py'), 'DATA'))
a.datas.extend(dir_files(os.path.join(module_path, 'plugins'), 'plugins'))

dist_dir = os.path.join('dist', 'main')
coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, strip=None,
               upx=False, name=dist_dir)
               
if platform.system() == 'Darwin':
    app = BUNDLE(exe, name='Spyke Viewer.app',
        version=find_version(viewer_path))
import os
pm1EditorExe = r'D:\Game\P5RModding\PM1MessageScriptEditor\PM1MessageScriptEditor.exe'

eventRoot = r'E:\Temp\p4g_text\data_ck.cpk_unpacked\event'


def dumpAllMsg(eventRoot):
  for root, dirs, files in os.walk(eventRoot):
    for name in files:
      if(name.endswith('.PM1')):
        os.system('{} {}'.format(pm1EditorExe, os.path.join(root, name)))


if __name__ == '__main__':
  dumpAllMsg(eventRoot)
  print('DONE')

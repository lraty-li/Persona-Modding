import os

deCompilerPath = "D:\Game\P5RModding\AtlusScriptToolchain.1\AtlusScriptCompiler.exe"

EventFolder = "D:\Game\P5RModding\All_Message_En\EVENT_DATA\MESSAGE"

# BMDFolderPath = "D:\Game\P5RModding\All_Message_En\EVENT_DATA\MESSAGE\E700"

EventFolders = os.listdir(EventFolder)

for folder in EventFolders:
  files = os.listdir(os.path.join(EventFolder, folder))

  for file in files:
    if(file.endswith(".BMD")):  
      os.system(deCompilerPath + " " + os.path.join(EventFolder,folder, file)+ " " + "-Decompile -Library P5 -Encoding P5")

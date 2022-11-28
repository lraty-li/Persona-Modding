import os

deCompilerPath = "D:\Game\P5RModding\AtlusScriptToolchain.1\AtlusScriptCompiler.exe"

# EventFolder = "D:\Game\P5RModding\All_Message_En\EVENT_DATA\MESSAGE"

FBFolderPath = "D:\Game\P5RModding\All_message_zh\FIELD\PANEL"

# EventFolders = os.listdir(EventFolder)

# for folder in EventFolders:
#   files = os.listdir(os.path.join(EventFolder, folder))
files = os.listdir(os.path.join(FBFolderPath))
for file in files:
  if(file.endswith(".BF")):  
    os.system(deCompilerPath + " " + os.path.join(FBFolderPath, file)+ " " + "-Decompile -Library P5 -Encoding p5R_chinese_sim")

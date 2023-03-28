import os

deCompilerPath = "D:\Game\P5RModding\AtlusScriptToolchain.1\AtlusScriptCompiler.exe"

# EventFolder = "D:\Game\P5RModding\All_Message_En\EVENT_DATA\MESSAGE"

BFFolderRoot = r"F:\Game\p5r_cpk\CAMP"

# EventFolders = os.listdir(EventFolder)

for EventFolder in os.listdir(BFFolderRoot):
  BFFolderPath = os.path.join(BFFolderRoot, EventFolder)
  files = os.listdir(BFFolderPath)
  for file in files:
    if(file.endswith(".BF")):  
      os.system(deCompilerPath + " " + os.path.join(BFFolderPath, file)+ " " + "-Decompile -Library P5 -Encoding p5R_chinese_sim")

# for folder in EventFolders:
#   files = os.listdir(os.path.join(EventFolder, folder))
# files = os.listdir(os.path.join(BFFolderPath))
# for file in files:
#   if(file.endswith(".BF")):  
#     os.system(deCompilerPath + " " + os.path.join(BFFolderPath, file)+ " " + "-Decompile -Library P5 -Encoding p5R_chinese_sim")

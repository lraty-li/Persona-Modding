import os

deCompilerPath = "D:\Game\P5RModding\AtlusScriptToolchain.1\AtlusScriptCompiler.exe"

# EventFolder = "D:\Game\P5RModding\All_Message_En\EVENT_DATA\MESSAGE"
messageRoot = r"F:\Game\p5r_cpk\COMMUNITY\EVENT"
# FBFolderPath = r"F:\Game\p5r_cpk\EVENT_DATA\MESSAGE\E500"

for BMDFolder in os.listdir(messageRoot):
  BMDFolderPath = os.path.join(messageRoot, BMDFolder)
BMDFolderPath = r"F:\Game\p5r_cpk\COMMUNITY\EVENT\MESSAGE"
files = os.listdir(BMDFolderPath)
for file in files:
  if(file.endswith(".BMD")):  
    os.system(deCompilerPath + " " + os.path.join(BMDFolderPath, file)+ " " + "-Decompile -Library P5 -Encoding p5R_chinese_sim")

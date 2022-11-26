import re
from openpyxl import load_workbook

# https://www.bilibili.com/read/cv19937910

class ColumnIndicator:
  def __init__(self, columns, starting):
    self.current = starting
    self.currentIndex = columns.index(self.current)
    self.columns = columns
    self.newLine = False
    self.columnsLen = len(columns)
    if(self.currentIndex == self.columnsLen - 1):
      self.newLine = True

  def next(self):
    self.currentIndex += 1
    if(self.currentIndex == self.columnsLen):
      self.currentIndex = 0
      self.newLine = False
    elif (self.currentIndex == self.columnsLen -1 ):
      self.newLine = True
    self.current = self.columns[self.currentIndex]
# gen the [ surrogate pair ] [ zh_sc token ] 

    






def collect_part(startingCell, startingSurrogate, endingCell, sheet):
  spiltRE = r'([a-zA-Z]+)+([0-9]+)'
  startingRow, startingColumn = re.findall(spiltRE, startingCell)[0]
  endingRow = re.findall(spiltRE, endingCell)[0][-1]
  rowIndicator = ColumnIndicator('CDEFGHIJKLMNOPQR', startingRow)

  surrogateOffset = 0
  for row in range(int(startingColumn), int(endingRow)+1):
    while True:
      cell_name = "{}{}".format(rowIndicator.current, row)
      sheet[cell_name].value 
      print(sheet[cell_name].value , hex(startingSurrogate + surrogateOffset))
      surrogateOffset += 1
      shouldNewLine = rowIndicator.newLine
      rowIndicator.next()
      if(shouldNewLine == True):
        break
    
if __name__ == '__main__':
  workbook = load_workbook(filename="P5R字库.xlsx")
  sheet = workbook["Sheet1"]

  startingCell = 'R24'
  startingSurrogate = 0x85EF

  # endingCell = 'R26'
  endingCell = 'R447'

  params = [('R24',0x85EF,'R26'), ] 
  collect_part(startingCell, startingSurrogate, endingCell, sheet)

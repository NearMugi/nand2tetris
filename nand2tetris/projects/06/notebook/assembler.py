#!/usr/bin/env python
# coding: utf-8

# # Assembler  
# .asmファイルを.hackファイルに変換する

# ## 仕様  
# アセンブラのルールをまとめる
# ### 命令  
# 
# #### A命令  
# **0vvv vvvv vvvv vvvv**  
# 15ビット目がゼロ、0～14ビットは数値orシンボルのアドレス値
# 
# #### C命令  
# **111a cccc ccdd djjj**  
# dest=comp;jump  
# ※関数を作成する際、変換する前に空白を削除しておく  
# 
# |パターン|comp|
# |:--:|:--:|
# |0|0101010|
# |1|0111111|
# |-1|0111010|
# |D|0001100|
# |A|0110000|
# |!D|0001101|
# |!A|0110001|
# |-D|0001111|
# |-A|0110011|
# |D+1|0011111|
# |A+1|0110111|
# |D-1|0001110|
# |A-1|0110010|
# |D+A|0000010|
# |D-A|0010011|
# |A-D|0000111|
# |D&A|0000000|
# |D\|A|0010101|
# |M|1110000|
# |!M|1110001|
# |-M|1110011|
# |M+1|1110111|
# |M-1|1110010|
# |D+M|1000010|
# |D-M|1010011|
# |M-D|1000111|
# |D&M|1000000|
# |D\|M|1010101|
# 
# |パターン|dest|
# |:--:|:--:|
# |null|000|
# |M|001|
# |D|010|
# |MD|011|
# |A|100|
# |AM|101|
# |AD|110|
# |AMD|111|
# 
# |パターン|jump|
# |:--:|:--:|
# |null|000|
# |JGT|001|
# |JEQ|010|
# |JGE|011|
# |JLT|100|
# |JNE|101|
# |JLE|110|
# |JMP|111|
# 
# ### シンボル  
# ・RAMに定義する  
# ・定義済みのシンボル  
# 
# |ラベル|RAMアドレス|  
# |---|---|  
# |SP|0|
# |LCL|1|
# |ARG|2|
# |THIS|3|
# |THAT|4|
# |R0~R15|0~15|
# |SCREEN|16384|
# |KBD|24576|  
# 
# ・ **ラベルシンボル(Xxx)** はシンボル名と次のプログラム行をテーブルに保存。プログラム内で使う。  
# ・ **変数シンボル** はRAMに箱を用意する。RAMアドレスは16(0x0010)から開始。  
# ### 記述  
# ・コメントは"//" 無視する。  
# ・空白は無視する。  
# ・"@xx"は変数or定数。数字なら定数。

# ### Symbolテーブル

# In[53]:


class symbolTable:
    def __init__(self):
        self.clear()
        
    def clear(self):
        self.tbl = {}
        initSymbol =[['SP',    '0000000000000000'],
                     ['LCL',   '0000000000000001'],
                     ['ARG',   '0000000000000010'],
                     ['THIS',  '0000000000000011'],
                     ['THAT',  '0000000000000100'],
                     ['R0',    '0000000000000000'],
                     ['R1',    '0000000000000001'],
                     ['R2',    '0000000000000010'],
                     ['R3',    '0000000000000011'],
                     ['R4',    '0000000000000100'],
                     ['R5',    '0000000000000101'],
                     ['R6',    '0000000000000110'],
                     ['R7',    '0000000000000111'],
                     ['R8',    '0000000000001000'],
                     ['R9',    '0000000000001001'],
                     ['R10',   '0000000000001010'],
                     ['R11',   '0000000000001011'],
                     ['R12',   '0000000000001100'],
                     ['R13',   '0000000000001101'],
                     ['R14',   '0000000000001110'],
                     ['R15',   '0000000000001111'],                     
                     ['SCREEN','0100000000000000'],
                     ['KBD',   '0110000000000000'],
                    ]
        self.tbl = dict(initSymbol)
        self.idx = 16
        
    def isExist(self, nm):
        '''シンボルが存在するかチェックする'''
        return nm in self.tbl
    
    def get(self, nm):
        '''シンボル名を取得する。存在しない場合は空白'''
        retValue = ''
        isExist = self.isExist(nm)
        if isExist:
            retValue = self.tbl[nm]
        return isExist, retValue 

    def setIdx(self, nm, idx):
        '''新しいシンボルを登録する。登録したデータを返す'''
        if self.isExist(nm):
            return False, ''
        
        self.tbl[nm] = format(idx, '016b')
        return True, self.tbl[nm]
            
    def setInc(self, nm):
        '''新しいシンボルを登録する。登録したデータを返す'''
        if self.isExist(nm):
            return False, ''
        
        self.tbl[nm] = format(self.idx, '016b')
        self.idx += 1
        return True, self.tbl[nm]
        
        


# ### Parser関数  
# 変換用のリストテーブル。以下の項目で一つのリスト  
# 
# | | |
# |:--:|:--:|
# |command|True:C命令, False: A命令|
# |symbol|A命令のとき保存|
# |comp|C命令のとき保存|
# |dest|C命令のとき保存|
# |jump|C命令のとき保存|
# 
# 

# In[57]:


compList = [
    ['0', '0101010'], 
    ['1', '0111111'], 
    ['-1', '0111010'], 
    ['D', '0001100'], 
    ['A', '0110000'], 
    ['!D', '0001101'], 
    ['!A', '0110001'], 
    ['-D', '0001111'], 
    ['-A', '0110011'], 
    ['D+1', '0011111'], 
    ['A+1', '0110111'], 
    ['D-1', '0001110'], 
    ['A-1', '0110010'], 
    ['D+A', '0000010'], 
    ['D-A', '0010011'], 
    ['A-D', '0000111'], 
    ['D&A', '0000000'], 
    ['D|A', '0010101'], 
    ['M', '1110000'], 
    ['!M', '1110001'], 
    ['-M', '1110011'], 
    ['M+1', '1110111'], 
    ['M-1', '1110010'], 
    ['D+M', '1000010'], 
    ['D-M', '1010011'], 
    ['M-D', '1000111'], 
    ['D&M', '1000000'], 
    ['D|M', '1010101'],
]
tblComp = dict(compList)

destList = [
    ['', '000'], 
    ['M', '001'], 
    ['D', '010'], 
    ['MD', '011'], 
    ['A', '100'], 
    ['AM', '101'], 
    ['AD', '110'], 
    ['AMD', '111'], 
]
tblDest = dict(destList)

jumpList = [
    ['', '000'], 
    ['JGT', '001'], 
    ['JEQ', '010'], 
    ['JGE', '011'], 
    ['JLT', '100'], 
    ['JNE', '101'], 
    ['JLE', '110'], 
    ['JMP', '111'],
]
tblJump = dict(jumpList)

def parser(code, st, codeIdx):
    '''コードを解析する'''
    # 空白を削除する
    code = code.replace('\n', '')
    code = code.replace(' ', '')
    # コメント、空白行は読み込まない
    if '//' in code[0:2]:
        return False, []
    if len(code) == 0:
        return False, []
    # コードの後ろにあるコメントを削除
    if '//' in code:
        code = code.split('/')[0]
    print(code)
    # シンボル(Xxx)はテーブルに登録、プログラムソースの行数を保存する
    # 変換用テーブルには登録しない
    if '(' in code:
        s = code.replace('(', '').replace(')', '')
        st.setIdx(s, codeIdx)
        return False, []
    
    # シンボル@Xxxは変換用テーブルに登録
    if '@' in code:
        s = code.replace('@', '')
        return True, [False, s, '', '', '']
    
    # 残りはC命令
    dest = ''
    if '=' in code:
        tmpCodeSplit = code.split('=')
        dest = tmpCodeSplit[0]
        code = tmpCodeSplit[1]
    jump = ''
    if ';' in code:
        tmpCodeSplit = code.split(';')
        jump = tmpCodeSplit[1]
        code = tmpCodeSplit[0]
    comp = code
    return True, [True, '', tblComp[comp], tblDest[dest], tblJump[jump]]
    
def getAssembleCode(l, st):
    '''変換したデータを取得する'''
    # C命令
    if l[0] is True:
        return '111' + l[2] + l[3] + l[4]
    
    # A命令
    symbol = l[1]
    # 数値の場合、2進数に変換して返す
    if symbol.isdecimal():
        return format(int(symbol), '016b')
    
    if st.isExist(symbol):
        isGet, value = st.get(symbol)
        return value
    else:
        isGet, value = st.setInc(symbol)
        return value
    


# ### メイン関数

# In[54]:


import sys
def main(inputFn):
    '''バイナリファイル(.hack)に変換する'''
    outputFn = inputFn.replace('.asm', '.hack')
    if not '.hack' in outputFn:
        return False
    
    st = symbolTable()
    
    # 1回目 ファイルを読み込んで変換用のテーブルに登録する
    chgList = list()
    codeIdx = 0
    with open(inputFn, 'r') as fin:
        lines = fin.readlines()
        for l in lines:
            isGet, tmpList = parser(l, st, codeIdx)
            if isGet:
                chgList.append(tmpList)
                codeIdx += 1

    # 2回目 ファイルに出力する
    with open(outputFn, 'w') as fout:
        for l in chgList:
            v = getAssembleCode(l, st)
            print(v)
            fout.write(v)
            fout.write('\n')

    return True

if __name__ == '__main__':
    fn = sys.argv[1]
    isAssemble = main(fn)
    print(isAssemble)


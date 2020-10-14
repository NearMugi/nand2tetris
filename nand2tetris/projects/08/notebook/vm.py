#!/usr/bin/env python
# coding: utf-8

# # VM変換器  
# .vmファイル(群)を.asmファイルに変換する  
# 7章の続き

# ## 仕様  
# 
# ### コマンドの種類  
# |||
# |:--|:--|  
# |算術コマンド|スタック上で算術演算と論理演算を行う|
# |メモリアクセスコマンド|スタックとバーチャルメモリ領域の間でデータの転送を行う|
# |プログラムフローコマンド|条件付き分岐処理または無条件の分岐処理を行う|
# |関数呼び出しコマンド|関数呼び出しとそれらからのリターンを行う|
# 
# 
# ### コマンドの構成  
# ・VMコマンドのフォーマットは3パターン  
# * command   
# * command arg   
# * command arg1 arg2  
# 
# ・コメントは"//" "//"以降無視する。  
# ・空白は無視する。  
# ・trueは"-1"、falseは"0"
# 
# 

# ### 算術コマンド  
# 
# |コマンド|戻り値|コメント|
# |:--:|:--|:--|
# |add|x+y|D=D+M|
# |sub|x-y|D=D-M|
# |neg|-y|M=-M|
# |eq|x=yのときtrue、それ以外false|D;JEQ|
# |gt|x>yのときtrue、それ以外false|D;JGT|
# |lt|x<yのときtrue、それ以外false|D;JLT|
# |and|x And y|D=D&M|
# |or|x Or y|D=D\|M|
# |not|Not y|!M|
# 
# コマンドごとに書き方は決まっている。基本形を定義して必要に応じて差し替える。

# In[1]:


class arithmeticCommand():
    '''算術コマンドの変換'''

    def __init__(self):
        # 変数2個のパターン 
        # 1. SPアドレスを取得 -> 2つ戻る -> 値取得 
        # 2. 算術
        # 3. SPアドレスを1つ戻す -> 値を2つ戻したところに保存する
        cmdArg2_H = "@SP\nA=M\nA=A-1\nA=A-1\nD=M\nA=A+1\n"
        cmdArg2_F = "@SP\nM=M-1\nA=M\nA=A-1\nM=D\n"

        # 条件付き分岐のパターン
        cmdBunki_H = "D=D-M\n@BUNKI_TRUE_000\n"
        cmdBunki_F = "D=0\n@BUNKI_END_000\n0;JMP\n(BUNKI_TRUE_000)\nD=-1\n(BUNKI_END_000)\n"        

        # 変数1個のパターン
        # 1. SPアドレスを取得 -> 1つ戻る 
        # 2. 算術
        # ※SPアドレスは変化しない。
        cmdArg1 = "@SP\nA=M\nA=A-1\n"

        cmdAdd = cmdArg2_H + "D=D+M\n" + cmdArg2_F
        cmdSub = cmdArg2_H + "D=D-M\n" + cmdArg2_F
        cmdNeg = cmdArg1 + "M=-M\n"
        cmdEq = cmdArg2_H + cmdBunki_H + "D;JEQ\n" + cmdBunki_F + cmdArg2_F
        cmdGt = cmdArg2_H + cmdBunki_H + "D;JGT\n" + cmdBunki_F + cmdArg2_F
        cmdLt = cmdArg2_H + cmdBunki_H + "D;JLT\n" + cmdBunki_F + cmdArg2_F
        cmdAnd = cmdArg2_H + "D=D&M\n" + cmdArg2_F
        cmdOr = cmdArg2_H + "D=D|M\n" + cmdArg2_F
        cmdNot = cmdArg1 + "M=!M\n"

        tmpList = [
            ["add", cmdAdd],
            ["sub", cmdSub],
            ["neg", cmdNeg],
            ["eq", cmdEq],
            ["gt", cmdGt],
            ["lt", cmdLt],
            ["and", cmdAnd],
            ["or", cmdOr],
            ["not", cmdNot],
        ]
        self.dict = dict(tmpList)
        self.idx = 0

    def isExist(self, ptn):
        '''存在するかチェックする'''
        return ptn in self.dict
    
    def get(self, ptn):
        '''コマンドを取得する。存在しない場合は空白'''
        retValue = ''
        isExist = self.isExist(ptn)
        if isExist:
            retValue = self.dict[ptn]
            # 分岐で使うシンボルが一意になるようにrename
            if ptn == "eq" or ptn == "gt" or ptn == "lt":
                retValue = retValue.replace("000", format(self.idx, '03x'))
                self.idx += 1
        return isExist, retValue     

if __name__ != '__main__':
    ac = arithmeticCommand()
    isGet, cmd = ac.get("eq")
    print(cmd)
    isGet, cmd = ac.get("lt")
    print(cmd)


# ### メモリアクセスコマンド  
# 
# 

# In[2]:


class memoryAccessCommand():
    '''メモリアクセスコマンドの変換'''

    def __init__(self):
        # Push パターン
        # 1. index値をセット
        # 2. 取得元のアドレスを取得
        # 3. スタックに追加 -> SPを1つ進ませる
        cmdPush_H = "@INDEX\nD=A\n"
        cmdPush_F = "@SP\nA=M\nM=D\n@SP\nM=M+1\n"

        tmpPushList = [
            ["argument", cmdPush_H + "@ARG\nA=D+M\nD=M\n" + cmdPush_F],
            ["local", cmdPush_H + "@LCL\nA=D+M\nD=M\n" + cmdPush_F],
            ["static", cmdPush_H + "@FN.INDEX\nA=D+A\nD=M\n" + cmdPush_F],
            ["constant", cmdPush_H + cmdPush_F],
            ["this", cmdPush_H + "@THIS\nA=D+M\nD=M\n" + cmdPush_F],
            ["that", cmdPush_H + "@THAT\nA=D+M\nD=M\n" + cmdPush_F],
            ["pointer", cmdPush_H + "@3\nA=D+A\nD=M\n" + cmdPush_F],
            ["temp", cmdPush_H + "@5\nA=D+A\nD=M\n" + cmdPush_F],
        ]
        self.dictPush = dict(tmpPushList)

        # Pop パターン
        # 1. baseアドレスを取得 -> index分加算 -> スタックに保存
        # 2. SPを1つ戻す -> スタックデータを取得 -> 1.のアドレスにデータをセット
        # 3. SPを1つ戻す
        cmdPop = "@INDEX\nD=D+A\n@SP\nA=M\nM=D\n"
        cmdPop += "@SP\nA=M\nA=A-1\nD=M\nA=A+1\nA=M\nM=D\n"
        cmdPop += "@SP\nM=M-1\n"

        tmpPopList = [
            ["argument", "@ARG\nD=M\n" + cmdPop],
            ["local", "@LCL\nD=M\n" + cmdPop],
            ["static", "@FN.INDEX\nD=A\n" + cmdPop],
            ["constant", "D=0\n" + cmdPop],
            ["this", "@THIS\nD=M\n" + cmdPop],
            ["that", "@THAT\nD=M\n" + cmdPop],
            ["pointer", "@3\nD=A\n" + cmdPop],
            ["temp", "@5\nD=A\n" + cmdPop],
        ]
        self.dictPop = dict(tmpPopList)

    def isExist(self, ptn):
        '''存在するかチェックする'''
        return ptn in self.dictPush
    
    def get(self, ptn, seg, index, fn):
        '''コマンドを取得する。存在しない場合は空白'''
        retValue = ''
        isExist = self.isExist(seg)
        if isExist:
            if ptn == 'push':   
                retValue = self.dictPush[seg]
            if ptn == 'pop':
                retValue = self.dictPop[seg]
            retValue = retValue.replace('INDEX', index).replace('FN', fn)
        return isExist, retValue     

if __name__ != '__main__':
    mac = memoryAccessCommand()
    ptn, seg, index, fn = ("push", "static", "7", "hoge")
    isGet, cmd = mac.get(ptn, seg, index, fn)
    print(cmd)


# ## プログラムフローコマンド  
# 
# |コマンド|コメント|
# |:--:|:--|
# |label xxx|現在の位置をラベル付けする|
# |goto xxx|無条件の移動命令|
# |if-goto xxx|条件付きの移動命令。スタックの最上位の値をポップし、その値がゼロでなければ移動する|

# In[29]:


class programFlowCommand():
    '''プログラムフローコマンドの変換'''
    def __init__(self):
        self.cmdLabel = "(LABEL)\n"
        self.cmdGoto = "@LABEL\n0;JMP\n"
        # 1. スタックの最上位データを取得する
        # 2. SPを1つ戻す
        # 3. 最上位データがゼロでなければ移動する
        self.cmdIfGoto = "@SP\nA=M\nA=A-1\nD=M\n"
        self.cmdIfGoto += "@SP\nM=M-1\n"
        self.cmdIfGoto += "@LABEL\nD;JNE\n"
    
    def get(self, ptn, label):
        '''コマンドを取得する。存在しない場合は空白'''
        if ptn == 'label':
            cmd = self.cmdLabel
            retValue = cmd.replace('LABEL', label)
            return True, retValue 

        if ptn == 'goto':
            cmd = self.cmdGoto
            retValue = cmd.replace('LABEL', label)
            return True, retValue 
        
        if ptn == 'if-goto':
            cmd = self.cmdIfGoto
            retValue = cmd.replace('LABEL', label)
            return True, retValue 
        
        return False, '' 

if __name__ != '__main__':
    pfc = programFlowCommand()
    


# ## 関数呼び出しコマンド  
# 
# |コマンド|コメント|
# |:--:|:--|
# |function f n|n個のローカル変数を持つfという名前の関数を定義する|
# |call f m|fという関数を呼ぶ。m個の引数はスタックにプッシュ済み|
# |return|呼び出し元へリターンする|

# In[46]:


class functionCallCommand():
    '''関数呼び出しコマンドの変換'''
    def __init__(self):
        # function f n
        # 1. 関数のラベルを宣言
        # 2. ローカル変数の個数分だけスタックにPush＆初期化
        self.cmdFunction = "(LABEL)\n"
        self.cmdFunctionPush = "@SP\nA=M\nM=0\n@SP\nM=M+1\n"
        
        # return
        # 1. スタックを戻す
        #    ARGの位置に返値セット、SPをARG+1にする
        # 2. LCLをR13に保存しておく
        # 3. 呼び出し元アドレスをR14に保存しておく
        # 4. 呼び出し元のLCL～THATに戻す
        #    LCLの位置から-1～-4に呼び出し元の値が入っている
        # 5. 2.で保存した呼び出し側のアドレスに移動する
        self.cmdReturn = "// 1\n"
        self.cmdReturn += "@SP\nA=M\nA=A-1\nD=M\n@ARG\nA=M\nM=D\n@ARG\nD=M\n@SP\nM=D+1\n"
        self.cmdReturn += "// 2\n"
        self.cmdReturn += "@LCL\nD=M\n@R13\nM=D\n"
        self.cmdReturn += "// 3\n"
        self.cmdReturn += "@R13\nD=M\n@5\nA=D-A\nD=M\n@R14\nM=D\n"
        self.cmdReturn += "// 3\n"
        self.cmdReturn += "@R13\nD=M\n@1\nA=D-A\nD=M\n@THAT\nM=D\n"
        self.cmdReturn += "@R13\nD=M\n@2\nA=D-A\nD=M\n@THIS\nM=D\n"
        self.cmdReturn += "@R13\nD=M\n@3\nA=D-A\nD=M\n@ARG\nM=D\n"
        self.cmdReturn += "@R13\nD=M\n@4\nA=D-A\nD=M\n@LCL\nM=D\n"
        self.cmdReturn += "// 4\n"
        self.cmdReturn += "@R14\nA=M\n0;JMP\n"
        
    def get3Args(self, ptn, func, cnt):
        '''コマンドを取得する。存在しない場合は空白'''
        if ptn == 'function':
            retValue = self.cmdFunction
            retValue = retValue.replace("LABEL", func)
            for i in range(int(cnt)):
                retValue += self.cmdFunctionPush
            return True, retValue 

        if ptn == 'call':
            retValue = ''
            return True, retValue 
        
        return False, '' 
    def get1Args(self, ptn):
        '''コマンドを取得する。存在しない場合は空白'''
        if ptn == 'return':
            retValue = self.cmdReturn
            return True, retValue 
        return False, ''     


# ### パース

# In[7]:


def parse(ac, mac, pfc, fcc, l, fn):
    '''1行分のデータを解析してasmコマンドを返す  
    ac : 算術コマンドクラス
    mac : メモリアクセスコマンドクラス
    pfc : プログラムフローコマンドクラス
    fcc : 関数呼び出しコマンドクラス
    l : 入力データ(1行分)
    fn : 出力ファイル名 (メモリアクセスコマンドのstaticで使用)
    '''
    # 改行を削除・2文字以上の空白を1文字に変換・コメント行を削除
    l = l.replace('\n', '')
    l = l.replace('  ', ' ')
    if '//' in l:
        l = l.split('//')[0]    
        
    # 前後の空白行を削除＆空白行で分割
    cmd = l.strip().split(' ')
    
    isGet = False
    retCmd = ''
    if len(cmd) == 1:
        isGet, retCmd = ac.get(cmd[0])
        if not isGet:
            isGet, retCmd = fcc.get1Args(cmd[0])

    if len(cmd) == 2:
        isGet, retCmd = pfc.get(cmd[0], cmd[1])

    if len(cmd) == 3:
        isGet, retCmd = mac.get(cmd[0], cmd[1], cmd[2], fn)
        if not isGet:
            isGet, retCmd = fcc.get3Args(cmd[0], cmd[1], cmd[2])

    return isGet, retCmd

if __name__ != '__main__':
    ac = arithmeticCommand()
    mac = memoryAccessCommand()
    fn = "hoge"    
    l = "push constant 7\n"
    print(parse(ac, mac, l, fn))

    l = "add\n"
    print(parse(ac, mac, l, fn))


# In[47]:


import sys
import re
import os
def main(folderPath):
    '''フォルダ内の.vmファイルをアセンブラファイル(.asm)に変換する'''
    
    # フォルダ内にvmファイルがあるかチェックする
    files = os.listdir(folderPath)
    files_file = [f for f in files if os.path.isfile(os.path.join(folderPath, f))]
    vmFiles = [f for f in files_file if ".vm" in f]
    
    if len(vmFiles) <= 0:
        return False

    inputFn = list()
    inputLines = list()
    # Sys.vm を取得する
    if "Sys.vm" in vmFiles:
        # ファイル名をリストに保存
        inputFn.append("Sys")
        with open(os.path.join(folderPath, "Sys.vm"), 'r') as fin:
            # ファイルの中身をリストに保存
            inputLines.append(fin.readlines())
            
    # Sys.vm 以外を取得する
    vmFiles = [f for f in vmFiles if not "Sys.vm" in f]
    for fn in vmFiles:
        # ファイル名をリストに保存
        inputFn.append(fn.replace('.vm', ''))
        with open(os.path.join(folderPath, fn), 'r') as fin:
            # ファイルの中身をリストに保存
            inputLines.append(fin.readlines())        
    #print(inputFn)
    #print(inputLines)
    
    # asmファイル名を指定    
    outputFn = folderPath.split('/')
    outputFn = outputFn[len(outputFn)-1] + ".asm"
    outputFn = os.path.join(folderPath, outputFn)
    
    ac = arithmeticCommand()
    mac = memoryAccessCommand()
    pfc = programFlowCommand()
    fcc = functionCallCommand()

    with open(outputFn, 'w') as fout:
        for fn, lines in zip(inputFn, inputLines):
            for l in lines:
                isGet, tmpList = parse(ac, mac, pfc, fcc, l, fn)
                if isGet:
                    fout.write("// " + l + tmpList)

    return True

if __name__ == '__main__':
    #folderPath = sys.argv[1]
    #folderPath = "D:/#WorkSpace/nand2tetris/nand2tetris/projects/08/ProgramFlow/FibonacciSeries"
    folderPath = "D:/#WorkSpace/nand2tetris/nand2tetris/projects/08/FunctionCalls/SimpleFunction"
    isAssemble = main(folderPath)
    print(isAssemble)


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
        # 1. SP - 1を取得 -> 値をR13に保存
        # 2. SPを1つ戻す        
        # 3. SP - 1を取得 -> 値をDに保存
        # 4. R13とDの値で算術
        # 5. SP - 1を取得 -> 値を保存
        cmdArg2_H = "@SP // 1\nA=M-1\nD=M\n@R13\nM=D\n"
        cmdArg2_H += "@SP // 2\nM=M-1\n"
        cmdArg2_H += "@SP // 3\nA=M-1\nD=M\n"
        
        cmdArg2_F = "@SP // 5\nA=M-1\nM=D\n"

        # 条件付き分岐のパターン
        # 4-1. R13 - D
        # 4-2. 分岐
        # 4-3-False. SP - 1を取得 -> ゼロを保存 -> ENDへJump
        # 4-3-True. SP - 1を取得 -> -1を保存
        
        cmdBunki_H = "@R13 // 4-1\nD=D-M\n"
        cmdBunki_F = "@SP // 4-3-False\nA=M-1\nM=0\n@BUNKI_END_000\n0;JMP\n"
        cmdBunki_F += "(BUNKI_TRUE_000) // 4-3-True\n@SP\nA=M-1\nM=-1\n(BUNKI_END_000)\n"        

        # 変数1個のパターン
        # 1. SP - 1を取得  -> 1つ戻る 
        # 2. 算術
        # ※SPアドレスは変化しない。
        cmdArg1 = "@SP // 1\nA=M-1\n"

        cmdAdd = cmdArg2_H + "@R13 // 4\nD=D+M\n" + cmdArg2_F
        cmdSub = cmdArg2_H + "@R13 // 4\nD=D-M\n" + cmdArg2_F
        cmdNeg = cmdArg1 + "M=-M // 2\n"
        cmdEq = cmdArg2_H + cmdBunki_H + "@BUNKI_TRUE_000 // 4-2\nD;JEQ\n" + cmdBunki_F
        cmdGt = cmdArg2_H + cmdBunki_H + "@BUNKI_TRUE_000 // 4-2\nD;JGT\n" + cmdBunki_F
        cmdLt = cmdArg2_H + cmdBunki_H + "@BUNKI_TRUE_000 // 4-2\nD;JLT\n" + cmdBunki_F
        cmdAnd = cmdArg2_H + "@R13 // 4\nD=D&M" + cmdArg2_F
        cmdOr = cmdArg2_H + "@R13 // 4\nD=D|M\n" + cmdArg2_F
        cmdNot = cmdArg1 + "M=!M // 2\n"

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
        # 1. 取得元のアドレスを取得
        # 2. index値を加算 -> そのアドレスの値を取得
        # 3. スタックに追加 
        # 4. SPを1つ進ませる
        cmdPushAddIdx = "@INDEX // 2\nA=D+A\nD=M\n"
        cmdPushAddStack = "@SP // 3\nA=M\nM=D\n"
        cmdPushAddStack += "@SP // 4\nM=M+1\n"

        tmpPushList = [
            ["argument", "@ARG\nD=M\n" + cmdPushAddIdx + cmdPushAddStack],
            ["local", "@LCL\nD=M\n" + cmdPushAddIdx + cmdPushAddStack],
            ["static", "@FN.static.INDEX\nD=M\n" + cmdPushAddStack],
            ["constant", "@INDEX\nD=A\n" + cmdPushAddStack],
            ["this", "@THIS\nD=M\n" + cmdPushAddIdx + cmdPushAddStack],
            ["that", "@THAT\nD=M\n" + cmdPushAddIdx + cmdPushAddStack],
            ["pointer", "@3\nD=M\n" + cmdPushAddIdx + cmdPushAddStack],
            ["temp", "@5\nD=M\n" + cmdPushAddIdx + cmdPushAddStack],
        ]
        self.dictPush = dict(tmpPushList)

        # Pop パターン
        # 1. baseアドレスを取得 -> index分加算 -> R13に保存
        # 2. SPを1つ戻す -> スタックデータを取得 -> 1.のアドレスにデータをセット
        # 3. SPを1つ戻す
        cmdPop = "@INDEX\nD=D+A\n@R13\nM=D\n"
        cmdPop += "@SP\nA=M-1\nD=M\n@R13\nA=M\nM=D\n"
        cmdPop += "@SP\nM=M-1\n"

        tmpPopList = [
            ["argument", "@ARG\nD=M\n" + cmdPop],
            ["local", "@LCL\nD=M\n" + cmdPop],
            ["static", "@SP\nA=M-1\nD=M\n@FN.static.INDEX\nM=D\n@SP\nM=M-1\n"],
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

# In[3]:


class programFlowCommand():
    '''プログラムフローコマンドの変換'''
    def __init__(self):
        self.cmdLabel = "(LABEL)\n"
        self.cmdGoto = "@LABEL\n0;JMP\n"
        # 1. スタックの最上位データを取得する
        # 2. SPを1つ戻す
        # 3. 最上位データがゼロでなければ移動する
        self.cmdIfGoto = "@SP\nAM=M-1\n"
        self.cmdIfGoto += "D=M\n@LABEL\nD;JNE\n"
    
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

# In[4]:


class functionCallCommand():
    '''関数呼び出しコマンドの変換'''
    def __init__(self):
        # function f n
        # 1. 関数のラベルを宣言
        # 2. ローカル変数の個数分だけスタックにPush＆初期化
        self.cmdFunction = "(LABEL)\n"
        self.cmdFunctionPush = "@SP\nA=M\nM=0\n@SP\nM=M+1\n"
        
        # call f m
        # 1. リターンラベルを設定してスタックにPush
        # 2. LCL～THATをスタックにPush
        # 3. ARGにSP - (n + 5) をセット
        # 4, LCLに SP をセット
        # 5. functionに移動
        # 6. リターンラベルをセット
        cmdPush = "@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        self.cmdCall = "@FUNC-ret // 1\nD=A\n" + cmdPush
        self.cmdCall += "@LCL // 2\nD=M\n" + cmdPush
        self.cmdCall += "@ARG\nD=M\n" + cmdPush
        self.cmdCall += "@THIS\nD=M\n" + cmdPush
        self.cmdCall += "@THAT\nD=M\n" + cmdPush
        self.cmdCall += "@5 // 3\nD=A\n@CNT\nD=D+A\n@SP\nD=M-D\n@ARG\nM=D\n"
        self.cmdCall += "@SP // 4\nD=M\n@LCL\nM=D\n"
        self.cmdCall += "@FUNC // 5\n0;JMP\n"
        self.cmdCall += "(FUNC-ret) // 6\n"
        
        # return
        # 1. LCLをR13に保存しておく
        # 2. 呼び出し元アドレスをR14に保存しておく
        # 3. スタックを戻す
        #    ARGの位置に返値セット、SPをARG+1にする
        # 4. 呼び出し元のLCL～THATに戻す
        #    LCLの位置から-1～-4に呼び出し元の値が入っている
        # 5. 2.で保存した呼び出し側のアドレスに移動する
        self.cmdReturn = "@LCL // 1\nD=M\n@R13\nM=D\n"
        self.cmdReturn += "@R13 // 2\nD=M\n@5\nA=D-A\nD=M\n@R14\nM=D\n"
        self.cmdReturn += "@SP // 3\nA=M-1\nD=M\n@ARG\nA=M\nM=D\n@ARG\nD=M+1\n@SP\nM=D\n"
        self.cmdReturn += "@R13 // 4\nA=M-1\nD=M\n@THAT\nM=D\n"
        self.cmdReturn += "@R13\nD=M\n@2\nA=D-A\nD=M\n@THIS\nM=D\n"
        self.cmdReturn += "@R13\nD=M\n@3\nA=D-A\nD=M\n@ARG\nM=D\n"
        self.cmdReturn += "@R13\nD=M\n@4\nA=D-A\nD=M\n@LCL\nM=D\n"
        self.cmdReturn += "@R14 // 5\nA=M\n0;JMP\n"
        
    def get3Args(self, ptn, func, cnt):
        '''コマンドを取得する。存在しない場合は空白'''
        if ptn == 'function':
            retValue = self.cmdFunction
            retValue = retValue.replace("LABEL", func)
            for i in range(int(cnt)):
                retValue += self.cmdFunctionPush
            return True, retValue 

        if ptn == 'call':
            retValue = self.cmdCall
            retValue = retValue.replace("FUNC", func)
            retValue = retValue.replace("CNT", cnt)
            return True, retValue 
        
        return False, '' 
    def get1Args(self, ptn):
        '''コマンドを取得する。存在しない場合は空白'''
        if ptn == 'return':
            retValue = self.cmdReturn
            return True, retValue 
        return False, ''     


# ### パース

# In[5]:


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
        # Sys専用
        if cmd[0] == "bootStrap":
            isGet = True
            retCmd = "@256\nD=A\n@SP\nM=D\n"
        if not isGet:
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


# In[8]:


import sys
import re
import os
def flatten(nested_list):
    """2重のリストをフラットにする関数"""
    return [e for inner_list in nested_list for e in inner_list]

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
        # Sys 専用コマンドを先頭に追加
        inputLines += [["bootStrap\n", "call Sys.init 0\n"]]
        with open(os.path.join(folderPath, "Sys.vm"), 'r') as fin:
            # ファイルの中身をリストに保存
            inputLines.append(fin.readlines())            
        # 一度多重リストをフラットにしてまた多重リストにする
        inputLines = [flatten(inputLines)]
        
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
    folderPath = "D:/#WorkSpace/nand2tetris/nand2tetris/projects/08/FunctionCalls/"
    
    fn = "SimpleFunction"
    isAssemble = main(folderPath + fn)
    print(fn, isAssemble)
    
    fn = "StaticsTest"
    isAssemble = main(folderPath + fn)
    print(fn, isAssemble)
    
    fn = "NestedCall"
    isAssemble = main(folderPath + fn)
    print(fn, isAssemble)
    
    fn = "FibonacciElement"
    isAssemble = main(folderPath + fn)
    print(fn, isAssemble)
    


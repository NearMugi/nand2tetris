#!/usr/bin/env python
# coding: utf-8

# # VM変換器  
# .vmファイル(群)を.asmファイルに変換する

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

# In[16]:


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

# In[26]:


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


# ### パース

# In[39]:


import re
def parse(ac, mac, l, fn):
    '''1行分のデータを解析してasmコマンドを返す  
    ac : 算術コマンドクラス
    mac : メモリアクセスコマンドクラス
    l : 入力データ(1行分)
    fn : 出力ファイル名 (メモリアクセスコマンドのstaticで使用)
    '''
    # 改行を削除・2文字以上の空白を1文字に変換・コメント行を削除
    l = l.replace('\n', '')
    l = l.replace('  ', ' ')
    l = re.sub('//*', '', l)

    cmd = l.split(' ')
    isGet = False
    retCmd = ''
    if len(cmd) == 1:
        isGet, retCmd = ac.get(cmd[0])

    if len(cmd) == 2:
        pass

    if len(cmd) == 3:
        isGet, retCmd = mac.get(cmd[0], cmd[1], cmd[2], fn)

    return isGet, retCmd

if __name__ != '__main__':
    ac = arithmeticCommand()
    mac = memoryAccessCommand()
    fn = "hoge"    
    l = "push constant 7\n"
    print(parse(ac, mac, l, fn))

    l = "add\n"
    print(parse(ac, mac, l, fn))


# In[1]:


import sys
import re
def main(inputFn):
    '''アセンブラファイル(.asm)に変換する'''
    outputFn = inputFn.replace('.vm', '.asm')
    if not '.asm' in outputFn:
        return False
    
    ac = arithmeticCommand()
    mac = memoryAccessCommand()
    fn = outputFn.replace('.asm', '')
    fn = fn.split('/')
    fn = fn[len(fn)-1]

    with open(outputFn, 'w') as fout:
        with open(inputFn, 'r') as fin:
            lines = fin.readlines()
            for l in lines:
                isGet, tmpList = parse(ac, mac, l, fn)
                if isGet:
                    fout.write(tmpList)

    return True

if __name__ == '__main__':
    fn = sys.argv[1]
    isAssemble = main(fn)
    print(isAssemble)


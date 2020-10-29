#!/usr/bin/env python
# coding: utf-8

# # トークン化モジュール(Tokenizer)  
# * xxx.jack -> xxxT.xmlに変換する  
# * jackソースをトークン単位に分解する  
# * 解析は別モジュール
# 
# ## 字句要素  
# 
# |word|value|
# |:-|:-|
# |keyword|'class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return'|
# |symbol|'{', '}', '(', ')', '\[', '\]', '.', '\,', ';', '+', '-', '\*', '/', '&', '\|', '<', '>', '=', '~' |
# |integerConstant|0から32767までの10進数の数字|
# |stringConstant|ダブルクォートと改行文字を含まないユニコードの文字列|
# |identifier|アルファベット、数字、アンダースコアの文字列。ただし数字から始まる文字列は除く|
# 

# ## トークン生成クラス

# In[44]:


class createToken:
    tupleKeyword = ('class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return')
    tupleSymbol = ('{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~', )
    
    xmlChangeSymbol = {"<" : "&lt;", ">" : "&gt;", "&" : "&amp;"}
    
    xmlKeyword = "<keyword> @ </keyword>\n"
    xmlSymbol = "<symbol> @ </symbol>\n"
    xmlIntegerConstant = "<integerConstant> @ </integerConstant>\n"
    xmlStringConstant = "<stringConstant> @ </stringConstant>\n"
    xmlIdentifier = "<identifier> @ </identifier>\n"

    def __init__(self):
        pass
    
    def devideSymbol(self, code):
        '''symbolを見つけてばらしてリストを返す'''
        # 空白で分ける
        codes = code.split(' ')
        tokens = list()
        for code in codes:
            t = ""
            for c in code:
                # 1文字ずつチェックしてSymbolを探す
                if c in self.tupleSymbol:
                    if len(t) > 0:
                        tokens.append(t)
                    tokens.append(c)
                    t = ""                
                else:
                    t += c
            if len(t) > 0:
                tokens.append(t)
        return tokens
    
    def getTokens(self, code):
        '''jackファイルの1行をトークンに分ける'''
        # 余計な空白やタブ、改行を削除
        code = code.replace('\n', '')
        code = code.replace('\t', ' ')
        code = code.replace('  ', ' ')
        
        # コードの後ろにあるコメントを削除
        if '//' in code:
            code = code.split('//')[0]
        # コメント、空白行は処理しない
        if '//' in code[0:2]:
            return False, [], []
        if len(code) == 0:
            return False, [], []
        # ダブルクォートあり -> 挟まれているところはスペース含めてStringConstant
        tmpCodes = code.split('\"')
        tokens = list()
        xmls = list()
        if len(tmpCodes) == 3:
            # ダブルクォート前
            codes = self.devideSymbol(tmpCodes[0])
            tokens = codes
            xmls = self.getXml(codes)
            # ダブルクォート内
            codes = tmpCodes[1]
            tokens.append(codes)
            xmls.append(self.xmlStringConstant.replace("@", codes))
            # ダブルクォート後
            codes = self.devideSymbol(tmpCodes[2])
            tokens += codes
            xmls += self.getXml(codes)
        else:
            tokens = self.devideSymbol(tmpCodes[0])
            xmls = self.getXml(tokens)
                    
        return True, tokens, xmls

    def getXml(self, tokens):
        '''トークンをxml形式に変換する。stringConstantは事前に処理している'''
        xmls = list()
        for t in tokens:
            # Keyword
            if t in self.tupleKeyword:
                xmls.append(self.xmlKeyword.replace("@", t))
                continue
            # Symbol
            if t in self.tupleSymbol:
                if t in self.xmlChangeSymbol:
                    t = self.xmlChangeSymbol[t]
                xmls.append(self.xmlSymbol.replace("@", t))
                continue
            # integerConstant
            if t.isnumeric():
                xmls.append(self.xmlIntegerConstant.replace("@", t))
                continue                
            # identifier
            xmls.append(self.xmlIdentifier.replace("@", t))
            
        return xmls
        
if __name__ != "__main__":
    ct = createToken()
    isGet, tokens, xmls = ct.getTokens('j = j / (-2);   // note: unary negate constant 2 \n')
    print(isGet, tokens, xmls)
        
    


# ## ファイル生成

# In[45]:


import os
import sys

def checkFolder(folderPath):
    '''指定したフォルダ内のファイルをチェックしてトークンファイルを出力する'''
    # フォルダ内にjackファイルがあるかチェックする
    files = os.listdir(folderPath)
    files_file = [f for f in files if os.path.isfile(os.path.join(folderPath, f))]
    jackFiles = [f for f in files_file if ".jack" in f]

    if len(jackFiles) <= 0:
        return False
    
    for fn in jackFiles:
        createFile(folderPath, fn)
    return True

def createFile(folderPath, fn):
    '''トークンファイルを生成する'''
    ct = createToken()
    outputFn = fn.split('.')[0] + "T.xml"
    outputFn = os.path.join(folderPath, outputFn)    
    
    isComment = False
    with open(outputFn, 'w') as fout:
        fout.write("<tokens>\n")
        with open(os.path.join(folderPath, fn), 'r') as fin:
            lines = fin.readlines()
            for l in lines:
                # /* ～ */で囲まれているコメントは除外する
                # 複数行に渡る場合がある
                if "/*" in l:
                    isComment = True
                if "*/" in l:
                    isComment = False
                    continue
                if isComment:
                    continue
                    
                isGet, tokens, xmls = ct.getTokens(l)
                if isGet is True:
                    for x in xmls:
                        fout.write(x)
        fout.write("</tokens>\n")

    return True

if __name__ == "__main__":
    checkFolder("./ArrayTest")
    checkFolder("./ExpressionLessSquare")
    checkFolder("./Square")


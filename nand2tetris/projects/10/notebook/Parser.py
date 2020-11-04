#!/usr/bin/env python
# coding: utf-8

# # トークンに分けたファイルを解析する  
# * 出力はxmlファイル  
# * あるキーワード(例えばclass)を見つけたらネストを作っていく  
# * キーワードはトークンのタグで分かる  
# 
# |word|value|
# |:-|:-|
# |keyword|'class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return'|
# 
# * スタックしていく感じでキーワードクラスをネストを管理する
# 

# ## xmlTファイルのフォーマットエラー

# In[1]:


class xmlTFormatException(Exception):
    '''エラーメッセージを表示するだけ'''
    # クラス名
    # Step数
    # メッセージ
    
    pass


# ## classキーワード  
# **class** className **{** classVarDec* subroutineDec* **}**  
# * **class** が来た時に該当  
# * classVarDec, subroutineDecはゼロ以上現れる
# * **{}** で括られている -> **}** が来たら閉じる  

# In[2]:


class keywordClass:
    step = 0
    def __init__(self):
        self.step = 0
    def check(self, line):
        errMsg = ""
        isClose = False
        ret = ""
        if self.step == 0:
            # class
            ret = "<class>\n" + line
            self.step += 1
        elif self.step == 1:
            # className
            ret = line
            self.step += 1
        elif self.step == 2:
            # {
            if " { " in line:
                ret = line
                self.step += 1
            else:
                errMsg = (__class__.__name__, self.step, "{ is missing")
        elif self.step == 3:
            # } or それ以外
            if " } " in line:
                ret = line + "</class>\n"
                isClose = True
            else:
                ret = line
        return errMsg, "", isClose, False, ret


# ## classVarDecキーワード  
# (**static** | **field**) type varName (**,** varName)* **;**  
# * **static or field** が来た時に該当  
# * varNameは2個以上の場合もある
# * **;** が来たら閉じる  

# In[3]:


class keywordClassVarDec:
    step = 0
    def __init__(self):
        self.step = 0
    def check(self, line):
        isClose = False
        ret = ""
        if self.step == 0:
            # static or field
            ret = "<classVarDec>\n" + line
            self.step += 1
        elif self.step == 1:
            # type
            ret = line
            self.step += 1
        elif self.step == 2:
            # varName
            ret = line
            self.step += 1
        elif self.step == 3:
            # , or ;
            if " , " in line:                
                ret = line
                self.step = 2
            if " ; " in line:
                ret = line + "</classVarDec>\n"
                isClose = True
        return "", "", isClose, False, ret    


# ## subroutineDecキーワード  
# (**constructor** | **function** | **method** ) (**void** | type) subroutineName **(** parameterList **)** subroutineBody  
# * **constructor or function or method** が来た時に該当  
# * paremeterListも合わせて処理する ()の中はparameterList 
# * subroutineBody は **{}** で括られている -> **}** が来たら閉じる  
# 
# ### parameterListキーワード  
# ((type varName) (',' type varName)*)?  
# * 関数の引数  
# * ゼロ個のときもある  
# 
# ### subroutineBody  
# **{** varDec* statements **}**  
# * {}の内側、varDec*以下を ＜statements＞＜/statements＞ で括る

# In[4]:


class keywordSubroutineDec:
    step = 0
    def __init__(self):
        self.step = 0
    def check(self, line):
        errMsg = ""
        isClose = False
        ret = ""
        if self.step == 0:
            # constructor or function or method
            ret = "<subroutineDec>\n" + line
            self.step += 1
        elif self.step == 1:
            # void or type
            ret = line
            self.step += 1
        elif self.step == 2:
            # subroutineName
            ret = line
            self.step += 1
        elif self.step == 3:
            # (
            if " ( " in line:
                ret = line + "<parameterList>\n"
                self.step += 1
            else:
                errMsg = (__class__.__name__, self.step, "( is missing")
        elif self.step == 4:
            # )を待つ
            if " ) " in line:
                ret = "</parameterList>\n" + line
                self.step += 1
            else:
                ret = line
        elif self.step == 5:
            # {
            if " { " in line:
                ret = "<subroutineBody>\n" + line
                self.step += 1
            else:
                errMsg = (__class__.__name__, self.step, "{ is missing")
        elif self.step == 6:
            # }を待つ
            if " } " in line:
                ret = "</statements>\n" + line + "</subroutineBody>\n" + "</subroutineDec>\n"
                isClose = True
            else:
                ret = line
        return errMsg, "", isClose, False, ret    


# ## varDecキーワード  
# **var** type varName (',' varName)* **;**  
# * 変数の宣言
# * **;** が来たら閉じる  
# 

# In[5]:


class keywordVarDec:
    step = 0
    def __init__(self):
        self.step = 0
    def check(self, line):
        isClose = False
        ret = ""
        if self.step == 0:
            # var
            ret = "<varDec>\n" + line
            self.step += 1
        elif self.step == 1:
            # type
            ret = line
            self.step += 1
        elif self.step == 2:
            # varName
            ret = line
            self.step += 1
        elif self.step == 3:
            # , or ;
            if " , " in line:                
                ret = line
                self.step = 2
            if " ; " in line:
                ret = line + "</varDec>\n"
                isClose = True
        return "", "", isClose, False, ret   


# ## letStatementキーワード  
# **let** varName (**[** expression **]**)? **=** expression **;**  
# * **let** が来た時に該当  
# * **[** expression **]** が来ることもある  
# * = の後はexpression  
# * **;** が来たら閉じる

# In[6]:


class keywordLetStatement:
    step = 0
    def __init__(self):
        self.step = 0
    def check(self, line):
        errMsg = ""
        nextKeyword = ""
        isClose = False
        ret = ""
        if self.step == 0:
            # let
            ret = "<letStatement>\n" + line
            self.step += 1
        elif self.step == 1:
            # varName
            ret = line
            self.step += 1
        elif self.step == 2:
            # [ 
            if " [ " in line:
                ret = line
                # 次はexpression
                nextKeyword = "expression"
            elif " ] " in line:
                ret = line
            else:
                if "=" in line:
                    ret = line
                    self.step += 1
                    # 次はexpression
                    nextKeyword = "expression"
                else:
                    errMsg = (__class__.__name__, self.step, "= is missing")
        elif self.step == 3:
            if " ; " in line:
                ret = line + "</letStatement>\n"
                isClose = True
            else:
                errMsg = (__class__.__name__, self.step, "; is missing")
        return errMsg, nextKeyword, isClose, False, ret


# ## ifStatementキーワード  
# **if** **(** expression **)** **{** statements **}** (**else** **{** statements **}**)?  
# * **if** が来た時に該当  
# * **else** が来ることもある  
# * **}** が来たら閉じる　※**else** が来ることに注意  
# * elseは別のスタックにする。elseが来たら 追加した＜/ifStatement＞を削除する

# In[7]:


class keywordIfStatement:
    step = 0
    def __init__(self):
        self.step = 0
    def check(self, line):
        errMsg = ""
        nextKeyword = ""
        isClose = False
        isRemain = False
        ret = ""
        if self.step == 0:
            # if
            ret = "<ifStatement>\n" + line
            self.step += 1
        elif self.step == 1:
            # ( 
            if " ( " in line:
                ret = line
                self.step += 1
                # 次はexpression
                nextKeyword = "expression"
            else:
                errMsg = (__class__.__name__, self.step, "( is missing")            
        elif self.step == 2:
            # ) 
            if " ) " in line:
                ret = line
                self.step += 1
            else:
                errMsg = (__class__.__name__, self.step, ") is missing")            
        elif self.step == 3:
            # {
            if " { " in line:
                ret = line + "<statements>\n"
                self.step += 1
            else:
                errMsg = (__class__.__name__, self.step, "{ is missing")            
        elif self.step == 4:
            # } が来たら終了
            if " } " in line:
                ret = "</statements>\n" + line + "</ifStatement>\n"
                isClose = True
            else:
                ret = line
        return errMsg, nextKeyword, isClose, isRemain, ret


# In[8]:


class keywordElseStatement:
    step = 0
    def __init__(self):
        self.step = 0
    def check(self, line):
        errMsg = ""
        nextKeyword = ""
        isClose = False
        isRemain = False
        ret = ""
        if self.step == 0:
            # else
            ret = line
            self.step += 1        
        elif self.step == 1:
            # {
            if " { " in line:
                ret = line + "<statements>\n"
                self.step += 1
            else:
                errMsg = (__class__.__name__, self.step, "{ is missing")            
        elif self.step == 2:
            # } が来たら終了
            if " } " in line:
                ret = "</statements>\n" + line + "</ifStatement>\n"
                isClose = True
            else:
                ret = line
        return errMsg, nextKeyword, isClose, isRemain, ret


# ## whileStatementキーワード  
# **while** **(** expression **)** **{** statements **}**  
# * **while** が来た時に該当  
# * 必ずexpressionが来る  
# * **}** が来たら閉じる

# In[9]:


class keywordWhileStatement:
    step = 0
    def __init__(self):
        self.step = 0
    def check(self, line):
        errMsg = ""
        nextKeyword = ""
        isClose = False
        ret = ""
        if self.step == 0:
            # do
            ret = "<whileStatement>\n" + line
            self.step += 1
        elif self.step == 1:
            # ( 
            if " ( " in line:
                ret = line
                self.step += 1
                # 次はexpression
                nextKeyword = "expression"
            else:
                errMsg = (__class__.__name__, self.step, "( is missing")            
        elif self.step == 2:
            # ) 
            if " ) " in line:
                ret = line
                self.step += 1
            else:
                errMsg = (__class__.__name__, self.step, ") is missing")            
        elif self.step == 3:
            # {
            if " { " in line:
                ret = line + "<statements>\n"
                self.step += 1
            else:
                errMsg = (__class__.__name__, self.step, "{ is missing")            
        elif self.step == 4:
            if " } " in line:
                # 終了
                ret = "</statements>\n" + line + "</whileStatement>\n"
                isClose = True
        return errMsg, nextKeyword, isClose, False, ret


# ## doStatementキーワード  
# **do** subroutineCall **;**  
# * **do** が来た時に該当  
# * **;** が来たら閉じる
# * subroutineCallの形式は決まっている

# In[10]:


class keywordDoStatement:
    step = 0
    def __init__(self):
        self.step = 0
    def check(self, line):
        errMsg = ""
        nextKeyword = ""
        isClose = False
        ret = ""
        if self.step == 0:
            # do
            ret = "<doStatement>\n" + line
            self.step += 1
            nextKeyword = "subroutineCall"
        elif self.step == 1:
            if " ; " in line:
                # 終了
                ret = line + "</doStatement>\n"
                isClose = True
        return errMsg, nextKeyword, isClose, False, ret


# ## returnStatementキーワード  
# **return** expression? **;**  
# * **return** が来た時に該当  
# * expressionが来ることもある  
# * **;** が来たら閉じる

# In[11]:


class keywordReturnStatement:
    step = 0
    def __init__(self):
        self.step = 0
    def check(self, line):
        errMsg = ""
        nextKeyword = ""
        isClose = False
        isRemain = False
        ret = ""
        if self.step == 0:
            # return
            ret = "<returnStatement>\n" + line
            self.step += 1
        elif self.step == 1:
            if " ; " in line:
                ret = line + "</returnStatement>\n"
                isClose = True
            else:
                nextKeyword = "expression"           
                isRemain = True
        return errMsg, nextKeyword, isClose, isRemain, ret   


# ## expressionキーワード  
# term (op term)*  
# * termとセット  
# * term = term のような形式もある  

# In[12]:


class keywordExpression:
    step = 0
    nextTerm = False
    termStackList = list()
    def __init__(self):
        self.step = 0
        self.nextTerm = False
        self.termStackList = list()
    def check(self, line):
        errMsg = ""
        nextKeyword = ""
        isClose = False
        isRemain = False
        ret = ""
        if self.step == 0:
            # expressionListがカラの場合
            if " ) " in line:
                isClose = True
                isRemain = True
            else:
                ret = "<expression>\n"
                self.step += 1
                # term
                nextKeyword = "term"
                isRemain = True
        elif self.step == 1:
            if " + " in line or " - " in line or " * " in line             or " / " in line or " &amp; " in line or " | " in line             or " &lt; " in line or " &gt; " in line or " = " in line:
                ret = line
                # term
                nextKeyword = "term"
                
            else:
                # 終了
                ret = "</expression>\n"
                isClose = True
                isRemain = True

        return errMsg, nextKeyword, isClose, isRemain, ret
    


# In[35]:


class keywordExpressionInTerm:
    step = 0
    nextTerm = False
    termStackList = list()
    def __init__(self):
        self.step = 0
        self.nextTerm = False
        self.termStackList = list()
    def check(self, line):
        errMsg = ""
        nextKeyword = ""
        isClose = False
        isRemain = False
        ret = ""
        if self.step == 0:
            ret = "<expression>\n"
            self.step += 1
            # term
            nextKeyword = "term"
            isRemain = True
        elif self.step == 1:
            if " + " in line or " - " in line or " * " in line             or " / " in line or " &amp; " in line or " | " in line             or " &lt; " in line or " &gt; " in line or " = " in line:
                ret = line
                # term
                nextKeyword = "term"
                
            else:
                # 終了
                ret = "</expression>\n" + line
                isClose = True

        return errMsg, nextKeyword, isClose, isRemain, ret
    


# ## termキーワード  
# integerConstant | stringConstant | keywordConstant | varName | varName**[** expression **]** | subroutineCall | **(** expression **)** | unaryOp term  
# * なんでも来る  
# * subroutineCall もあり得る  
# 
# ### 識別  
# * 1文字目 : ( の場合、次はexpression
# * 2文字目 : \[ の場合、次はexpression ,( or . の場合、subroutineCall それ以外の場合は終了
# * 終了条件 : \], ), ; が来たら処理を終わらせてスタックを削除する＆**ひとつ前のスタックを処理する**

# In[72]:


class keywordTerm:
    step = 0
    def __init__(self):
        self.step = 0
    def check(self, line):
        errMsg = ""
        nextKeyword = ""
        isClose = False
        isRemain = False
        ret = ""
        if self.step == 0:
            ret = "<term>\n" + line
            self.step += 1
            # ( expression ) 
            if " ( " in line:
                # 次はexpression in Term
                nextKeyword = "expressionInTerm"     
            # unaryOp term    
            elif " - " in line or " ~ " in line:
                # 次はterm
                nextKeyword = "term"
        elif self.step == 1:
            # varName[ expression ] 
            if " [ " in line:
                ret = line
                # 次はexpression in Term
                nextKeyword = "expressionInTerm"
            elif " ] " in line:
                # 終了
                ret = "</term>\n"
                isClose = True
                isRemain = True
                
            # ( expression ) 
            elif " ) " in line:
                # 終了
                ret = "</term>\n"
                isClose = True
                isRemain = True                        
                
            # subroutineCall    
            elif " ( " in line:
                ret = line
                # 次はexpressionList
                nextKeyword = "expressionList"
                self.step += 1            
            elif " . " in line:
                ret = line
                self.step += 1            
            else:
                # 終了
                ret = "</term>\n"
                isClose = True
                isRemain = True
        # 以下subroutineCall
        elif self.step == 2:
            # ) or subroutineName
            if " ) " in line:
                ret = line + "</term>\n"
                isClose = True
            else:
                ret = line
                self.step += 1            
        elif self.step == 3:
            # ( 
            if " ( " in line:
                ret = line
                self.step += 1            
                # 次はexpressionList
                nextKeyword = "expressionList"
            else:
                errMsg = (__class__.__name__, self.step, "( is missing")            
        elif self.step == 4:
            # ) 
            if " ) " in line:
                ret = line + "</term>\n"
                isClose = True
            else:
                errMsg = (__class__.__name__, self.step, ") is missing")  
                
        return errMsg, nextKeyword, isClose, isRemain, ret
    


# ## subroutineCall  
# subroutineName **(** expressionList **)** | (className | varName) **.** subroutineName **(** expressionList **)**  
# * className or varName **.** が付く場合がある  
# * **)** が来たら閉じる
# 

# In[68]:


class keywordSubroutineCall:
    step = 0
    def __init__(self):
        self.step = 0
    def check(self, line):
        errMsg = ""
        nextKeyword = ""
        isClose = False
        isRemain = False
        ret = ""
    
        if self.step == 0:
            ret = line
            self.step += 1
        elif self.step == 1:
            # ( or .
            if " ( " in line:
                ret = line
                self.step += 1            
                # 次はexpressionList
                nextKeyword = "expressionList"
            else:
                ret = line
                self.step += 1            
        elif self.step == 2:
            # ) or subroutineName
            if " ) " in line:
#                ret = line + "</term>\n"
                ret = line
                isClose = True
            else:
                ret = line
                self.step += 1            
        elif self.step == 3:
            # ( 
            if " ( " in line:
                ret = line
                self.step += 1            
                # 次はexpressionList
                nextKeyword = "expressionList"
            else:
                errMsg = (__class__.__name__, self.step, "( is missing")    
        elif self.step == 4:
            # ) 
            if " ) " in line:
#                ret = line + "</term>\n"
                ret = line
                isClose = True
            else:
                errMsg = (__class__.__name__, self.step, ") is missing")       
                
        return errMsg, nextKeyword, isClose, isRemain, ret


# ## expressionListキーワード  
# (expression (**,** expression)*)?  
# * subroutineCallのときだけ使う

# In[16]:


class keywordExpressionList:
    step = 0
    def __init__(self):
        self.step = 0
    def check(self, line):
        errMsg = ""
        nextKeyword = ""
        isClose = False
        isRemain = False
        ret = ""

        if self.step == 0:
            ret = "<expressionList>\n"
            self.step += 1
            # 次はexpression
            nextKeyword = "expression"
            isRemain = True
        elif self.step == 1:
            if " , " in line:
                # 次はexpression
                ret = line
                nextKeyword = "expression"
            else:
                # 終了
                ret = "</expressionList>\n"
                isClose = True
                isRemain = True
                
        return errMsg, nextKeyword, isClose, isRemain, ret


# ## スタック管理

# In[45]:


class stack:
    xmlKeyword = "<keyword>"
    xmlSymbol = "<symbol>"
    
    keywordStackList = list()
    nextKeyword = ""
    isSubroutineDec = False
    isStatements = False
    
    def __init__(self):
        self.keywordStackList = list()
        self.nextKeyword = ""
        self.isSubroutineDec = False
    def searchKeyword(self, line):
        '''読み込んだ文にキーワードが含まれているかチェックする'''
        isElse = False
        self.isStatements = False
        
        # 前回の処理からキーワードに指定がある場合はそちらに従う
        # expression, subroutineCall, expressionList, term
        if self.nextKeyword == "expression":
            self.keywordStackList.append(keywordExpression())
            return True, isElse
        if self.nextKeyword == "subroutineCall":
            self.keywordStackList.append(keywordSubroutineCall())
            return True, isElse
        if self.nextKeyword == "expressionList":
            self.keywordStackList.append(keywordExpressionList())
            return True, isElse
        
        
        # キーワードが含まれている場合、スタックにPush
        if self.xmlKeyword in line:
            if " class " in line:
                self.keywordStackList.append(keywordClass())
            elif " static " in line or " field " in line:
                self.keywordStackList.append(keywordClassVarDec())
            elif " constructor " in line or " function " in line or " method " in line:
                self.keywordStackList.append(keywordSubroutineDec())
                self.isSubroutineDec = True
            elif " var " in line:
                self.keywordStackList.append(keywordVarDec())
            elif " let " in line:
                self.keywordStackList.append(keywordLetStatement())
                self.isStatements = True
            elif " do " in line:
                self.keywordStackList.append(keywordDoStatement())
                self.isStatements = True
            elif " if " in line:
                self.keywordStackList.append(keywordIfStatement())
                self.isStatements = True
            elif " else " in line:
                self.keywordStackList.append(keywordElseStatement())
                # if のスタックで </ifStatement>で締めてしまっているので削除する
                isElse = True
            elif " while " in line:
                self.keywordStackList.append(keywordWhileStatement())
                self.isStatements = True
            elif " return " in line:
                self.keywordStackList.append(keywordReturnStatement())
                self.isStatements = True
                
            return True, isElse
        else:
            return False, isElse
    
    def processStack(self, line):
        '''スタック処理'''
        # 最後にPushしたキーワードクラスを処理する
        # キーワードクラスが終了した場合、スタックから削除する
        errMsg = ""
        if len(self.keywordStackList) <= 0:
            return False, "", ""
        
        # expressionなどはすぐに識別できないのでループ処理にする
        isRemain = True
        ret = ""
        while isRemain:
            errMsg, self.nextKeyword, isClose, isRemain, retLine = self.keywordStackList[-1].check(line)
            ret += retLine
            if len(errMsg) > 0:
                break                
            if isClose:
                self.keywordStackList = self.keywordStackList[:-1]
            if self.nextKeyword == "expression":
                self.keywordStackList.append(keywordExpression())
                self.nextKeyword = ""
            if self.nextKeyword == "expressionInTerm":
                self.keywordStackList.append(keywordExpressionInTerm())
                self.nextKeyword = ""
            if self.nextKeyword == "term":
                self.keywordStackList.append(keywordTerm())
                self.nextKeyword = ""
            if self.nextKeyword == "expressionList":
                self.keywordStackList.append(keywordExpressionList())              
                self.nextKeyword = ""
                
        # subroutineDecの{ のあと、statementキーワードが来たら <statements>を追加する
        if self.isSubroutineDec and self.isStatements:
            self.isSubroutineDec = False
            ret = "<statements>\n" + ret
        
        return isClose, ret, errMsg


# ## ファイル生成

# In[73]:


import os
import sys
 
def createFile(folderPath, fn):
    st = stack()
    wrLines = list()
    with open(os.path.join(folderPath, fn), 'r') as fin:
        lines = fin.readlines()
        for l in lines:
            isKeyword, isElse = st.searchKeyword(l)
            # else が来たらひとつ前の</ifStatement>を削除する
            if isElse:
                wrLines[-1] = wrLines[-1].replace("</ifStatement>\n", "")
            isClose, ret, errMsg = st.processStack(l)
            wrLines.append(ret)
            if len(errMsg) > 0:
                print(folderPath, fn, l, errMsg, "\n")
                break

    outputFn = fn.replace("T.xml", ".xml")
    outputFn = os.path.join(folderPath, outputFn)             
    with open(outputFn, 'w') as fout:
        for w in wrLines:
            fout.write(w)

def checkFolder(folderPath):
    '''指定したフォルダ内のファイルをチェックしてxmlファイルを出力する'''
    # フォルダ内にT.xmlファイルがあるかチェックする
    files = os.listdir(folderPath)
    files_file = [f for f in files if os.path.isfile(os.path.join(folderPath, f))]
    tokenFiles = [f for f in files_file if "T.xml" in f]

    if len(tokenFiles) <= 0:
        return False

    for fn in tokenFiles:
        createFile(folderPath, fn)
    return True

if __name__ == "__main__":
    checkFolder("./ArrayTest")
    checkFolder("./ExpressionLessSquare")
    checkFolder("./Square")


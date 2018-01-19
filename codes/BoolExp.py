# coding: utf-8
__author__ = 'multiangle'

class LogicExpression():
    def __init__(self,expression):
        """
        :param expression:
        :return:
        规定几种运算符号:   或运算     +
                            与运算     *或者没有
                            非运算     []
                            异或运算   #
        ATTENTION:不区分大小写，统一按大写看待
        """
        self.variables=[]           #参数列表（输入值）
        self.truth_table=None      #真值表
        self.truth_table_short=None
        self.karnaugh_map=None     #卡诺图

        if expression=='':
            raise ValueError('void string!')
        expression=expression.replace(' ','')
        expression=list(expression)
        for i in range(0,expression.__len__()):
            char=expression[i]
            if ord(char)>=97 and ord(char)<=122:
                char=char.upper()
                expression[i]=char
                if char not in self.variables:
                    self.variables.append(char)
            elif ord(char)>=65 and ord(char)<=90:
                if char not in self.variables:
                    self.variables.append(char)
        self.variables.sort()
        self.expression=''.join(expression)

        self.Generate_Truth_Table()
        self.Generate_Karnaugh_Map()

    def Generate_Truth_Table(self):
        truth_table=[]
        truth_table.append(self.variables+['Y'])
        for i in range(0,2**self.variables.__len__()):
            local_expression=self.expression
            variable_value=list(bin(i))[2:]
            variable_value=['0']*(self.variables.__len__()-variable_value.__len__())+variable_value
            for x in range(0,self.variables.__len__()):
                local_expression=local_expression.replace(self.variables[x],variable_value[x])
            local_res=self.cal_expression(local_expression)
            truth_table.append(variable_value+[local_res])
        self.truth_table=truth_table
        self.truth_table_short=[[''.join(x[0:x.__len__()-1]),x[x.__len__()-1]] for x in self.truth_table]
        # self.Print_Truth_Table()       local_expression=local_expression.replace(self.variables[x],variable_value[x])

    def Print_Truth_Table(self):
        lines=self.truth_table.__len__()
        cols=self.truth_table[0].__len__()
        print(('|---')*cols+'|')
        for line in self.truth_table:
            output='|'
            for col in line:
                output+=str(col)+'\t'+'|'
            print(output)
            # print(('|---')*cols+'|')
        print(('|---')*cols+'|')

    def Generate_Karnaugh_Map(self):
        tag_list=[x[0] for x in self.truth_table_short]
        tag_value=[x[1] for x in self.truth_table_short]
        if self.variables.__len__()==1:
            label_1=['0','1']
            label_2=['']
        if self.variables.__len__()==2:
            label_1=['0','1']
            label_2=['0','1']
        if self.variables.__len__()==3:
            label_1=['0','1']
            label_2=['00','01','11','10']
        if self.variables.__len__()==4:
            label_1=['00','01','11','10']
            label_2=['00','01','11','10']
        map=[[0 for col in range(label_2.__len__())] for row in range(label_1.__len__())]
        for x in range(0,label_1.__len__()):
            for y in range(0,label_2.__len__()):
                tag=''.join([label_1[x],label_2[y]])
                map[x][y]=tag_value[tag_list.index(tag)]
        self.karnaugh_map={
            'value':map,
            'l1':label_1,
            'l2':label_2
        }

    def cal_expression(self,expression):
        init_stack=[]       #括号运算
        for x in expression:
            if x!=')':
                init_stack.append(x)
            else:
                sub_expression=[]
                while(True):
                    item=init_stack.pop()
                    if item=='(':
                        break
                    else:
                        sub_expression.insert(0,item)
                sub_value=self.cal_expression(''.join(sub_expression))
                init_stack.append(sub_value)

        expression=''.join(init_stack)
        init_stack=[]        #非运算
        for x in expression:
            if x!=']':
                init_stack.append(x)
            else:
                sub_expression=[]
                while(True):
                    item=init_stack.pop()
                    if item=='[':
                        break
                    else:
                        sub_expression.insert(0,item)
                sub_value=self.cal_expression(''.join(sub_expression))
                if sub_value==0 or sub_value=='0':
                    sub_value='1'
                elif sub_value==1 or sub_value=='1':
                    sub_value='0'
                init_stack.append(sub_value)
        expression=''.join(init_stack)

        # print(expression)
        num_stack=[]
        sig_stack=[]
        num_stack.append(expression[0])
        for i in range(1,expression.__len__()):
            if expression[i] in ['0','1']:
                if expression[i-1] in ['0','1']:
                    num_stack.append(expression[i])
                    sig_stack.append('*')
                else:
                    num_stack.append(expression[i])
            else:
                if expression[i]=='+' or expression=='#':
                    if sig_stack.__len__()==0:
                        sig_stack.append(expression[i])
                    else:
                        if sig_stack[sig_stack.__len__()-1]=='+' or sig_stack[sig_stack.__len__()-1]=='#':
                            sig_stack.append(expression[i])
                        else:
                            while True:
                                a=num_stack.pop()
                                b=num_stack.pop()
                                sig=sig_stack.pop()
                                res=self.logic_cal(a,b,sig)
                                num_stack.append(res)
                                if sig_stack.__len__()==0:
                                    sig_stack.append(expression[i])
                                    break
                                if sig_stack[sig_stack.__len__()-1]=='+' or sig_stack[sig_stack.__len__()-1]=='#' :
                                    sig_stack.append(expression[i])
                                    break
                else:
                    sig_stack.append(expression[i])

        while True:
            if sig_stack.__len__()==0:
                break
            a=num_stack.pop()
            b=num_stack.pop()
            sig=sig_stack.pop()
            res=self.logic_cal(a,b,sig)
            num_stack.append(res)
        return num_stack[0]

    def Plot_Karnaugh_Map(self):
        row_num=self.karnaugh_map['l1'].__len__()+1
        col_num=self.karnaugh_map['l2'].__len__()+1
        # print('|'+'---|'*col_num)       #第一行的上限
        content='|'+'\t'+'|'
        for x in self.karnaugh_map['l2']:
            content+=x+'\t'+'|'
        print(content)
        # print('|'+'---|'*col_num)
        for i in range(0,self.karnaugh_map['l1'].__len__()):
            content='|'+self.karnaugh_map['l1'][i]+'\t'+'|'
            for j in range(0,self.karnaugh_map['l2'].__len__()):
                content+=self.karnaugh_map['value'][i][j]+'\t'+'|'
            print(content)
            # print('|'+'---|'*col_num)

    def Equal_To(self,b_expression):
        cmp_obj=LogicExpression(b_expression)
        if self.karnaugh_map['value']==cmp_obj.karnaugh_map['value']:
            return True
        else:
            return False

    def logic_cal(self,in_1,in_2,sig):
        #sig='+','*','#'
        if isinstance(in_1,str) or isinstance(in_2,str):
            in_1=int(in_1)
            in_2=int(in_2)

        if sig=='+':
            if in_1==1 or in_2==1:
                return '1'
            else:
                return '0'
        elif sig=='*':
            if in_1==1 and in_2==1:
                return '1'
            else:
                return '0'
        elif sig=='#':
            if in_1==in_2:
                return '0'
            else:
                return '1'

if __name__=='__main__':
    x='a#b'
    a=LogicExpression(x)
    # print('|'+'---'+'|'+'---')
    # print('|'+'AB'+'\t'+'|')
    # print('-'+'---'+'-')
    # for x in a.truth_table_short:
    #     print(x)
    # print(a.truth_table_short)
    # a.Plot_Karnaugh_Map()
    # b=LogicExpression('a')
    a.Plot_Karnaugh_Map()
    for x in a.truth_table_short:
        print(x)
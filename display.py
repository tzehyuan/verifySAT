def display_formula(F):
    ''' display the formula F'''
    return [display_clause(c) for c in F]

def display_clause(c):  
        ''' display the clause c'''
        return [display_literal(l) for l in c]

def display_literal(l):
            ''' display the literal l'''
            s = ""
            if l<0:
                s+="¬"
            if abs(l) ==1:
                s+="x" 
            elif abs(l) ==2:
                s+="y" 
            elif abs(l) ==3:
                s+="z" 
            elif abs(l)<100:
                s+="v"+ str(abs(l) -  10)
            else:
                s+="C"+str(abs(l)-100)
            return s
    

def pad_string(s, length=150):
    return s.ljust(length)

def convert_list_of_lists_to_string(list_of_lists):
    result_list = []
    for sublist in list_of_lists:
        sublist_str = ', '.join(map(str, sublist))
        result_list.append(f'[{sublist_str}]')
    result_string = ', '.join(result_list)
    return f'[{result_string}]'
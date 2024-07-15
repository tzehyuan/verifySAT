from CNF import  all_positive
from display import pad_string, convert_list_of_lists_to_string, display_formula
from copy import deepcopy as dc

def w(file, f, reason):
    '''write to the file f and reason if it is non-empty'''
    file.write(pad_string(convert_list_of_lists_to_string(f)))
    if reason!="":
        file.write(reason)
    file.write("\n")

def generate_initial_2(c1,c2,c3,c4):
    '''
    (¬x ∨ ¬y) and let there be clauses (x ∨ α), (x ∨ β), (y ∨ γ),(y ∨ δ) and label this clauses 1 to 4 respectively
    Whenever applicable, ensure that |α| >= |β|, |γ|>= |δ|, and |ω|>=|σ| and  |α| + |β|>= |γ| + |δ| >= |ω|+|σ|

    By aasumption (A1: all clause are length at most 3)
    let c1,c2,c3,c4 be the parameters that the length of clause 1 to 4 respectively (6 cases, 3333,3332,3322,3232,3222,2222)
    '''
    s = f"2-clause/{c1}{c2}{c3}{c4}_all.txt"
    size =[c1,c2,c3,c4]
    with open(s, 'a') as file:
        iterate_2([[-1,-2],[1],[1],[2],[2]], [11,12,13,14,15,16,17,18] , file, size)

def iterate_2(f, vars, file, size):
    '''iterate the variables recursively, maintaining the partial formula f, let vars be the unassigned variables and file be the file to write on and size correlate to c1-c4'''
    
    if len(vars)>0:
        vars = dc(vars)
        v = vars.pop(0)
        '''iterate possible ways to slot the literals in v into f'''
        '''constraint 1 : f should not exceed the size given by c1-c4 '''
        current = [len(c) for c in f]
        current.pop(0)
        slots_remaining = sum([size[i]-current[i] for i in range(4)]) #number of slots remaining
        if slots_remaining == 0:
            iterate_2(f, [], file, size)
            return #we can not slot any remaining variables in 
        min_av = 0
        while (min_av <4):
            if size[min_av]-current[min_av]>0:
               break
            min_av+=1 
        min_av+=1
        #min_av is the minimum index where a clause is free and 5 o/w
        ''''
        Symmetry-break: we slot in a literal of v into the earliest available clause

        rule 5: if v can not be both in clause 1 & 2 or 3 & 4
        rule 6.1: if ¬v shares a clause with x or y, v does not share a clause with x or y
        rule 6.3: if v is in a clause of length 2 with x or y, then the other instance of v does not share a clause with x or y

        Thus 3 case, (1) solely slot v into the earlieast available clause, (2) slot ¬v in the earliest available clause,
         (3) or if the earliest available clause is size 3, then if the clause is 1 or 2, put another instance into clause 3/4 subject to if they are not full and can be size 3
        
        To ensure the literal x,y share a clause with a negative literal (AS2), if f currently consist of solely positive literals (other than the all negative clause), 
        if there are 2 'slots' left then (3) is not applicable, if there are 1 'slot' left than (1)&(3) are not applicable
        '''
        f1 , f2 = dc(f), dc(f)
        f1[min_av].append(-1 * v)  #slot in ¬v in the earliest available clause
        f2[min_av].append(v)  #slot v in the earliest avaiable clause
        f3,f4 = dc(f2),dc(f2)
        f3[3].append(v) #slot an additional instance of v in c3
        f4[4].append(v) #slot an additional instance of v in c4

        iterate_2(f1, vars, file, size)
        if slots_remaining > 1 or not all_positive(f): #(AS2)
            iterate_2(f2, vars, file, size)
        if min_av <=2 and not all_positive(f) and size[min_av-1] ==3 and size[2] ==3 and current[2]<=2:
            iterate_2(f3, vars, file, size)
        if min_av <=2 and not all_positive(f) and size[min_av-1] ==3 and size[3] ==3 and current[3]<=2:
            iterate_2(f4, vars, file, size)
        
    else:
        w(file,display_formula(f),"")

generate_initial_2(3,2,3,2)
from CNF import all_positive, branching_constraints
from display import display_formula
from copy import deepcopy as dc
from generate_clause_2 import w

def generate_initial_3(c1,c3,c5):
    '''
    (¬x ∨ ¬y ∨ ¬z) and let there be clauses (x ∨ α), (x ∨ β), (y ∨ γ),(y ∨ δ), (z ∨ ω) and (z ∨ σ) and label this clauses 1 to 6 respectively

    Whenever applicable, ensure that |α| >= |β|, |γ|>= |δ|, and |ω|>=|σ| and  |α| + |β|>= |γ| + |δ| >= |ω|+|σ| 
    Whenever applicable, ensure that |α| >= |β|, |γ|>= |δ|, and |ω|>=|σ| and  |α| + |β|>= |γ| + |δ| >= |ω|+|σ|

    By assumption (A1: |N(x)| =3 and |N(y)|, |N(z)|<=3), thus c2,c4,c6 are length 2  
    let c1,c3,c5 be the parameters that the length of clause 1,3,5 respectively (3 cases, 333, 332, 322)
    '''
    s = f"3-clause/{c1}{c3}{c5}_all.txt"
    filtered = f"3-clause/{c1}{c3}{c5}_filtered.txt"
    size =[c1,2,c3,2,c5,2]
    with open(s, 'a') as file1, open(filtered, 'a') as file2 :
        iterate_3([[-1,-2,-3],[1],[1],[2],[2],[3],[3]], [11,12,13,14,15,16,17,18,19] , file1, file2, size)

def iterate_3(f, vars, file1, file2, size):
    '''iterate the variables recursively, maintaining the partial formula f, let vars be the unassigned variables and file be the file to write on and size correlate to c1-c4'''
    
    if len(vars)>0:
        vars = dc(vars)
        v = vars.pop(0)
        '''iterate possible ways to slot the literals in v into f'''
        '''constraint 1 : f should not exceed the size given by c1-c4 '''
        current = [len(c) for c in f]
        current.pop(0)
        slots_remaining = sum([size[i]-current[i] for i in range(6)]) #number of slots remaining
        if slots_remaining == 0:
            iterate_3(f, [], file1, file2, size)
            return #we can not slot any remaining variables in 
        min_av = 0
        while (min_av <6):
            if size[min_av]-current[min_av]>0:
               break
            min_av+=1 
        min_av+=1
        #min_av is the minimum index where a clause is free and 6 o/w
        ''''
        Symmetry-break: we slot in a literal of v into the earliest available clause

        rule 5: if v can not be both in clause 1 & 2 or 3 & 4
        rule 6.1: if ¬v shares a clause with x (or y z), v does not share a clause with any of  x, y, z
        rule 6.2: if v is in a clause of length 2 with x or y or z, then if the other instance of v is in a clause of size x or y or z then the clause is size 3

        Thus 3 case, (1) solely slot v into the earlieast available clause, (2) slot ¬v in the earliest available clause,
         (3) or if the earliest available clause is size , then if the clause is 1 or 2, put another instance into clause 3/4 subject to if they are not full and can be size 3
        '''
        f1 , f2 = dc(f), dc(f)
        f1[min_av].append(-1 * v)  #slot in ¬v in the earliest available clause
        f2[min_av].append(v)  #slot v in the earliest avaiable clause
        f3,f4,f5,f6 = dc(f2),dc(f2), dc(f2),dc(f2)
        f3[3].append(v) #slot an additional instance of v in c3
        f4[4].append(v) #slot an additional instance of v in c4
        f5[5].append(v) #slot an additional instance of v in c5
        f6[6].append(v) #slot an additional instance of v in c6      



        iterate_3(f1, vars, file1, file2, size)
        iterate_3(f2, vars, file1, file2, size)
        if min_av <=2 and current[2]<size[2] and (size[min_av-1] == 3 or size[2] ==3 ):
            iterate_3(f3, vars, file1, file2, size)
        if min_av <=2 and current[3]<size[3] and (size[min_av-1] == 3 or size[3] ==3):
            iterate_3(f4, vars, file1, file2, size)
        if min_av <=4 and current[4]<size[4] and (size[min_av-1] == 3 or size[4] ==3 ):
            iterate_3(f5, vars, file1, file2, size)
        if min_av <=4 and current[5]<size[5] and (size[min_av-1] == 3 or size[5] ==3 ):
            iterate_3(f6, vars, file1, file2, size)
        
    else:
        isAdmissable = branching_constraints().admissiable_branching(f)
        w(file1,display_formula(f),isAdmissable)
        if isAdmissable == "":
            w(file2,display_formula(f),isAdmissable)

generate_initial_3(3,3,3)
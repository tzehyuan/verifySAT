from display import display_formula, display_clause, display_literal
from copy import deepcopy as dc

'''
Representation of CNF formula:

A CNF formula is represent by a list of list of integers (each list is a clause, positive/negative int represent postive/negative literal)
clause are numbered by their position in F
Clause 0 (F[0]) always contain the all-negative clause

number 1-3 represents our variables in an all negative clause
number 11-19 represents variables that share a clause with a variable from 1-3
number 101-120 represents possibly empty subclauses that share a clause with variables from 11-19
'''

def vars(c):
    '''returns the variables in a clause c'''
    s = set()
    for l in c:
        s.add(abs(l))
    return s
        
def vars_clauses(C):
    '''returns the variables in a set of clauses C'''
    s = set()
    for c in C:
        s = s.union(vars(c))
    return s
    


def occurences(f, v):
    '''
    given a formula f, decide how many occurences of v is present
    -return (a,b) the number of positive and negative literals of v present in f
    '''
    p , n = 0,0
    for c in f:
        if v in c:
            p+=1
        if -1 * v in c:
            n+=1
    return (p,n)
            
def add_resolvents(f, v):
    pos_clauses = [clause for clause in f if v in clause]
    neg_clauses = [clause for clause in f if -1 * v in clause]
    resolvents = []

    for pos_clause in pos_clauses:
        for neg_clause in neg_clauses:
            resolvent = resolve_clauses(pos_clause, neg_clause, v)
            if resolvent not in resolvents:
                resolvents.append(resolvent)

    # Remove all clauses containing v or -v
    new_f = [clause for clause in f if v not in clause and -v not in clause]

    # Add the resolvents
    new_f.extend(resolvents)

    return new_f

def resolve_clauses(pos_clause, neg_clause, v):
    # Create a new clause without the variable v or -v
    new_clause = [literal for literal in pos_clause if literal != v]
    new_clause += [literal for literal in neg_clause if literal != -v]
    # Remove duplicates
    new_clause = list(set(new_clause))
    return new_clause
    
class branching_constraints:
    '''
    very basic branching rule 
    - when we set l to true, remove clauses than contain l and remove ¬l from all clauses
    - if we remove a negative literal ¬v, assign v to 1
    - if there is a singleton clause [v], we can set v to 1
    '''
    def assign(f,l):
            '''set l to True in f'''
            variables = [i for i in range(11,20)]+[1,2,3]
            f = dc(f)
            variables_removed = set()
            literals = [l] #set of literals to assign   6a34n
            while len(literals)>0:
                l = literals.pop()
                variables_removed.add(abs(l))
                f_temp = []
                for c in f:
                    if l in c: #remove c
                        for v in variables:
                            if -1 * v in c and abs(v)!=abs(l): #if we remove a clause containing the literal ¬v, we can set v to 1
                                literals.append(v)
                        for v in c: #add variables removed in the clause
                            variables_removed.add(abs(v))
                    elif -1*l in c:
                        if len(c)==1: return [[]] #F is unsatisfiable
                        c1 = [v for v in c if v != -1*l]
                        f_temp.append(c1) #add c removing ¬l
                    else:
                        f_temp.append(c) #else c goes back to f
                for c in f_temp: #if we have a singleton clause [v], we can set v to 1
                    if len(c) == 1: 
                        literals.append(c[0])
                f = f_temp
            return (f,variables_removed)
    
    def admissiable_branching(self,f):
        ''' see if there is a branching in f with branching factor better than τ(3,11) or τ(4,9)'''

        for v in f[0]:
            f1 , r1 = branching_constraints.assign(f, -v)
            f2, r2 = branching_constraints.assign(f,v)
            r1,r2 = sorted(r1),sorted(r2)
            s, b = min(len(r1),len(r2)),max(len(r1),len(r2))
            if (s >= 4 and s+b >=13) or (s==3 and s+b>=14):
                return f"Branching on {display_literal(-1 * v)} has branching factor of τ({s},{b}) eliminating {display_clause(r1)} when set to 1 and {display_clause(r2)} when set to 0"
        return ""
    
    
class full_branching:
    '''
    Pre-requisite, in f, all variables (from 1 to 19) contain 3 occurences
    '''
    def standardisation(f):
        '''apply some basic reduction rules
        - step 3-4 of the algorithm
        '''
        def no_opposite_pairs(lst):
            seen = set()
            for num in lst:
                if -num in seen:
                    return False  
                seen.add(num)
            return True
        f = dc(f)
        f = [c for c in f if no_opposite_pairs(c)] #remove  a clause (x ∨ ¬x ∨ α) 
        f = [list(set(c)) for c in f] #remove duplicates literals / subclause in f (x ∨ x ∨ α) 
        
        for c in f:
            if len(c)==1 and c[0] < 20: #only assign the literal in a singleton clause to be true if it does not contain a subclause
                f, _ = branching_constraints.assign(f,c[0])
                return full_branching.standardisation(f)
        f_set = [set(c) for c in f]
        for i in range(len(f)): #remove a clause c1 if c2 is a subset of c1
            for j in range(len(f)):
                if f_set[i].issubset(f_set[j]) and i != j:
                    f.pop(j)
                    return full_branching.standardisation(f)

        variables = vars_clauses(f)
        print(f,variables)
        for v in variables:
            if v < 20: #do not resolve subclauses
                p , n = occurences(f,v)
                if p +n < 3:
                    f = add_resolvents(f, v)
                    return full_branching.standardisation(f)

        return f
    
    
    





    
        

def all_positive(f):
            '''check if f contains solely positve literals other than clause 0'''
            for idx , c in enumerate(f):
                if idx>0:
                    for l in c:
                        if l<0:
                            return False
            return True

f = [[-1, -2, -3], [1, -11,  12], [1,12], [1, 13], [2, 13, 14], [2, 15], [3, 15, -16], [3, 12]]

print(full_branching.standardisation(f))
import random
import itertools
def remove_duplicates(L):
    #this is needed in the game class, to avoid duplicate options
    if L==[]:
        return L
    new_list = [L[0]]
    for i in range(1,len(L)):
        if new_list[-1] != L[i]:
            new_list.append(L[i])
    return new_list
sum_lookup = dict()

class Game:
    def __init__(self, L, R):
        self.Lopt = sorted(L)
        self.Ropt = sorted(R)
        self.Lopt = remove_duplicates(self.Lopt)
        self.Ropt = remove_duplicates(self.Ropt)
# 
    # def __str__(self):
    #     return str([self.Lopt, self.Ropt])

    def __repr__(self):
        if self == zero:
            return "0"
        if self == star:
            return "*"
        if self == up:
            return "↑"
        if self == down:
            return "↓"
        if self == up_star:
            return "↑*"
        if self == down_star:
            return "↓*"
        if self == double_up:
            return "⇑"
        if self == double_down:
            return "⇓"
        n = self.rank()
        if self == num(n):
            return str(n)
        if self == num(-n):
            return "-" + str(n)
        if self == Star(n):
            return "*" + str(n)
        if self == waiting(n):
            return "W" + str(n)
        if self == neg(waiting(n)):
            return "-W" + str(n)
        # if self == tiny(n - 2):
        #     return "⧾" + str(n - 2)
        # if self == neg(tiny(n - 2)):
        #     return "⧿" + str(n - 2)
        if self == z:
            return "z"
        if self == neg(z):
            return "-z"
        return repr([self.Lopt, self.Ropt])

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return self.Lopt == other.Lopt and self.Ropt == other.Ropt

    def __lt__(self, other):
        return repr(self) < repr(other)

    def Options(self, Player):
        if Player == 0:
            return self.Lopt
        if Player == 1:
            return self.Ropt
       
    def __add__(self, other):
        if (self, other) in sum_lookup:
            return sum_lookup[(self,other)]
        leftoptions = []
        rightoptions = []
        for Gl in self.Lopt:
            leftoptions.append(Gl + other)
        for Hl in other.Lopt:
            leftoptions.append(self + Hl)
        for Gr in self.Ropt:
            rightoptions.append(Gr + other)
        for Hr in other.Ropt:
            rightoptions.append(self + Hr)
        sum_lookup[(self,other)] = Game(leftoptions, rightoptions)
        return Game(leftoptions, rightoptions)

    def __sub__(self, other):
        return self + neg(other)

    def __neg__(self):
        return neg(self)

    def is_dicot(self):
        # Checks if self is a dicot (the game tree has no options or at least one for each Player)
        # Returns a Boolean
        if self == zero:
            return True
        if (self.Lopt == []) != (self.Ropt == []):
            return False
        for Player in range(2):
            for H in self.Options(Player):
                if not H.is_dicot():
                    return False
        return True

    def oL(self):
        #Returns the misere result when Left plays first
        GL=self.Lopt
        if GL==[]:
            return 'L'
        for Gl in GL:
            if Gl.oR()=='L':
                return 'L'
        return 'R'

    def oR(self):
        #Returns the misere result when Right plays first
        GR=self.Ropt
        if GR ==[]:
            return "R"
        for Gr in GR:
            if Gr.oL()=='R':
                return "R"
        return "L"

    def o(self):
        #Returns the misere outcome
        LeftFirst=self.oL()
        RightFirst=self.oR()
        if LeftFirst=='L' and RightFirst=='R':
            return 'N'
        if LeftFirst=='L' and RightFirst=='L':
            return 'L'
        if LeftFirst=='R' and RightFirst=='R':
            return 'R'
        if LeftFirst=='R' and RightFirst=='L':
            return 'P'
    
    def rank(self):
        if self==zero:
            return 0
        left_ranks = [Gl.rank() for Gl in self.Lopt]
        right_ranks = [Gr.rank() for Gr in self.Ropt]
        return 1 + max(left_ranks + right_ranks)

zero = Game([], [])

def num(n):
    if n== 0:
        return Game([],[])
    elif n>0:
        return Game([num(n-1)],[])
    else:
        return Game([],[num(n+1)])

def Star(n):
    if n == 0:
        return Game([], [])
    else:
        opts = [Star(i) for i in range(n)]
        return Game(opts, opts)

def waiting(n):
    """Returns the Right waiting game of rank n (useful in deadending)"""
    if n==0:
        return zero
    if n==1:
        return negone
    else:
        return Game([],[zero,waiting(n-1)])

def passing(n):
    """Returns the Right passing game of rank n"""
    if n==0:
        return zero
    if n==1:
        return negone        
    if n==2:
        return Game([],[one,zero])
    else:
        return Game([],[one,passing(n-1)])

def neg(G):
    HL = []
    HR = []
    if G == zero:
        return zero
    for Gl in G.Lopt:
        HR.append(neg(Gl))
    for Gr in G.Ropt:
        HL.append(neg(Gr))
    return Game(HL, HR)

one = Game([zero],[])
negone = neg(one)
star = Star(1)
up = Game([zero], [star])
down = Game([star], [zero])
up_star = Game([zero, star], [zero])
down_star = Game([zero],[zero, star])
z = Game([star,zero],[star])
mup = z
double_up = Game([zero], [up_star])
double_down = Game([down_star], [zero])


# def power_set(L):
#     if L == []:
#         return [L]
#     else:
#         e = L[0]
#         t = L[1:]
#         pt = power_set(t)
#         fept = [x + [e] for x in pt]
#     return pt + fept


def soL(G):
    """Returns the strong Left outcome of G (deadend)"""
    n = G.rank()
    if n==0:
        return 'L'
    X = G + waiting(n-1)
    if X.oL()=='R' or G.oL()=='R':
        return 'R'
    return 'L'

def soR(G):
    """Returns the strong Right outcome of G (deadeng)"""
    n = G.rank()
    if n==0:
        return 'R'
    X = G+neg(waiting(n-1))
    if X.oR()=='L' or G.oR()=='L':
        return 'L'
    return 'R'

# def so(G):
#     """Returns the strong outcome of G"""
#     LeftStrong=soL(G)
#     RightStrong=soR(G)
#     if LeftStrong=='L' and RightStrong=='R':
#         return 'N'
#     if LeftStrong=='L' and RightStrong=='L':
#         return 'L'
#     if LeftStrong=='R' and RightStrong=='R':
#         return 'R'
#     if LeftStrong=='R' and RightStrong=='L':
#         return 'P'

def LeftStrong(G,U):
    if U=="M":
        if G.Lopt==[]:
            return True
    if U=="D":
        return G.oL()=="L"
    if U=="E":
        return soL(G)
    if U=="B":
        if G.Lopt==[]:
            return True
        for GL in G.Lopt:
            if GL.o()=="L" and LeftStrong(GL,"B"):
                flag=True
                for GLR in GL.Ropt:
                    if not LeftStrong(GLR,"B"):
                        flag=False
                if flag:
                    return True
        return False

def RightStrong(G,U):
    if U=="M":
        if G.Ropt==[]:
            return True
    if U=="D":
        return G.oR()=="R"
    if U=="E":
        return soR(G)
    if U=="B":
        if G.Ropt==[]:
            return True
        for GR in G.Ropt:
            if GR.o()=="R" and RightStrong(GR,"B"):
                flag=True
                for GRL in GR.Lopt:
                    if not RightStrong(GRL,"B"):
                        flag=False
                if flag:
                    return True
        return False


def proviso(G,H,U):
    """Checks the Proviso for G>=H mod B"""
    return (H.Lopt!=[] or LeftStrong(G,U)) and (G.Ropt!=[] or RightStrong(H,U))
    # if H.Lopt==[]: 
    #     return LeftStrong(G,U)
    # if G.Ropt==[]:
    #     return RightStrong(H,U)
    # return True

def maintenance1(G,H,U):
    #Returns True if part 1 of maintenance is true
    for Hl in H.Lopt:
        exists = False
        for Gl in G.Lopt:
            if greater(Gl,Hl,U):
                exists=True
                break
        if not exists:
            for Hlr in Hl.Ropt:
                if greater(G,Hlr,U):
                    exists=True
                    break
        if not exists:
            return False
    return True

def maintenance2(G,H,U):
    #Returns True if part 2 of maintenance is true
    for Gr in G.Ropt:
        exists = False
        for Hr in H.Ropt:
            if greater(Gr,Hr,U):
                exists = True
                break
        if not exists:
            for Grl in Gr.Lopt:
                if greater(Grl,H,U):
                    exists = True
                    break
        if not exists:
            return False
    return True

def greater(G,H,U):
    if G==H:
        return True
    #Given games G=[GL,GR] and H=[HL,HR], returns true if proviso and maintenance are true
    if proviso(G,H,U) and maintenance1(G,H,U) and maintenance2(G,H,U):
        return True
    else:
        return False

def equal(G,H,U):
    if G==H:
        return True
    return greater(G,H,U) and greater(H,G,U)

def is_invertible(G,U):
    H = G+neg(G)
    return greater(H,zero,U)

def is_Pfree(G):
    """Returns True if no followers of G, including G, have outcome P"""
    if G.o()=="P":
        return False
    for GL in G.Lopt:
        if not is_Pfree(GL):
            return False
    for GR in G.Ropt:
        if not is_Pfree(GR):
            return False
    return True

def remove_left_dominated(G,U):
    #returns G with dominated Left options removed
    GL = G.Lopt
    reduced_GL = GL.copy()
    dominated_option_indices = []
    l = len(GL)
    for h in range(l):
        if not h in dominated_option_indices:
            H = GL[h]
            for k in range(l):
                if k != h and not k in dominated_option_indices:
                    K = GL[k]
                    if greater(H,K,U):
                        reduced_GL.remove(K)
                        dominated_option_indices.append(k)
    return Game(reduced_GL,G.Ropt)

def remove_right_dominated(G,U):
    #returns G with dominated Right options removed
    GR = G.Ropt
    reduced_GR = GR.copy()
    dominated_option_indices = []
    l = len(GR)
    for h in range(l):
        if not h in dominated_option_indices:
            H = GR[h]
            for k in range(l):
                if k != h and not k in dominated_option_indices:
                    K = GR[k]
                    if greater(K,H,U):
                        reduced_GR.remove(K)
                        dominated_option_indices.append(k)
    return Game(G.Lopt,reduced_GR)

################


"""
Next we create the non-end dead-ending day2 games
by using all possible non-empty subsets of day 1 games as option sets.
We use the powerset function from itertools.
"""
day1 = [zero, one, negone, star]


#day2ends = [num(2), num(-2), waiting(2), neg(waiting(2))]

subsets=[]
def powerset(S,n):
    """Given a list S and length n,
    returns a list of all non-empty subsets of S up to size n""" 
    if n > 0:
        for x in itertools.combinations( S, n ):
            subsets.append(list(x))
        powerset( S, n-1 )
    return(subsets)

option_sets= list(powerset(day1,4))

# day2nonends= []
# for GL in option_sets:
#     for GR in option_sets:
#         G = Game(GL, GR)
#         day2nonends.append(G)

# day2 = day2ends + day2nonends


#todo -- make a function that removes reversible options recursively

#generate all day 2 blocked left ends
leftendsB2 =[]
for XR in option_sets:
    X = Game([],XR)
    leftendsB2.append(X)

#all blocking games up to rank 2
day2B = [zero]
for GL in option_sets:
    for GR in option_sets:
        G = Game(GL,GR)
        day2B.append(G)

# GRL = Game([num(-3)],[])
# GR = Game([GRL],[])
# G = Game([num(-3)],[negone, GR])
# H = Game([num(-3)],[num(-1)])
# C = negone

# print(equal(G+C,H+C,"M"))
# print(equal(G,H,"M"))

half = Game([zero],[one])
G = Game([waiting(2)],[zero,one])
print(greater(zero,G,"B"))
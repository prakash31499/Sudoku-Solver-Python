import copy
ret = 0

sudoku = [[0 for x in range(9)]for y in range(9)]

test1 = [
    [ 8,0,0,0,0,0,0,0,0],
    [ 0,0,3,6,0,0,0,0,0],
    [ 0,7,0,0,9,0,2,0,0],
    [ 0,5,0,0,0,7,0,0,0],
    [ 0,0,0,0,4,5,7,0,0],
    [ 0,0,0,1,0,0,0,3,0],
    [ 0,0,1,0,0,0,0,6,8],
    [ 0,0,8,5,0,0,0,1,0],
    [ 0,9,0,0,0,0,4,0,0]
    ]

test2 = [
     [ 0,7,0,0,0,0,0,5,0],
     [ 0,9,3,0,0,0,1,6,0],
     [ 1,0,5,0,7,0,4,0,3],
     [ 9,0,0,2,1,6,0,0,4],
     [ 4,0,0,3,0,9,0,0,1],
     [ 0,1,0,8,0,7,0,2,0],
     [ 0,0,8,0,0,0,5,0,0],
     [ 0,6,1,0,9,0,7,8,0],
     [ 0,4,0,0,8,0,0,1,0]
      ]

square = [[]for x in range(81)]

bodef = ((0,0,0),(0,1,1),(0,2,2),(1,0,3),(1,1,4),(1,2,5),(2,0,6),(2,1,7),(2,2,8))

boxxx = (0,1,2,9,10,11,18,19,20)

rem_in = [ [ [] for x in range(9) ] for y in range(3) ]

def printbox(box):
    print("\n")
    for x in range(9):
        for y in range(9):
            print("  ",box[x][y]," ",end = " ")
        print("\n")

def inpu():
    global sudoku
    global test
    ans = input("Do you want to input (y/n) ")
    if ans != 'y':
        ch = int(input("Choose any one 1. or 2."))
        if ch == 1:
            print(" The question is.. ")
            printbox(test1)
            return test1
        else:    
            print(" The question is.. ")
            printbox(test2)
            return test2
    n = int(input(" How Many Numbers? "))
    for x in range(n):
        pos = int(input("Enter the position "))
        sudoku [ int(pos/9) ][ pos%9 ] = int(input(" Enter the number "))
    print(" The question is.. ")
    printbox(sudoku)
    return sudoku

def solved(box):
    global ret
    res = solve(box)
    if not res:
        result(box)
    else:
        assume(box)
            
def solve(bx):
    global square
    global rem_in
    assign_rem(bx)
    fill_sq(bx)
    while 1:
        for x in range(81):
            fake = copy.deepcopy(square)
            if bx[ int(x/9) ][ x%9 ] == 0:
                if basic_check(bx,x) :
                    break
        if fake == square:
            if not basic_check2(bx):
                break
    for x in range(9):
        if 0 in bx[x]:
            return 1
            break
    for x in range(81):
        if len( square[x] ) == 0 and bx[ int(x/9) ][ x%9 ] == 0 :
            return 2        
    return 0

def assume(box):
    global square
    global ret
    assq = [[],[]]
    ret = 1
    assign_rem(box)
    fill_sq(box)
    assq[0] = copy.deepcopy(box)
    assq[1] = copy.deepcopy(box)
    for x in range(81):
        if len( square[x] ) == 2 and box [ int(x/9) ][x%9] == 0 :
            val1 = square[x][0]
            val2 = square[x][1]
            put( assq[0] , int(x/9) , x%9 , val1 )
            put( assq[1] , int(x/9) , x%9 , val2)
            u = solve(assq[0])
            if not u:
                result(assq[0])
            elif u == 1:
                if not assume(assq[0]):
                    u = solve(assq[1])
                    if not u:
                        result(assq[1])
                    elif u == 1:
                        assume(assq[1])
                    elif u == 2:
                        return 0
                    
            elif u == 2:
                u = solve(assq[1])
                if not u:
                    result(assq[1])
                elif u == 1:
                    assume(assq[1])
                elif u == 2:
                    return 0
            
def intersec(s1,s2,s3):
    s_1 = set(s1)
    s_2 = set(s2)
    s_3 = set(s3)
    inter = s_1.intersection(s_2)
    final = inter.intersection(s_3)
    return list(final)

def which_box( row,col ) :
    global bodef
    for y in range(9):
            if bodef[y][0] == int(row/3) and bodef[y][1] == int(col/3):
                return bodef[y][2]

def fill_sq(b):
    global square
    global rem_in
    assign_rem(b)
    for x in range(81):
        if b[int(x/9)][ x%9 ] == 0:
            row = int(x/9)
            col = x%9
            boxx = which_box(row,col)
            lis = intersec(rem_in[0][row],rem_in[1][col],rem_in[2][boxx])
            square[x] = lis[:]
        else:
            square[x] = []

def basic_check( box,x ):
    global square
    if len( square[x] ) == 1 :
        val = square[x][0]
        put( box , int(x/9) , x%9 , val)
        return 1
    return 0
    
def basic_check2( box ):
    global boxxx
    global square
    for x in range(9):
        value = [ [ 0 for i in range(9) ] for j in range(3) ]
        for y in boxxx:
            for z in range(1,10):
                if z in square[y + 3*(x%3) + 27*int(x/3)]:
                    value[2][z-1] += 1
        for y in range(9):
                for z in range(1,10):
                    if z in square[9*x + y]:
                        value[0][ z-1 ] += 1
                    if z in square[9*y + x]:
                        value[1][ z-1 ] += 1

        if 1 in value[0]:
            val = value[0].index(1) + 1
            for y in range(9):
                if val in square[ 9*x + y ]:
                    put( box,x,y,val )
                    return 1
        if 1 in value[1]:
            val = value[1].index(1) + 1
            for y in range(9):
                if val in square[ 9*y + x ]:
                    put( box,y,x,val )
                    return 1
        if 1 in value[2]:
            val = value[2].index(1) + 1
            for y in boxxx:
                b = y + 3*(x%3) + 27*int(x/3)
                if val in square[ b ]:
                    r = int(b/9)
                    c = b%9
                    put( box,r,c,val )
                    return 1
    return 0 
def put( box , r , c , val ):
    global square
    global rem_in
    box[r][c] = val
    fill_sq(box)
    
def assign_rem(box):
    global rem_in
    rem_in = [ [ [] for x in range(9) ] for y in range(3) ]
    for x in range(9):
        for z in range(1,10):
            if z not in box[x]:
                rem_in[0][x].append(z)
            flag = 0 
            for y in range(9):
                if box[y][x] == z:
                    flag = 1
                    break
            if not flag:
                rem_in[1][x].append(z)
    for a in range(1,10):
        for z in range(9):
            flag = 0
            for x in range(3):
                for y in range(3):
                    if box[3* int(z/3) + x][3*(z%3) + y] == a:
                        flag = 1
                        x = 3
                        break
            if not flag:
                rem_in[2][z].append(a)

def result(bx):
    printbox(bx)
    input("Press Any key to exit")
    sys.exit    
#main
print("\t\t\t WELCOME TO SUDOKU SOLVER ")
bx = inpu()
solved(bx)

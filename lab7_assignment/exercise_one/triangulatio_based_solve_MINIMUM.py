## this solve relies on the MIN of guards needed. 
import matplotlib.pyplot as plt
import tripy
import time
Start = time.time()

polygon = [
    (4, -4),   # P1
    (-5, 6),   # P2
    (6, -4),   # P3
    (-7, 4),   # P4
    (9, 6),    # P5
    (11, 6),   # P6
    (11, -6),  # P7
    (9, -6),   # P8
    (-7, -4),  # P9
    (6, 4),    # P10
    (-5, -6),  # P11
    (4, 4)     # P12
]

polygon = [
    (-70, 40),   # D
    (-50, 60),   # B
    (40, 40),    # A'
    (60, 40),    # C'
    (90, 60),    # E
    (110, 60),   # F
    (110, -60),  # F'
    (90, -60),   # E'
    (60, -40),   # C
    (40, -40),   # A
    (-50, -60),  # B'
    (-70, -40)   # D'
]

A_triangles = []

'''We have to enter the first coordinate again at the end so as to perfectly 
   trianglate the polygon'''

def tri_poly_and_find_SG(polygon):
    triangles = tripy.earclip(polygon)
    #print(triangles)
    
    '''We introduces A_triangles to remove the last triangle from the
       triangulation because unnecessary coordinates are counted further'''
    
    A_triangles = []  
    for i in range(len(triangles)-1): 
        A_triangles.append(triangles[i])
        
    '''We introduce Plot_lstx and Plot_lsty to make list of X and Y coordinates
       of points of polygon to plot on the matplotlib'''
    
    Plot_lstx=[]; Plot_lsty=[];Diag_lstx=[];Diag_lsty=[];lst=[]
    for i in polygon:
        Plot_lstx.append(i[0])
        Plot_lsty.append(i[1])
        
    '''We append the first coordinate again in order to complete the polygon
       if in case we don't enter the first coordinate again in (polygon)'''
    
    Plot_lstx.append(Plot_lstx[0])   
    Plot_lsty.append(Plot_lsty[0])
    #print(Plot_lstx,Plot_lsty)
    
    '''We introduce Diag_lstx and Diag_lsty to make list of X and Y coordinates
       of points of triangles to plot on the matplotlib'''
    
    for i in triangles: 
        for j in i:
            Diag_lstx.append(j[0])
            Diag_lsty.append(j[1])
    A = final_security_guards(polygon,A_triangles)#check
    #print("The security guards are:",A)
    SGlstx = []; SGlsty = []
    
    '''we introduce SGlstx and SGlsty to make list of coordinates of security
       guards so as to plot them on matplotlib'''
    
    for i in range(len(A)):
        SGlstx.append(A[i][0])
        SGlsty.append(A[i][1])
    # plt.scatter(Diag_lstx,Diag_lsty,\
    # s = 200, marker = '.',color = 'r')
    plt.scatter(SGlstx,SGlsty,\
    marker = '.',s = 1000, color = 'k')
    plt.plot(Diag_lstx,Diag_lsty,color = 'g')
    plt.plot(Plot_lstx,Plot_lsty,color = 'b')
    End = time.time()
    return plt.show(), print("The running time is:",(End - Start)),print("The end time:",End)

''' the function def most_freq() gives us the most frequent coordinate in
    the triangles and then we assign this coordinate as a fan center.'''

def most_freq(List): 
    counter = 0;num = List[0] 
    for i in List: 
        curr_freq = List.count(i) 
        if(curr_freq> counter): 
            counter = curr_freq
            num = i
    return num

''' the function def fan_components gives us the list of coordinates of polygon
    and their occurances, so using most_freq function on this list gives us
    the fan centers.'''

def fan_components(polygon,triangles):# complexity o(n^3)
    lst = []
    for i in range(0,len(polygon)-1): 
         for j in range(0,len(triangles)):  
             for k in range(0,3):
                 if polygon[i]==triangles[j][k]:
                     lst.append(triangles[j][k])
                 else:
                    continue
    return lst

''' the function def chk_pts() gives us the update list of triangles after
    removing the processed most frequent element triangles from the list.'''

def chk_pts(triangles):
    X =[]
    for i in range(len(triangles)):
        if most_freq(fan_components(polygon,triangles))in triangles[i]:
            continue
        else:
            X.append(triangles[i])
    return X
Flst = []; lst = []; M = []; X = []

''' the function def final_security_guards() gives us the final list of the
    security guard which can cover the total boundary of the polygon and can be
    plotted on matplotlib'''

def final_security_guards(polygon,A_triangles): #check A_triangles
    while A_triangles != []:
        lst = fan_components(polygon,A_triangles) #complexity 3+1 = O(n^4)
        #print(lst)
        M  = most_freq(lst)
        Flst.append(M)
        X = chk_pts(A_triangles)
        A_triangles = X                 
    return Flst                         
#polygon = list();X = list();Y = list()  
'''while True:
    Vx = input("Enter the x coordinates:")
    if Vx == "done": break
    try: Vx = float(Vx)
    except: print("Invalid Input");continue
    X.append(Vx)
    Vy = input("Enter the y coordinates:")
    if Vy == "done": break
    try: Vy = float(Vy)
    except: print("Invalid Input");continue
    Y.append(Vy)
polygon = [(X[i],Y[i]) for i in range(0,len(X))]'''
tri_poly_and_find_SG(polygon)


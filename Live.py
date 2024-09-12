MOVIES=["Inception","Interstellar","John Wick 4","Casino Royale"]
SCREENS = 4
SEATS =['D10', 'D09', 'D08', 'D07', 'D06', 'D05', 'D04', 'D03', 'D02', 'D01',
        'C10', 'C09', 'C08', 'C07', 'C06', 'C05', 'C04', 'C03', 'C02', 'C01',
        'B10', 'B09', 'B08', 'B07', 'B06', ' B05', 'B04', 'B03', 'B02', 'B01',
        'A10', 'A09', 'A08', 'A07', 'A06', 'A05', 'A04', 'A03', 'A02', 'A01']


import mysql.connector as M
def connect():
        return M.connect(user="root",password="root",host="localhost",database="theatre")

def init(): #Initialize databases
    con=connect()
    C=con.cursor()
    try:
        C.execute("DROP DATABASE THEATRE")
    except:
        pass
    C.execute("CREATE DATABASE THEATRE")
    C.execute("USE THEATRE")   
    C.execute("CREATE TABLE Movies(MCode int(1) primary key,MName varchar(64))")
    C.execute("CREATE TABLE Screens(Screen int(1) Primary key)")
    C.execute("CREATE TABLE Tickets(id int(1) Primary key,name varchar(64),screen int,movie varchar(64),\
                seat varchar(10),time varchar(64))")             
    for i in range(len(MOVIES)):
      C.execute("insert into Movies values(%s,'%s')"%(i+1,MOVIES[i]))
    for i in range(SCREENS):
        C.execute("insert into Screens value(%s)"%(i+1))
    C.execute("alter table screens add(t1 varchar(999) default '[]')")
    C.execute("alter table screens add(t2 varchar(999) default '[]')")
    C.execute("alter table screens add(t3 varchar(999) default '[]')")
    con.commit()
    con.close()
    
def space(s,u):
    print(' '*s,'_'*u)
    
def printMovies():
    con=connect()
    C=con.cursor()
    C.execute("select * from MOVIES")
    cf= C.fetchall()
    space(0,21)
    print(" "*7,"MOVIES")
    for i in cf:
        print ('¦',i[0],''*3,i[1])
    con.close()
def printScreens():
   for i in range(SCREENS):
       print("¦",i+1," SCREEN",str(i+1))
def printTimings():
    print("¦",1,"MORNING 9:00 AM")
    print("¦",2,"NOON 1:00 PM")
    print("¦",3,"NIGHT 7:00 PM")

def getScreens(a_):
    con= connect()
    C=con.cursor()
    C.execute("select Screen,t%s from screens"%(a_))
    return C.fetchall()
     


  
def DISPLAYSEATS(MSeat,MAudi,MTime,MName):#movie Seating  variable
    m_l =len(MName)
    print(" "*(30-m_l),"¦"+MAudi,' '*(m_l+1),"¦")
    print(" "*(30-m_l),"¦Movie:",MName," ¦")
    print(" "*(30-m_l),"¦Time:",MTime," "*(m_l-7),"¦")
    print(" "*(30-m_l),"¦Capacity:", len(MSeat)," "*(m_l-5),"¦")
    print(" "*(30-m_l),"¦Available:",len(MSeat)-MSeat.count(" X ")," "*(m_l-6),"¦")
    print()
    for r  in range( len(MSeat)//10):
        print(end="|  ")
        for c in range(10):
            print(MSeat[10*r+c],end="")
            print(" "*2,end="")
            if c==4:
                print(" "*5,end='')
        print(end=" |")
        print("\n")
    print(" "*17,"_________________________")
    print(" "*17,"#######SCREEN HERE#######")










init()

while True:
    print("\
    ¦1| View Movies        ¦\n\
    ¦2| Book Tickets       ¦ \n\
    ¦3| Edit Tickets       ¦ \n\
    ¦4| Print Tickets      ¦ \n\
    ¦5| View Screen Status ¦\n\
    ")
    CHOICE=int(input("¦ Enter your choice: "))

    if CHOICE == 1: #View Movies
        printMovies()

    if CHOICE == 2:
        space(0,45)
        print(" "*15,"TICKET BOOKING")
        print("(1/3) SELECT MOVIE")
        printMovies();print()
        movieC=int(input("¦ Enter movie code: "))
        space(0,21)
        printTimings();print()
        movieT=int(input("¦ Enter movie timing code: "))
        space(0,21)
        c_gScreen = getScreens(movieT)
        print(" "* 5,"Screen status for given timing")
        countFree=SCREENS
        canBook=False
        for i in range(len(c_gScreen)):
            try:
                print("¦ ",i+1,"   SCREEN",c_gScreen[i][0]," "*5,MOVIES[eval(c_gScreen[i][1])[1]] )
                countFree-=1
            except:
                print("¦ ",i+1,"   SCREEN",c_gScreen[i][0]," "*5,"TBD" )
        if countFree !=0:
            movieS=int(input("¦ Enter Screen code: "))
            try:
                if eval(c_gScreen[i][1])[1] == movieS:
                    canBook= True

            except:
                canBook = True
        

            if canBook == True:
                #Book
                pass
            else:
                print("No Screens found Matching Conditions, Try again")
                continue
        else:
            continue






            
    continue_choice=input("Continue? ")
    if continue_choice in "Nn":
        break

  
  
  

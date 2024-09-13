import mysql.connector as M

MOVIES=["Inception","Interstellar","John Wick 4","Casino Royale"]
scr=["Screen 1","Screen 2", "Screen 3","Screen 4"]
TIMINGS=["MORNING 9:00 AM","NOON 1:00 PM","NIGHT 7:00 PM"]
TIME=["9:00 AM","1:00 PM","7:00 PM"]
SCREENS = 4
SEATS =['D10', 'D09', 'D08', 'D07', 'D06', 'D05', 'D04', 'D03', 'D02', 'D01',
        'C10', 'C09', 'C08', 'C07', 'C06', 'C05', 'C04', 'C03', 'C02', 'C01',
        'B10', 'B09', 'B08', 'B07', 'B06', 'B05', 'B04', 'B03', 'B02', 'B01',
        'A10', 'A09', 'A08', 'A07', 'A06', 'A05', 'A04', 'A03', 'A02', 'A01']



def connect():
        return M.connect(user="root",password="root",host="localhost",database="theatre")

def init(): #Initialize databases
    con=M.connect(user="root",password="root",host="localhost")
    C=con.cursor()
    try:
        C.execute("DROP DATABASE THEATRE")
    except:
        pass
    C.execute("CREATE DATABASE THEATRE")
    C.execute("USE THEATRE")   
    C.execute("CREATE TABLE Movies(MCode int(1) primary key,MName varchar(64))")
    C.execute("CREATE TABLE Screens(Screen int(1) Primary key)")
    C.execute("CREATE TABLE Tickets(id int(1) Primary key,\
              name varchar(64),\
              movie int,\
              time int,\
              screen int,\
                seat varchar(10))")             
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
    print("¦",1,TIMINGS[0])
    print("¦",2,TIMINGS[1])
    print("¦",3,TIMINGS[2])

def getScreens(a_):
    con= connect()
    C=con.cursor()
    C.execute("select Screen,t%s from screens"%(a_))
    kkk=C.fetchall()
    con.close()
    return kkk


  
def DISPLAYSEATS(MSeat,MScreen,MTime,MName):#movie Seating  variable
    m_l =len(MName)
    print(" "*(30-m_l),"¦"+MScreen,' '*(m_l-1),"¦")
    print(" "*(30-m_l),"¦Movie:",MName," ¦")
    print(" "*(30-m_l),"¦Time:",MTime," "*(m_l-6),"¦")
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
        if movieC>len(MOVIES):
                print("|||| ENTER CORRECT MOVIE CODE, TRY AGAIN")
                continue
        space(0,21)
        printTimings();print()
        movieT=int(input("¦ Enter movie timing code: "))
        if movieT>len(TIMINGS):
                print("|||| ENTER CORRECT TIMING CODE, TRY AGAIN")
                continue
        space(0,21)
        c_gScreen = getScreens(movieT)
        print(" "* 5,"Screen status for given timing")
        countFree=SCREENS
        canBook=False
        for i in range(len(c_gScreen)):
            
            try:
                print("¦ ",i+1,"   SCREEN",c_gScreen[i][0]," "*5,MOVIES[(eval(c_gScreen[i][1])[0])-1] )
                if movieC!=eval(c_gScreen[i][1])[0]:
                    countFree-=1
            except:
                print("¦ ",i+1,"   SCREEN",c_gScreen[i][0]," "*5,"TBD" )
        
        if countFree >0:
            movieS=int(input("¦ Enter Screen code: "))
            print(c_gScreen[movieS-1])
            if movieS>SCREENS:
                print("|||| ENTER CORRECT SCREEN CODE, TRY AGAIN")
                continue
            try:
                if eval(eval(c_gScreen[movieS-1])[1])[0] == movieC:
                    canBook= True
                
            except:
                if len(eval(c_gScreen[movieS-1][1]))==0:
                    canBook = True

        if canBook == True:
            
            no_Tickets = int(input("¦ Enter number of tickets:"))
            for i in range(no_Tickets):

                #
                print("Booking Ticket",i+1)
                movieP=input("Enter your name: ")
                if len(movieP)>63:
                    print("Error: Name should be less than 64 characters")
                    continue
                con= connect()
                C=con.cursor()
                C.execute("Select t%s from screens where screen=%s"%(movieT,movieS))
                print(C.fetchall())
                try:
                    moviePlan=(eval(C.fetchall()[0][0]))[1]
                        
                except:
                    
                    moviePlan=SEATS
                    
                con.close()
                
                
                DISPLAYSEATS(moviePlan,scr[movieS-1],TIME[movieT-1],MOVIES[movieC-1])
                movieSeat=input("Enter correct Seat code: ")
                if movieSeat not in moviePlan or movieSeat==' X ':
                    print("Error: Enter Correct Seat Number")
                    print("Ticket Not Booked")
                    continue

                con=connect()
                C=con.cursor()
                C.execute('Select id from tickets')
                existingId=[]
                for i in C.fetchall():
                    existingId.append(i[0])
                lastTicket=0
                con.close()
                if len(existingId)>0:
                    lastTicket=existingId[-1]
                movieTID=lastTicket+1

                for i in range(len(moviePlan)):
                    if moviePlan[i]==movieSeat:
                        moviePlan[i]=' X '
                

                movieTicket=[movieTID,movieP,movieC,movieT,movieS,movieSeat]
                con=connect()
                C=con.cursor()
                C.execute("Insert into tickets values(%s,'%s',%s,%s,%s,'%s')\
                            "%(movieTID,movieP,movieC,movieT,movieS,movieSeat))
                
                C.execute("update screens set t%s = %s where screen=%s",(movieT,str([movieC,moviePlan]),movieS))


                con.commit()
                con.close()

                print("ticket booked, your Ticket Id is",movieTID)
        else:
            print("No Screens found Matching Conditions, Try again")
            continue

    if CHOICE==3:
        ID=int(input("Enter Ticket id: "))
        con=connect()
        C=con.cursor()
        C.execute("Select id from tickets")
        idExists=False
        for i in range(len(C.fetchall())):
            if C.fetchall()[i][0] == ID:
                idExists==True
        if idExists == False:
            print("Id does not exist")
            continue
        else:
            print("Id exists")

            #C.execute("Select * from tickets where id")

    if CHOICE==4:
        id=int(input("Enter ticket Id:"))
        con=connect()
        C=con.cursor()
        C.execute("Select id from tickets")
        t=len(C.fetchall())
        for i in C.fetchall():
            if i[0] != id:
                t-=1
        if t == 0:
            print("Ticket id does not exist")
            continue
        C.execute("Select * from tickets where id=%s"%(id))
        for i in C.fetchall():
            for j in i:
                if type(j) != list:
                    print(j,end='  ')
            print()
        
        con.close()
    
    if CHOICE==5:
        con=connect()
        C=con.cursor()
        C.execute("Select t1,t2,t3 from screens")
        t=C.fetchall()
        con.close()
        for i in TIMINGS:
            print(i,end='\t')
        print()    
        for i in range(len(t)):
            print("Screen",i+1,end="\t")
            for j in range(len(t[i])):
                try:
                    print(MOVIES[eval(t[i][j])[0]-1], end="\t")
                except:
                    print("Available", end="\t")
            print()


            
    continue_choice=input("Continue? ")
    if continue_choice in "Nn":
        break

  
  
  

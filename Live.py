MOVIES=["Inception","Interstellar","John Wick 4","Casino Royale"]
SCREENS = 4
SEATS =['D10', 'D09', 'D08', 'D07', 'D06', 'D05', 'D04', 'D03', 'D02', 'D01',
        'C10', 'C09', 'C08', 'C07', 'C06', 'C05', 'C04', 'C03', 'C02', 'C01',
        'B10', 'B09', 'B08', 'B07', 'B06', ' B05', 'B04', 'B03', 'B02', 'B01',
        'A10', 'A09', 'A08', 'A07', 'A06', 'A05', 'A04', 'A03', 'A02', 'A01']





import mysql.connector as M
def connect(s):
    if s==True:
        connect_t= M.connect(user="root",password="root",host="localhost")
        return connect_t
    else:
        connect_t=M.connect(user="root",password="root",host="localhost",database="THEATRE")
        return connect_t
        
con=connect(1)
C=con.cursor()

C.execute("DROP DATABASE IF EXISTS THEATRE")
C.execute("CREATE DATABASE THEATRE")
C.execute("USE THEATRE")

  
C.execute("CREATE TABLE Movies(MCode int(1) primary key,MName varchar)")
for i in MOVIES:
  C.execute("insert into Movies values(%s,'%s')"%(i,i[1]))
C.execute("CREATE TABLE Screen(Screen int(1) Primary key,Morning varchar,Noon varchar, Night varchar)")

for i in range(SCREENS):
  C.execute("INSERT INTO Movies values(%s)"%(i))

C.execute("CREATE TABLE Tickets(Screen int(1) Primary key,Morning varchar,Noon varchar, Night varchar)")

for i in  range(SCREENS):
  C.execute("INSERT INTO Tickets values(%s)"%(i))
con.commit()
con.close()

def getMovies():
    con=connect()
    C=con.cursor()
    C.execute("USE THEATRE")
    C.execute("select * from MOVIES")
    gm_M=C.fetchall()
    con.close()
    return gm_M
     


  
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
        u_movies=getMovies()
        for i in u_movies:
            print (i)
    continue_choice=input("Continue? ")
    if continue_choice in "Nn":
        break

  
  
  

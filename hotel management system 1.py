import datetime
import pandas as pd
import math
from datetime import date

import mysql.connector as sql
con=sql.connect(host='localhost',user='root',password='a',db='hotel_insignia',charset='utf8')
c=con.cursor(buffered=True)

def pricebreakup():
    print('''OUR PRICE BREAKUP-->
+---------------------------------------+
| CHARGES PER ROOM TYPE -->             |
+---------------------------------------+
|# Normal --> Rs.1500                   |
|# Luxury --> Rs.3000                   |
+---------------------------------------+''')
    print('''
+----------------------------------------+
| RESTAURANT MENU -->                    |
+----------------------------------------+
|# TEA/COFFEE --> Rs.20                  |
|# BREAKFAST VEG COMBO --> Rs.50         |
|# BREAKFAST NON-VEG COMBO --> Rs.250    |
|# LUNCH/DINNER VEG COMBO--> Rs.550      |
|# LUNCH/DINNER NON-VEG COMBO--> Rs.1250 |
+----------------------------------------+''')
    print()

def checkinout(name,adhaar,hout,num):
    while 1!=0:
        c.execute('select * from bookings where roomno='+str(num)+" and name='"+name+"' and adhaarno='"+adhaar+"';")
        data=c.fetchall()
        if len(data)==0:
            print('Enter correct details')
            continue
        nowtime=datetime.datetime.now()
        nt=nowtime.strftime('%Y-%M-%D %H:%M:%S')
        chin=nt[:5]+nt[8:10]+'-'+nt[11:13]+nt[16:]
        c.execute("update bookings set "+hout+"='"+chin+"' where roomno="+str(num)+" and name='"+name+"' and adhaarno='"+adhaar+"';")
        con.commit()
        if hout=='checkout':
            c.execute("update rooms set occupied='NO' where roomno="+str(num)+";")
            con.commit()
            billing(name,adhaar,num)
        break

def roomno(name,adhaar):
    phone=input('Enter your phone number: ')
    n=int(input('Enter the number of rooms you would like to book: '))
    print("We have the following rooms available for you:-")
    print("1) Normal----->Rs1500/- per night")
    print("2) Luxury----->Rs3000/- per night")   
    while 1!=0:
        x=int(input("Enter Your Choice Please: "))
        if(x==1):
            print("you have opted for Normal")
            s=1500
            room='normal'
        elif(x==2):
            print("you have opted for Luxury")
            s=3000
            room='luxury'
        else:
            print("Please choose a correct room option")
            continue
        c.execute("select roomno from rooms where occupied='NO' and roomtype='"+room+"';")
        rs=c.fetchall()
        if len(rs)==n:
            print('Rooms are not available')
            print('Please choose again')
            continue
        else:
            break
    roomlist=[]
    print('Your rooms are',end=' ')
    for i in rs[0:n]:
        print(i[0],end=' ')
        roomlist=roomlist+[i[0]]
    print()
    nowtime=datetime.datetime.now()
    nt=nowtime.strftime('%Y-%M-%D %H:%M:%S')
    nt=nt[:5]+nt[8:10]+'-'+nt[11:13]+nt[16:]
    chin='0000-00-00 00:00:00'
    chou='0000-00-00 00:00:00'
    rbill=0
    for i in roomlist:
        c.execute('insert into bookings values(%s, "%s", "%s", "%s", "%s", "%s", %s, "%s", %s);' %(i, name ,adhaar, phone, chin, chou, s, nt, rbill))
        c.execute("update rooms set occupied='YES' where roomno="+str(i)+";")
    con.commit()
    listt=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    while 1!=0:
        yn=input('Do you want to check in(y/n): ')
        if yn=='y':
            for i in range(n):
                chin=checkinout(name,adhaar,"checkin",roomlist[i])
            break
        elif yn=='n':
            break
        else:
            print('Enter correct input')
            continue
    c.execute('select * from bookings where name="%s" and adhaarno="%s";' %(name,adhaar))
    data=c.fetchall()
    print('Your details:')
    print(pd.DataFrame(data,columns=['Room Number','Name','Adhaar Card Number','Phone Number','Check in date/time','Check out date/time','Bill','Booking Time','Restraunt Bill'],index=listt[0:n]))

def billing(name,adhaar,num):
    c=con.cursor(buffered=True)
    c.execute('select bill,checkin,checkout,rbill from bookings where roomno='+str(num)+" and name='"+name+"' and adhaarno='"+adhaar+"';")
    data=c.fetchall()
    roombill=data[0][0]
    t2=str(data[0][1])
    t1=str(data[0][2])
    d1=date(int(t2[0:4]),int(t2[5:7]),int(t2[8:11]))
    d2=date(int(t1[0:4]),int(t1[5:7]),int(t1[8:11]))
    l=str(d2-d1)
    a=l[0:-14]*roombill
    d=((int(t1[11:13])-int(t2[11:13]))*roombill/24)
    bill=a+d+(data[0][3])
    print("Amount for Room No.",num,"is",math.ceil(bill))

def restraunt():
    while 1!=0:
        print('''
+------------------------------------------+
| RESTAURANT MENU -->                      |
+------------------------------------------+
|1) TEA/COFFEE --> Rs.20                   |
|2) BREAKFAST VEG COMBO --> Rs.150         |
|3) BREAKFAST NON-VEG COMBO --> Rs.250     |
|4) LUNCH/DINNER VEG COMBO --> Rs.550      |
|5) LUNCH/DINNER NON-VEG COMBO --> Rs.1250 |
+------------------------------------------+''')
        choice=int(input("Enter the number that you want to order: "))
        if choice==1:
            bil=20
        elif choice==2:
            bil=150
        elif choice==3:
            bil=250
        elif choice==4:
            bil=550
        elif choice==5:
            bil=1250
        else:
            print("Enter correct choice")
            continue
        name=input('Enter your name: ')
        num=int(input("Enter your room number: "))
        c.execute('select rbill from bookings where roomno='+str(num)+" and name='"+name+"';")
        rbil=c.fetchall()
        if len(rbil)==0:
            print('Enter correct details')
            continue
        rbil=rbil[0][0]
        sett=int(input("Enter the number of sets you want to order: "))
        bil=bil*sett
        bil=bil+rbil
        c.execute("update bookings set rbill=%s where name='%s' and roomno= %s;" %(bil,name,num))
        con.commit()
        break

def Insignia():
    print("******WELCOME TO HOTEL INSIGNIA******")
    while 1!=0:
        print('''MENU:-
1) OUR PRICE BREAKUP
2) BOOK A ROOM 
3) CHECK IN
4) CHECK OUT
5) RESTAURANT
6) EXIT''')
        ch=int(input('Enter your choice: '))
        if(ch==1):
            pricebreakup()
        elif(ch==2):
            name=input('Enter your name: ')
            adhaar=input('Enter Adhaar card number: ')
            roomno(name,adhaar)
        elif(ch==3):
            name=input('Enter your name: ')
            adhaar=input('Enter Adhaar card number: ')
            num=int(input('Enter room number: '))
            checkinout(name,adhaar,"checkin",num)
        elif(ch==4):
            name=input('Enter your name: ')
            adhaar=input('Enter Adhaar card number: ')
            num=int(input('Enter room number: '))
            checkinout(name,adhaar,"checkout",num)
        elif(ch==5):
            restraunt()
        elif(ch==6):
            print("Thank You")
            break
        else:
            print('Wrong input')
            continue

Insignia()

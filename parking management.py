import tkinter as tk
import mysql.connector as sql
from datetime import datetime
from datetime import timedelta
import pyfiglet
root = tk.Tk()
c1=tk.Canvas(root, bg='alice blue',width=1000, height=1000, relief='raised')#creating a window 1000*1000
c1.pack()

mydb=sql.connect(host='localhost', user='root', passwd="2003",database="pams", use_pure=True)#establishing connection between Python&MySQL
mycursor=mydb.cursor()

s = pyfiglet.figlet_format("PAMS",font="big")
ns=s.center(90)
print(ns)
#Creating Table in SQL
mycursor.execute("CREATE TABLE CARS(NAME CHAR(30),PASSWORD CHAR(20), CARDETAILS CHAR(30),COLOUR CHAR(20),SLOT int(20),ARRIVALTIME DATETIME,DEPARTURETIME DATETIME,TIMEDIFFERENCE CHAR(30), BILL CHAR(30));")
 
for i in range(1,11):

    def f():
            
            c1.delete("all")
            l1=tk.Label(root, text="PAMS",bg='snow')
            l1.config(font=('helvetica',30,"bold"))
            c1.create_window(500,140,window=l1)
                  
                  
                       


           
            l2=tk.Label(root, text="PRESS 1 TO ENTER OR PRESS 2 TO LEAVE",bg='snow')# User Choice to Enter or Exit Parking Lot
            l2.config(font=('helvetica',14))#size & font of above text 
            c1.create_window(500,200,window=l2)#assigning coordinates to above text 
            e1=tk.Entry(root)#creates entry box for user to type in and takes the entry 
            c1.create_window(500,240,window=e1)# config of entry box

            def loop():
                
                n=e1.get()# getting value from e1
                n1=int(n)#converting canvas text to int variable 
                if n1==1:# check for entry 
                    c1.delete("all")
                    l0=tk.Label(root, text="ENTER THE FOLLOWING DETAILS:")#asking user to enter following details
                    l0.config(font=('helvetica',18))
                    c1.create_window(500,60,window=l0)

                    l3=tk.Label(root, text="Name:")
                    l3.config(font=('helvetica',14))
                    c1.create_window(400,100,window=l3)
                    e2=tk.Entry(root)
                    c1.create_window(515,100,window=e2)
                    
     
                    l4=tk.Label(root, text="Password:")
                    l4.config(font=('helvetica',14))
                    c1.create_window(400,150,window=l4)
                    e3=tk.Entry(root)
                    c1.create_window(515,150,window=e3)
                    
                    l5=tk.Label(root, text="Car Details:")
                    l5.config(font=('helvetica',14))
                    c1.create_window(400,200,window=l5)
                    e4=tk.Entry(root)
                    c1.create_window(515,200,window=e4)
                    
                    l6=tk.Label(root, text="Car Colour:")
                    l6.config(font=('helvetica',14))
                    c1.create_window(400,250,window=l6)
                    e5=tk.Entry(root)
                    c1.create_window(515,250,window=e5)

   
                    def sl():
                        
                        slot=1
                        
                        
                        name1=e2.get()
                        name=str(name1)
                        pswd1=e3.get()
                        pswd=str(pswd1)
                        crdet1=e4.get()
                        crdet=str(crdet1)
                        color1=e5.get()
                        color=str(color1)
                        arvtime = datetime.now()
                       
                        
                        mycursor.execute("INSERT INTO CARS"
                                   "(NAME,PASSWORD,CARDETAILS,COLOUR,SLOT,ARRIVALTIME)"
                                     "VALUES(%s,%s,%s,%s,%s,%s)",(name,pswd,crdet,color,slot,arvtime))#inserting user details into sql query 
                        mydb.commit()
                        
                        c1.delete("all")
                        
                        l7=tk.Label(root, text="THE SLOT ASSIGNED TO YOU IS :")
                        l7.config(font=('helvetica',14))
                        c1.create_window(400,100,window=l7)
                        l8=tk.Label(root, text=slot)
                        l8.config(font=('helvetica',14))
                        c1.create_window(580,100,window=l8)
                        
                        b2=tk.Button(text="NEXT",command=f, bg='brown',fg='white',font=('helvetica',9,'bold'))#creating a button 
                        c1.create_window(460,150,window=b2)
                        b2.update()
                        
                    
                    
                    b1=tk.Button(text="ENTER",command=sl,bg='brown',fg='white',font=('helvetica',9,'bold'))
                    c1.create_window(515,300,window=b1)
                    b1.update()
         
                    
                       
                if n1==2:#checking for exit
                     
                     c1.delete("all")
                     def check():
                         
                         l9=tk.Label(root, text=" PLEASE ENTER YOUR PASSWORD:")#to verify the user 
                         l9.config(font=('helvetica',14))
                         c1.create_window(400,150,window=l9)
                         e9=tk.Entry(root)
                         c1.create_window(650,150,window=e9)
                        

                         l10=tk.Label(root, text=" PLEASE ENTER YOUR CAR DETAILS:")#to verify the user
                         l10.config(font=('helvetica',14))
                         c1.create_window(400,200,window=l10)
                         e10=tk.Entry(root)
                         c1.create_window(650,200,window=e10)
                         
                         def cbill():
                              c1.delete("all")
                              passcheck1=e9.get()
                              passcheck=str(passcheck1)
                              
                              cdcheck1=e10.get()
                              cdcheck=str(cdcheck1)
                         
                         
                              deptime=datetime.now()
                              deptimee=str(deptime)  
                              sql_select_Query = "select * from Cars where password='"+passcheck+"' and cardetails='"+cdcheck+"';"#to check for the specific user whose password and cardetails match 
                              mycursor.execute(sql_select_Query)
                              
                              
                              records=mycursor.fetchall()#extracting the query 
                         
                              l11=tk.Label(root, text=" CUSTOMER DETAILS")# printing the bill
                              l11.config(font=('helvetica',18,"bold"))
                              c1.create_window(500,100,window=l11)
                              i=100
                              for row in records:#extracting rows from that query
                                  
                                  l12=tk.Label(root, text=" NAME:")
                                  l12.config(font=('helvetica',14))
                                  c1.create_window(300,200,window=l12)
                                  l13=tk.Label(root, text=row[0])
                                  l13.config(font=('helvetica',14))
                                  c1.create_window(500,200,window=l13)

                                  l14=tk.Label(root, text=" CAR DETAILS:")
                                  l14.config(font=('helvetica',14))
                                  c1.create_window(300,250,window=l14)
                                  l15=tk.Label(root, text=row[2])
                                  l15.config(font=('helvetica',14))
                                  c1.create_window(500,250,window=l15)

                                  l16=tk.Label(root, text=" CAR COLOUR:")
                                  l16.config(font=('helvetica',14))
                                  c1.create_window(300,300,window=l16)
                                  l17=tk.Label(root, text=row[3])
                                  l17.config(font=('helvetica',14))
                                  c1.create_window(500,300,window=l17)

                                  l18=tk.Label(root, text=" SLOT NUMBER:")
                                  l18.config(font=('helvetica',14))
                                  c1.create_window(300,350,window=l18)
                                  l19=tk.Label(root, text=row[4])
                                  l19.config(font=('helvetica',14))
                                  c1.create_window(500,350,window=l19)

                                  l20=tk.Label(root, text=" TICKET NUMBER:")
                                  l20.config(font=('helvetica',14))
                                  c1.create_window(300,400,window=l20)
                                  l21=tk.Label(root, text=i)
                                  l21.config(font=('helvetica',14))
                                  c1.create_window(500,400,window=l21)
                                  i=i+1

                                  l22=tk.Label(root, text=" ENTRY TIME:")
                                  l22.config(font=('helvetica',14))
                                  c1.create_window(300,450,window=l22)
                                  l23=tk.Label(root, text=row[5])
                                  l23.config(font=('helvetica',14))
                                  c1.create_window(500,450,window=l23)
                                  l24=tk.Label(root, text="EXIT TIME:")
                                  l24.config(font=('helvetica',14))
                                  c1.create_window(300,500,window=l24)
                                  l25=tk.Label(root, text=deptime)
                                  l25.config(font=('helvetica',14))
                                  c1.create_window(500,500,window=l25)
                                  
                                  
                                  def calctimediff(x,y):#calculating time difference and extracting the minutes
                                   
                                        #datetimeformat='%Y-%M-%d%H:%M:%S.%f'
                                        date1= deptime
                                        date2= row[5]
                                        diff= date1-date2
                                        totsec = diff.total_seconds()
                                        h = totsec//3600
                                        m = (totsec%3600) // 60
                                        m1=int(m)
                                        sec =(totsec%3600)%60
                                        l26=tk.Label(root, text="DURATION:")
                                        l26.config(font=('helvetica',14))
                                        c1.create_window(300,550,window=l26)
                                        l27=tk.Label(root, text=diff)
                                        l27.config(font=('helvetica',14))
                                        c1.create_window(500,550,window=l27)
                                        print("DURATION:",m1,"MINUTES",sec,"SECONDS")
                                        return m
          
                                  td = calctimediff(deptime,row[5])
                                  time=td
                                  tdd=str(td)
                                 
                                  sum=0
                                  def bill(time):#bill tariff
                                        if time<60:
                                            sum=15
                                        elif time>60 and time<180:
                                            sum=20
                                        elif time>180 and time<360:
                                            sum=30
                                        elif time>360 and time<720:
                                            sum=55
                                        elif time>720 and time<1440:
                                            sum=65
                                        else:
                                            print("You have exceeded the limit for parking. A tow truck has been called. Please contact the authorities to retrieve car")
                                        return sum
                    
                                  a=bill(time)
                                  
   
                                  print("TOTAL: Rs",a)
                                  print("\t","THANK YOU!")
                                  print("\t","DRIVE SAFE.")
                                  l28=tk.Label(root, text="TOTAL:(₹)")#Displaying the amount 
                                  l28.config(font=('helvetica',14))
                                  c1.create_window(300,600,window=l28)
                                
                                  l30=tk.Label(root, text=a)
                                  l30.config(font=('helvetica',14))
                                  c1.create_window(505,600,window=l30)
                                  
                                  l31=tk.Label(root, text="THANK YOU!")
                                  l31.config(font=('helvetica',14,"bold italic"))
                                  c1.create_window(500,650,window=l31)
                                  
                                  l32=tk.Label(root, text="DRIVE SAFE.")
                                  l32.config(font=('helvetica',14,"bold italic"))
                                  c1.create_window(500,700,window=l32)
                                  b4=tk.Button(text="NEXT",command=f, bg='brown',fg='white',font=('helvetica',9,'bold'))# for the next user to enter or leave
                                  c1.create_window(500,750,window=b4)
                                  b4.update()
                                  
                                
                         b3=tk.Button(text="NEXT",command=cbill, bg='brown',fg='white',font=('helvetica',9,'bold'))
                         c1.create_window(550,250,window=b3)
                         b3.update()
                     check()
                     

            b=tk.Button(text="Enter",command=loop,bg='brown',fg='white',font=('helvetica',9,'bold'))
            c1.create_window(500,280,window=b)    
            
    f()


import sys
import random
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox, QLineEdit
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.uic import loadUi
import mysql.connector
import smtplib
from email.message import EmailMessage


mydb = mysql.connector.connect(host="bzf2fyi4xvsv6xzguzrq-mysql.services.clever-cloud.com" ,user="uyag4sfjf0h8anbb", passwd="yn8qWQqO3pC6yHpWUhzq", database="bzf2fyi4xvsv6xzguzrq")
mycursor = mydb.cursor()


##################################  MAIN PAGE  ##################################################
class MainClass(QtWidgets.QMainWindow):

	def __init__(self):
		super(MainClass,self).__init__()
		loadUi("tourn1.ui",self)
		self.register_button.clicked.connect(self.Open_register)
		self.signin_button.clicked.connect(self.Open_signin)


	def Open_register(self):
			register = Register()
			widget.addWidget(register)
			widget.setCurrentIndex(widget.currentIndex()+1)


	def Open_signin(self):
			signin = Signin()
			widget.addWidget(signin)
			widget.setCurrentIndex(widget.currentIndex()+1)







##########################################  REGISTER PAGE  ################################################
class Register(QtWidgets.QMainWindow):
	def __init__(self):
		super(Register,self).__init__()
		loadUi("tourn2.ui",self)
		self.pushButton_back.clicked.connect(self.Open_back)
		self.Button_register.clicked.connect(self.record_registration)


	def Open_back(self):
		back_to_main = MainClass()
		widget.addWidget(back_to_main)
		widget.setCurrentIndex(widget.currentIndex()+1)


	def record_registration(self):


		uid = self.lineEdit_uid.text()
		name = self.lineEdit_name.text()
		email = self.lineEdit_email.text()
		contact = self.lineEdit_contact.text()
		if self.lineEdit_password.text() == self.lineEdit_cpassword.text():
			password = self.lineEdit_password.text()
		else:
			self.passwd_error()


		if self.RB_admin.isChecked():
			query = "INSERT INTO admin (AdminId,Name,Email_ID,Contact_no,Password) VALUES (%s,%s,%s,%s,%s)"
		elif self.RB_owner.isChecked():
			query = "INSERT INTO owner (OwnerId,Name,Email_ID,Contact_no,Password) VALUES (%s,%s,%s,%s,%s)"
		elif self.RB_generaluser.isChecked():
			query = "INSERT INTO generaluser (UserId,Name,Email_ID,Contact_no,Password) VALUES (%s,%s,%s,%s,%s)"
		else:
			pass



		value = (uid,name,email,contact,password)
		mycursor.execute(query, value)
		mydb.commit()
		print("Account successfully created with user_id :",uid)

		signin_page_open = Signin()
		widget.addWidget(signin_page_open)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def passwd_error(self):
		print("Password not matching!")
		msg = QMessageBox()
		msg.setWindowTitle("Error message!")
		msg.setText("Password not matching!")
		msg.setIcon(QMessageBox.Information)
		msg.setStandardButtons(QMessageBox.Ok)
		x = msg.exec_()






#########################################  SIGN IN PAGE  ############################################
class Signin(QtWidgets.QMainWindow):
	def __init__(self):
		super(Signin,self).__init__()
		loadUi("tourn3.ui",self)
		self.pushButton_back.clicked.connect(self.Open_back)
		self.pushButton_login.clicked.connect(self.record_signin)
		self.pushButton_forgotpass.clicked.connect(self.ForgotPassword)

	def record_signin(self):
		print("Sign in Button clicked successfully!")
		uid = self.lineEdit_uid.text()
		password = self.lineEdit_password.text()

		cur=mydb.cursor()

		if self.RB_admin.isChecked() | self.RB_owner.isChecked() | self.RB_generaluser.isChecked():
			if self.RB_admin.isChecked():
				query = "SELECT * FROM admin WHERE AdminID=%s and Password=%s"
				exe=cur.execute(query,(uid,password))
			elif self.RB_owner.isChecked():
				query = "SELECT * FROM owner WHERE OwnerID=%s and Password=%s"
				exe=cur.execute(query,(uid,password))
			elif self.RB_generaluser.isChecked():
				query = "SELECT * FROM generaluser WHERE UserID=%s and Password=%s"
				exe=cur.execute(query,(uid,password))
			else:
				pass
				

			if(len(cur.fetchall())>0):
				if self.RB_admin.isChecked():
					HomePage_A = AdminHP(uid)
					widget.addWidget(HomePage_A)
					widget.setCurrentIndex(widget.currentIndex()+1)

				elif self.RB_owner.isChecked():
					HomePage_O = OwnerHP(uid)
					widget.addWidget(HomePage_O)
					widget.setCurrentIndex(widget.currentIndex()+1)

				elif self.RB_generaluser.isChecked():
					HomePage_U = GeneralUserHP(uid)
					widget.addWidget(HomePage_U)
					widget.setCurrentIndex(widget.currentIndex()+1)


				else:
					pass


				print("Successfully logged in")
			else:
				print("Fields doenst match! Try Again.")
				msg = QMessageBox()
				msg.setWindowTitle("Cannot login!")
				msg.setText("Fields doenst match! Try Again.")
				msg.setIcon(QMessageBox.Warning)
				msg.setStandardButtons(QMessageBox.Ok)
				msg.exec()
		else:
			msg = QMessageBox()
			msg.setWindowTitle("Cannot login!")
			msg.setText("Please select your user type!")
			msg.setIcon(QMessageBox.Warning)
			msg.setStandardButtons(QMessageBox.Ok)
			msg.exec()



	def Open_back(self):
		back_to_main = MainClass()
		widget.addWidget(back_to_main)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def ForgotPassword(self):
		pass_recovery_page = PasswordRecovery()
		widget.addWidget(pass_recovery_page)
		widget.setCurrentIndex(widget.currentIndex()+1)



############################################ SIGNIN PAGE END #############################################


############################################ PASSWORD RECOVERY PAGE #############################################
class PasswordRecovery(QtWidgets.QMainWindow):
	def __init__(self):
		super(PasswordRecovery,self).__init__()
		loadUi("PasswordRecovery.ui",self)
		self.pushButton_back.clicked.connect(self.Open_back)
		self.pushButton_sendemail.clicked.connect(self.SendEmail)

	def Open_back(self):
		back_to_main = MainClass()
		widget.addWidget(back_to_main)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def SendEmail(self):
		email = self.lineEdit_recoveryemail.text()
		print(email)
		# mydb = mysql.connector.connect(host="bzf2fyi4xvsv6xzguzrq-mysql.services.clever-cloud.com" ,user="uyag4sfjf0h8anbb", passwd="yn8qWQqO3pC6yHpWUhzq", database="bzf2fyi4xvsv6xzguzrq")
		cursorr = mydb.cursor()
		# try:
		if self.RB_admin.isChecked():
			query = "SELECT AdminID,Name,Email_ID,Contact_no,Password FROM admin WHERE Email_ID = %s"
		elif self.RB_owner.isChecked():
			query = "SELECT * FROM owner WHERE Email_ID = %s"
		elif self.RB_generaluser.isChecked():
			query = "SELECT * FROM generaluser WHERE Email_ID = %s"
		else:
			pass
		
		cursorr.execute(query,(email,))
		# mydb.commit()

		# exe = mycurr.execute(query , (email))
		AccountDetails = []	
		result = cursorr.fetchone()

		RowNum = 0
		for row in result:
			AccountDetails.append(result[RowNum])
			RowNum = RowNum + 1
		mydb.commit()		

		print(AccountDetails)
		User_ID = AccountDetails[0]
		Name = AccountDetails[1]
		Email_ID = AccountDetails[2]
		Contact_no = AccountDetails[3]
		Password = AccountDetails[4] 
		print(User_ID)
		print(Name)
		print(Email_ID)
		print(Contact_no)
		print(Password)


		msg = EmailMessage()
		msg.set_content(f'''
		<!doctype html>
		<html lang="en-US">

		<head>
			<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
			<title>Reset Password Email Template</title>
			<meta name="description" content="Reset Password Email Template.">
			


		</head>

		<body marginheight="0" topmargin="0" marginwidth="0" style="margin: 0px; background-color: #f2f3f8;" leftmargin="0">
			<!--100% body table-->
			<table cellspacing="0" border="0" cellpadding="0" width="100%" bgcolor="#f2f3f8"
				style="@import url(https://fonts.googleapis.com/css?family=Rubik:300,400,500,700|Open+Sans:300,400,600,700); font-family: 'Open Sans', sans-serif;">
				<tr>
					<td>
						<table style="background-color: #f2f3f8; max-width:670px;  margin:0 auto;" width="100%" border="0"
							align="center" cellpadding="0" cellspacing="0">
							<tr>
								<td style="height:80px;">&nbsp;</td>
							</tr>
							<tr>
								<td style="text-align:center;">
									<img width="120" src="https://www.khellindia.com/wp-content/uploads/2018/12/ipl.png" title="logo" alt="logo">
								  </a>
								</td>
							</tr>
							<tr>
								<td style="height:20px;">&nbsp;</td>
							</tr>
							<tr>
								<td>
									<table width="95%" border="0" align="center" cellpadding="0" cellspacing="0"
										style="max-width:670px;background:#fff; border-radius:3px; text-align:center;-webkit-box-shadow:0 6px 18px 0 rgba(0,0,0,.06);-moz-box-shadow:0 6px 18px 0 rgba(0,0,0,.06);box-shadow:0 6px 18px 0 rgba(0,0,0,.06);">
										<tr>
											<td style="height:40px;">&nbsp;</td>
										</tr>
										<tr>
											<td style="padding:0 35px;">
												<h1 style="color:blue; font-weight:500; margin:0;font-size:32px;font-family:'Rubik',sans-serif;">You have
													requested us for your login details.</h1>
												<span
													style="display:inline-block; vertical-align:middle; margin:29px 0 26px; border-bottom:1px solid #cecece; width:100px;"></span>
												<p style="color:#455056; font-size:15px;line-height:24px; margin:0;">
													Hi {Name},<br>
													
													As per your request we are providing you your login details.<br><br>

													User ID : {User_ID}<br>
													Name : {Name}<br>
													Email : {Email_ID}<br>
													Contact No. : +91 {Contact_no}<br>
													Password : {Password}<br>
													<br>
													Please do not share your password with anyone! <br><br>
													<b>Thank you.</b>
												</p>
												
											</td>
										</tr>
										<tr>
											<td style="height:40px;">&nbsp;</td>
										</tr>
									</table>
								</td>
							<tr>
								<td style="height:20px;">&nbsp;</td>
							</tr>
							
							<tr>
								<td style="height:80px;">&nbsp;</td>
							</tr>
						</table>
					</td>
				</tr>
			</table>
			<!--/100% body table-->
		</body>

		</html>
		''',subtype='html')
		msg['subject'] = "Password Recovery Email!"
		msg['to'] = Email_ID

		user = "sc.911gt@gmail.com"
		msg['from'] = user
		password = "kbvctlcddmijpnlj"

		server = smtplib.SMTP("smtp.gmail.com",587)

		server.starttls()
		server.login(user, password)
		server.send_message(msg)
		server.quit()

		# except:
		msg = QMessageBox()
		msg.setWindowTitle("Information")
		msg.setText("Login details successfully sent on your E-mail!")
		msg.setIcon(QMessageBox.Information)
		msg.setStandardButtons(QMessageBox.Ok)
		x = msg.exec_()


		
		signinpage = Signin()
		widget.addWidget(signinpage)
		widget.setCurrentIndex(widget.currentIndex()+1)
############################################ PASSWORD RECOVERY PAGE END#############################################


##########################################  ADMIN HOME PAGE  #############################################
class AdminHP(QtWidgets.QMainWindow):
	def __init__(self,uid):
		super(AdminHP,self).__init__()
		loadUi("tourn4a.ui",self)
		self.uid = uid
		self.pushButton_logout.clicked.connect(self.Logout)
		self.pushButton_teams.clicked.connect(self.Open_teamsA)
		self.pushButton_players.clicked.connect(self.Open_PlayersA)
		self.pushButton_pt.clicked.connect(self.Open_PointsTableA)
		
		self.pushButton_schedule.clicked.connect(self.Open_ScheduleA)
		self.pushButton_auction.clicked.connect(self.Open_Auction)

		self.pushButton_uid.setText(self.uid)

	def Logout(self):
		back_to_main = MainClass()
		widget.addWidget(back_to_main)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Open_teamsA(self):
		openA = TEAMS_A(self.uid)
		widget.addWidget(openA)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Open_PlayersA(self):
		openPlayers = Players_A(self.uid)
		widget.addWidget(openPlayers)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Open_PointsTableA(self):
		openPointsTable = PointsTable_A(self.uid)
		widget.addWidget(openPointsTable)
		widget.setCurrentIndex(widget.currentIndex()+1)

	

	def Open_ScheduleA(self):
		openSchedule = Schedule_A(self.uid)
		widget.addWidget(openSchedule)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Open_Auction(self):
		openAuction = Auction_A(self.uid)
		widget.addWidget(openAuction)
		widget.setCurrentIndex(widget.currentIndex()+1)
		# msg = QMessageBox()
		# msg.setWindowTitle("Action can't performed!")
		# msg.setText("Auction page is currently under maintenance!")
		# msg.setIcon(QMessageBox.Warning)
		# msg.setStandardButtons(QMessageBox.Ok)
		# x = msg.exec_()




##########################################  OWNER HOME PAGE  #############################################
class OwnerHP(QtWidgets.QMainWindow):
	def __init__(self,uid):
		super(OwnerHP,self).__init__()
		loadUi("tourn4o.ui",self)
		self.uid = uid
		self.pushButton_logout.clicked.connect(self.Logout)
		self.pushButton_teams.clicked.connect(self.Connect_to_teamsOU)
		self.pushButton_players.clicked.connect(self.Open_PlayersA)
		self.pushButton_pt.clicked.connect(self.Open_PointsTableA)
		self.pushButton_schedule.clicked.connect(self.Open_ScheduleA)
		self.pushButton_auction.clicked.connect(self.Open_Auction)

		self.pushButton_uid.setText(self.uid)

	def Logout(self):
		back_to_main = MainClass()
		widget.addWidget(back_to_main)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Connect_to_teamsOU(self):
		teamsOU = TEAMS_OU('Owner',self.uid)
		widget.addWidget(teamsOU)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Open_PlayersA(self):
		openPlayers = Players_OU('Owner',self.uid)
		widget.addWidget(openPlayers)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Open_PointsTableA(self):
		openPointsTable = PointsTable_OU('Owner',self.uid)
		widget.addWidget(openPointsTable)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Open_ScheduleA(self):
		openSchedule = Schedule_OU('Owner',self.uid)
		widget.addWidget(openSchedule)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Open_Auction(self):
		openAuction = Auction_O(self.uid)
		widget.addWidget(openAuction)
		widget.setCurrentIndex(widget.currentIndex()+1)
		# msg = QMessageBox()
		# msg.setWindowTitle("Action can't performed!")
		# msg.setText("Auction page is currently under maintenance!")
		# msg.setIcon(QMessageBox.Warning)
		# msg.setStandardButtons(QMessageBox.Ok)
		# x = msg.exec_()

###################################### GENERAL USER HOME PAGE  ############################################
class GeneralUserHP(QtWidgets.QMainWindow):
	def __init__(self,uid):
		super(GeneralUserHP,self).__init__()
		loadUi("tourn4u.ui",self)
		self.uid = uid
		self.pushButton_logout.clicked.connect(self.Logout)
		self.pushButton_teams.clicked.connect(self.Connect_to_teamsOU)
		self.pushButton_players.clicked.connect(self.Open_PlayersOU)
		self.pushButton_pt.clicked.connect(self.Open_PointsTableOU)
		self.pushButton_schedule.clicked.connect(self.Open_ScheduleOU)

		self.pushButton_uid.setText(self.uid)

	def Logout(self):
		back_to_main = MainClass()
		widget.addWidget(back_to_main)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Connect_to_teamsOU(self):
		teamsOU = TEAMS_OU('GeneralUser',self.uid)
		widget.addWidget(teamsOU)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Open_PlayersOU(self):
		openPlayers = Players_OU('GeneralUser',self.uid)
		widget.addWidget(openPlayers)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Open_PointsTableOU(self):
		openPointsTable = PointsTable_OU('GeneralUser',self.uid)
		widget.addWidget(openPointsTable)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Open_ScheduleOU(self):
		openSchedule = Schedule_OU('GeneralUser',self.uid)
		widget.addWidget(openSchedule)
		widget.setCurrentIndex(widget.currentIndex()+1)


###################################### TEAMS ADMIN PAGE  ############################################
class TEAMS_A(QtWidgets.QMainWindow):
	def __init__(self,uid):
		super(TEAMS_A,self).__init__()
		loadUi("teamsA.ui",self)
		self.uid = uid
		self.pushButton_back.clicked.connect(self.Home)
		self.pushButton_update.clicked.connect(self.Update)
		
		# displayquery = "SELECT Team,Owner,Captian,Coach,Home_Ground FROM team"
		# self.tableWidget_teamA.setRowCount(50)
		# tablerow = 0
		# for row in mycurr.execute(displayquery):
		# 	self.tableWidget_teamA.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
		# 	self.tableWidget_teamA.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[0]))
		# 	self.tableWidget_teamA.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[0]))
		# 	self.tableWidget_teamA.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[0]))
		# 	self.tableWidget_teamA.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(row[0]))
		# 	tablerow+=1

		try:
			mydb = mysql.connector.connect(host="bzf2fyi4xvsv6xzguzrq-mysql.services.clever-cloud.com" ,user="uyag4sfjf0h8anbb", passwd="yn8qWQqO3pC6yHpWUhzq", database="bzf2fyi4xvsv6xzguzrq")
			mycurr = mydb.cursor()
			# mycurr.execute("SELECT Team,Owner,Captian,Coach,Home_Ground FROM {}".format(team))
			mycurr.execute("SELECT Team,Owner,Captian,Coach,Home_Ground FROM team")

			result = mycurr.fetchall()
			self.tableWidget_teamA.setRowCount(0)
			for row_number, row_data in enumerate(result):
				print(row_number)
				self.tableWidget_teamA.insertRow(row_number)
				for column_number, data in enumerate(row_data):
					self.tableWidget_teamA.setItem(row_number, column_number, QTableWidgetItem(str(data)))

			mydb.commit() 

		except:
			print("Cannot display Teams Table")
			self.tableWidget_teamA.rowClicked.connect(row_number)

	def Home(self):
		backbutton = AdminHP(self.uid)
		widget.addWidget(backbutton)
		widget.setCurrentIndex(widget.currentIndex()+1)




	def Update(self):
		try:
			mycurr = mydb.cursor()
			rowCount = self.tableWidget_teamA.rowCount()
			print(rowCount)
			columnCount = self.tableWidget_teamA.columnCount()
			print(columnCount)
			for row in range(rowCount):
				rowNum = row + 1
				rowData = []
				for column in range(columnCount):
					widgetItem = self.tableWidget_teamA.item(row,column)
					if(widgetItem and widgetItem.text()):
						rowData.append(widgetItem.text())
					else:
						rowData.append('NULL')
				rowData.append(rowNum)
				print(rowData)
				# query = "INSERT INTO team (Team, Owner, Captian, Coach, Home_Ground) VALUES(%s, %s, %s, %s, %s)"
				query = "UPDATE team SET Team = %s, Owner = %s, Captian = %s, Coach = %s, Home_Ground = %s WHERE Team_ID = %s"
				mycurr.execute(query, rowData)
			mydb.commit()

			msg = QMessageBox()
			msg.setWindowTitle("Success!")
			msg.setText("Teams Table Updated Successfully!")
			msg.setIcon(QMessageBox.Information)
			msg.setStandardButtons(QMessageBox.Ok)
			x = msg.exec_()

		except:
			msg = QMessageBox()
			msg.setWindowTitle("Information!")
			msg.setText("Data Insertion Failed!")
			msg.setIcon(QMessageBox.Warning)
			msg.setStandardButtons(QMessageBox.Ok)
			x = msg.exec_()
		

# TeamID = [self.tableWidget_teamA.item(row,0).text() for row in range(self.tableWidget_teamA)]


		

		



###################################### TEAMS OWNER/GEN.USER PAGE  ############################################
class TEAMS_OU(QtWidgets.QMainWindow):
	def __init__(self,s,uid):
		super(TEAMS_OU,self).__init__()
		loadUi("teamsOU.ui",self)
		self.UserType = s
		self.uid = uid
		print(self.UserType)
		self.pushButton_back.clicked.connect(self.Back_to_HP)
		
		# try:
		mydb = mysql.connector.connect(host="bzf2fyi4xvsv6xzguzrq-mysql.services.clever-cloud.com" ,user="uyag4sfjf0h8anbb", passwd="yn8qWQqO3pC6yHpWUhzq", database="bzf2fyi4xvsv6xzguzrq")
		mycurr = mydb.cursor()
		# mycurr.execute("SELECT Team,Owner,Captian,Coach,Home_Ground FROM {}".format(team))
		mycurr.execute("SELECT Owner,Captian,Coach,Home_Ground FROM team")

		result = mycurr.fetchall()
		self.tableWidget_teamsOU.setRowCount(0)
		for row_number, row_data in enumerate(result):
			print(row_number)
			self.tableWidget_teamsOU.insertRow(row_number)
			for column_number, data in enumerate(row_data):
				self.tableWidget_teamsOU.setItem(row_number, column_number + 1, QTableWidgetItem(str(data)))

		mydb.commit()
		# except:	
		# 	print("Unable to display table content")

	def Back_to_HP(self):
		if self.UserType == 'Owner':
			back = OwnerHP(self.uid)
		else:
			back = GeneralUserHP(self.uid)
		widget.addWidget(back)
		widget.setCurrentIndex(widget.currentIndex()+1)

	
		

##################################  PLAYERS ADMIN PAGE  ##################################################
class Players_A(QtWidgets.QMainWindow):
	def __init__(self,uid):
		super(Players_A,self).__init__()
		loadUi("PlayersA.ui",self)
		self.uid = uid
		self.pushButton_back.clicked.connect(self.Home)
		self.pushButton_update.clicked.connect(self.Update)

		mydb = mysql.connector.connect(host="bzf2fyi4xvsv6xzguzrq-mysql.services.clever-cloud.com" ,user="uyag4sfjf0h8anbb", passwd="yn8qWQqO3pC6yHpWUhzq", database="bzf2fyi4xvsv6xzguzrq")
		mycurr = mydb.cursor()
		# mycurr.execute("SELECT Team,Owner,Captian,Coach,Home_Ground FROM {}".format(team))
		mycurr.execute("SELECT Name,Team,DOB,Role,Batting_Style,Bowling_Style,Matches,Runs,Wickets,IPL_Debut FROM player")

		result = mycurr.fetchall()
		self.tableWidget_playersA.setRowCount(0)
		for row_number, row_data in enumerate(result):
			print(row_number)
			self.tableWidget_playersA.insertRow(row_number)
			for column_number, data in enumerate(row_data):
				self.tableWidget_playersA.setItem(row_number, column_number, QTableWidgetItem(str(data)))

		mydb.commit()



	def Home(self):
		backbutton = AdminHP(self.uid)
		widget.addWidget(backbutton)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Update(self):
		msg = QMessageBox()
		msg.setWindowTitle("Success!")
		msg.setText("Players Data Updated Successfully!")
		msg.setIcon(QMessageBox.Information)
		msg.setStandardButtons(QMessageBox.Ok)
		x = msg.exec_()





###################################### PLAYERS OWNER/GEN.USER PAGE  ############################################
class Players_OU(QtWidgets.QMainWindow):
	def __init__(self,s,uid):
		super(Players_OU,self).__init__()
		loadUi("PlayersOU.ui",self)
		self.UserType = s
		self.uid = uid
		self.pushButton_back.clicked.connect(self.Back_to_HP)

		mydb = mysql.connector.connect(host="bzf2fyi4xvsv6xzguzrq-mysql.services.clever-cloud.com" ,user="uyag4sfjf0h8anbb", passwd="yn8qWQqO3pC6yHpWUhzq", database="bzf2fyi4xvsv6xzguzrq")
		mycurr = mydb.cursor()
		# mycurr.execute("SELECT Team,Owner,Captian,Coach,Home_Ground FROM {}".format(team))
		mycurr.execute("SELECT Name,Team,DOB,Role,Batting_Style,Bowling_Style,Matches,Runs,Wickets,IPL_Debut FROM player")

		result = mycurr.fetchall()
		self.tableWidget_playersOU.setRowCount(0)
		for row_number, row_data in enumerate(result):
			print(row_number)
			self.tableWidget_playersOU.insertRow(row_number)
			for column_number, data in enumerate(row_data):
				self.tableWidget_playersOU.setItem(row_number, column_number, QTableWidgetItem(str(data)))

		mydb.commit()


	def Back_to_HP(self):
		if self.UserType == 'Owner':
			back = OwnerHP(self.uid)
		else:
			back = GeneralUserHP(self.uid)
		widget.addWidget(back)
		widget.setCurrentIndex(widget.currentIndex()+1)
		




##################################  POINTS TABLE ADMIN PAGE  ##################################################
class PointsTable_A(QtWidgets.QMainWindow):
	def __init__(self, uid):
		super(PointsTable_A,self).__init__()
		loadUi("PointsTable_A.ui",self)
		self.uid = uid
		self.pushButton_back.clicked.connect(self.Home)
		# self.pushButton_qualifier.setVisible(False)
		self.pushButton_update.clicked.connect(self.Update)
		self.pushButton_qualifier.clicked.connect(self.Qualifier)


		mydb = mysql.connector.connect(host="bzf2fyi4xvsv6xzguzrq-mysql.services.clever-cloud.com" ,user="uyag4sfjf0h8anbb", passwd="yn8qWQqO3pC6yHpWUhzq", database="bzf2fyi4xvsv6xzguzrq")
		mycurr = mydb.cursor()
		mycursor = mydb.cursor()
		# mycurr.execute("SELECT Team,Owner,Captian,Coach,Home_Ground FROM {}".format(team))
		mycurr.execute("SELECT Team_name,Matches,Won,Lost,Points FROM pointstable ORDER BY Points DESC")

		result = mycurr.fetchall()
		self.tableWidget_PTA.setRowCount(0)
		for row_number, row_data in enumerate(result):
			print(row_number)
			self.tableWidget_PTA.insertRow(row_number)
			for column_number, data in enumerate(row_data):
				self.tableWidget_PTA.setItem(row_number, column_number , QTableWidgetItem(str(data)))

		mycursor.execute("Select Sum(Matches) From pointstable")
		result = mycursor.fetchone()

		mydb.commit()

		matches = result[0]

		if matches == 112.0:
			print("Successful 112")
			self.pushButton_qualifier.setVisible(True)
		else:
			print("Failed to load value")
			self.pushButton_qualifier.setVisible(False)

	def Home(self):
		backbutton = AdminHP(self.uid)
		widget.addWidget(backbutton)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Update(self):
		try:
			mydb = mysql.connector.connect(host="bzf2fyi4xvsv6xzguzrq-mysql.services.clever-cloud.com" ,user="uyag4sfjf0h8anbb", passwd="yn8qWQqO3pC6yHpWUhzq", database="bzf2fyi4xvsv6xzguzrq")
			mycurr = mydb.cursor()
			rowCount = self.tableWidget_PTA.rowCount()
			print(rowCount)
			columnCount = self.tableWidget_PTA.columnCount()
			print(columnCount)

			c = mydb.cursor()
			# for i in range(rowCount):
			TeamId = []
			c.execute("Select Team_ID from pointstable ORDER BY Points")
			result = c.fetchall()
			# TeamId.append(result)
			for row in result:
				TeamId.append(row[0])
			mydb.commit()
			print(TeamId)
			print(TeamId[1])




			for row in range(rowCount):
				rowData = []
				for column in range(columnCount):
					widgetItem = self.tableWidget_PTA.item(row,column)
					if(widgetItem and widgetItem.text()):
						rowData.append(widgetItem.text())
					else:
						rowData.append('NULL')
				rowData.append(TeamId[row])
				print(rowData)
				# query = "INSERT INTO team (Team, Owner, Captian, Coach, Home_Ground) VALUES(%s, %s, %s, %s, %s)"
				# (SELECT Team_ID from pointstable WHERE @row_number:= %s)
				query = "UPDATE pointstable SET Team_name = %s, Matches = %s, Won = %s, Lost = %s, Points = %s WHERE Team_ID = %s"
				mycurr.execute(query, rowData)
			mydb.commit()

			msg = QMessageBox()
			msg.setWindowTitle("Success!")
			msg.setText("Points Table Updated Successfully!")
			msg.setIcon(QMessageBox.Information)
			msg.setStandardButtons(QMessageBox.Ok)
			x = msg.exec_()

			mydb = mysql.connector.connect(host="bzf2fyi4xvsv6xzguzrq-mysql.services.clever-cloud.com" ,user="uyag4sfjf0h8anbb", passwd="yn8qWQqO3pC6yHpWUhzq", database="bzf2fyi4xvsv6xzguzrq")
			mycursor = mydb.cursor()
			mycursor.execute("Select Sum(Matches) From pointstable")
			result = mycursor.fetchone()
			mydb.commit()

			print(result)
			print(type(result))
			matches = result[0]
			print(type(matches))
			print(matches)
			# string1 = " "
			# matches = ' '.join(map(str,result))
			# print(matches)
			# print(type(matches))

			# a = matches.
			# matches = result(0)
			# if matches == 112.0:
			# 	print("Successful 112")
			# 	self.pushButton_qualifier.setVisible(True)
			# else:
			# 	print("Failed to load value")




			call_page_again = PointsTable_A(self.uid)
			widget.addWidget(call_page_again)
			widget.setCurrentIndex(widget.currentIndex()+1)
		except:
			msg = QMessageBox()
			msg.setWindowTitle("Warning!")
			msg.setText("Please fill all the fields!")
			msg.setIcon(QMessageBox.Warning)
			msg.setStandardButtons(QMessageBox.Ok)
			x = msg.exec_()

	def Qualifier(self):
		qualifier = Qualifier_A(self.uid)
		widget.addWidget(qualifier)
		widget.setCurrentIndex(widget.currentIndex()+1)



###################################### POINTS TABLE OWNER/GEN.USER PAGE  ############################################
class PointsTable_OU(QtWidgets.QMainWindow):
	def __init__(self,s,uid):
		super(PointsTable_OU,self).__init__()
		loadUi("PointsTable_OU.ui",self)
		self.UserType = s
		self.uid = uid
		self.pushButton_back.clicked.connect(self.Back_to_HP)
		self.pushButton_qualifier.clicked.connect(self.Qualifier)


		mydb = mysql.connector.connect(host="bzf2fyi4xvsv6xzguzrq-mysql.services.clever-cloud.com" ,user="uyag4sfjf0h8anbb", passwd="yn8qWQqO3pC6yHpWUhzq", database="bzf2fyi4xvsv6xzguzrq")
		mycursor = mydb.cursor()
		mycursor.execute("Select Sum(Matches) From pointstable")
		result = mycursor.fetchone()
		mydb.commit()

		matches = result[0]
		if matches == 112.0:
			print("Successful 112")
			self.pushButton_qualifier.setVisible(True)
		else:
			print("Failed to load value")
			self.pushButton_qualifier.setVisible(False)






		mydb = mysql.connector.connect(host="bzf2fyi4xvsv6xzguzrq-mysql.services.clever-cloud.com" ,user="uyag4sfjf0h8anbb", passwd="yn8qWQqO3pC6yHpWUhzq", database="bzf2fyi4xvsv6xzguzrq")
		mycurr = mydb.cursor()
		# mycurr.execute("SELECT Team_name,Matches,Won,Lost,Tied,Points FROM {}".format(team))
		mycurr.execute("SELECT Team_name,Matches,Won,Lost,Points FROM pointstable ORDER BY Points DESC")

		result = mycurr.fetchall()
		self.tableWidget_PTOU.setRowCount(0)
		for row_number, row_data in enumerate(result):
			print(row_number)
			self.tableWidget_PTOU.insertRow(row_number)
			for column_number, data in enumerate(row_data):
				self.tableWidget_PTOU.setItem(row_number, column_number, QTableWidgetItem(str(data)))

		mydb.commit()


	def Back_to_HP(self):
		if self.UserType == 'Owner':
			back = OwnerHP(self.uid)
		else:
			back = GeneralUserHP(self.uid)
		widget.addWidget(back)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Qualifier(self):
		qualifier = Qualifier_OU(self.UserType,self.uid)
		widget.addWidget(qualifier)
		widget.setCurrentIndex(widget.currentIndex()+1)
		




##################################  SCHEDULE TABLE ADMIN PAGE  ##################################################
class Schedule_A(QtWidgets.QMainWindow):
	def __init__(self,uid):
		super(Schedule_A,self).__init__()
		loadUi("Schedule_A.ui",self)
		self.uid = uid
		self.pushButton_back.clicked.connect(self.Home)
		self.pushButton_update.clicked.connect(self.Update)
		self.pushButton_st.setEnabled(False)
		self.pushButton_st.setVisible(False)
		self.pushButton_st.clicked.connect(self.SchTournament)

	########################Displaying Table##############################
		mydb = mysql.connector.connect(host="bzf2fyi4xvsv6xzguzrq-mysql.services.clever-cloud.com" ,user="uyag4sfjf0h8anbb", passwd="yn8qWQqO3pC6yHpWUhzq", database="bzf2fyi4xvsv6xzguzrq")
		mycurr = mydb.cursor()
		# mycurr.execute("SELECT Team_name,Matches,Won,Lost,Tied,Points FROM {}".format(team))
		mycurr.execute("SELECT Match_no,Match_Status,Team_1,Team_2 FROM schedule")

		result = mycurr.fetchall()
		self.tableWidget_scheduleA.setRowCount(0)
		for row_number, row_data in enumerate(result):
			# print(row_number)
			self.tableWidget_scheduleA.insertRow(row_number)
			for column_number, data in enumerate(row_data):
				self.tableWidget_scheduleA.setItem(row_number, column_number, QTableWidgetItem(str(data)))

		mydb.commit()
		#####################################################################

		self.tableWidget_scheduleA.cellClicked.connect(self.MatchDetails)



	def MatchDetails(self):
		try:
			rowCount = self.tableWidget_scheduleA.rowCount()
			for row in range(rowCount):
				if self.tableWidget_scheduleA.item(row,0).isSelected():
					rowNum = row + 1
					print(rowNum)
		except:
			print("Please click on match number.")

		mycurr = mydb.cursor()
		query = ("SELECT Match_no,Team_1,Team_2,Match_Status,Schedule_id FROM schedule WHERE Match_no = %s")
		mycurr.execute(query,(rowNum,))
		result = mycurr.fetchone()
		MatchDetail = []
		R = 0
		for col in result:
			MatchDetail.append(result[R])
			R = R + 1
		print(MatchDetail)
		Match = MatchDetail[0]
		Team1 = MatchDetail[1]
		Team2 = MatchDetail[2]
		MS = MatchDetail[3]
		Sid = MatchDetail[4]

		md = MatchDetails_A(self.uid,Match,Team1,Team2,MS,Sid)
		widget.addWidget(md)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Home(self):
		backbutton = AdminHP(self.uid)
		widget.addWidget(backbutton)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Update(self):
		mycurr = mydb.cursor()
		rowCount = self.tableWidget_scheduleA.rowCount()
		print(rowCount)
		columnCount = self.tableWidget_scheduleA.columnCount()
		print(columnCount)
		for row in range(rowCount):
			rowNum = row + 1
			rowData = []
			for column in range(columnCount):
				widgetItem = self.tableWidget_scheduleA.item(row,column)
				if(widgetItem and widgetItem.text()):
					rowData.append(widgetItem.text())
				else:
					rowData.append('NULL')
			rowData.append(rowNum)
			print(rowData)
			# query = "INSERT INTO team (Team, Owner, Captian, Coach, Home_Ground) VALUES(%s, %s, %s, %s, %s)"
			query = "UPDATE schedule SET Match_no = %s, Day = %s, Date = %s, Time = %s, Venue = %s, Team_1 = %s, Team_2 = %s WHERE Match_no = %s"
			mycurr.execute(query, rowData)
		mydb.commit()

		msg = QMessageBox()
		msg.setWindowTitle("Success!")
		msg.setText("Schedule Table Updated Successfully!")
		msg.setIcon(QMessageBox.Information)
		msg.setStandardButtons(QMessageBox.Ok)
		x = msg.exec_()

	def SchTournament(self):
		# back_to_main = MainClass()
		# widget.addWidget(back_to_main)
		# widget.setCurrentIndex(widget.currentIndex()+1)

		mydb = mysql.connector.connect(host="bzf2fyi4xvsv6xzguzrq-mysql.services.clever-cloud.com" ,user="uyag4sfjf0h8anbb", passwd="yn8qWQqO3pC6yHpWUhzq", database="bzf2fyi4xvsv6xzguzrq")
		mycurr = mydb.cursor()

		team_1 = 'MI'
		team_2 = 'CSK'
		team_3 = 'RCB'
		team_4 = 'DC'
		team_5 = 'SRH'
		team_6 = 'PBKS'
		team_7 = 'RR'
		team_8 = 'KKR'
		time = '7:30 pm IST'
		# Date = '2021-04-09'

		TeamName = {team_1,team_2,team_3,team_4,team_5,team_6,team_7,team_8}
		Teamlist = list(TeamName)
		# Teamlist = [team_1,team_2,team_3,team_4,team_5,team_6,team_7,team_8]

		# NoOfTeams = len(Teamlist)
		NoOfTeams = 8
		# rowCount = (NoOfTeams)*(NoOfTeams - 1)/2
		# columnCount = self.tableWidget_scheduleA.columnCount()
			# print(columnCount)


		for row in range(NoOfTeams - 1):
			# rowNum = row + 1
			# rowData = []
			for column in range(row + 1, NoOfTeams):
				query = "INSERT INTO schedule (Time, Team_1, Team_2) VALUES (%s, %s, %s)"
				data = (time, Teamlist[row],Teamlist[column])
			# query = "UPDATE team SET Team = %s, Owner = %s, Captian = %s, Coach = %s, Home_Ground = %s WHERE Team_ID = %s"
				mycurr.execute(query, data)
		mydb.commit()

		msg = QMessageBox()
		msg.setWindowTitle("Success!")
		msg.setText("Tournament Scheduled Successfully!")
		msg.setIcon(QMessageBox.Information)
		msg.setStandardButtons(QMessageBox.Ok)
		x = msg.exec_()

		updatepage = Schedule_A(self.uid)
		widget.addWidget(updatepage)
		widget.setCurrentIndex(widget.currentIndex()+1)


###################################### SCHEDULE TABLE OWNER/GEN.USER PAGE  ############################################
class Schedule_OU(QtWidgets.QMainWindow):
	def __init__(self, s, uid):
		super(Schedule_OU,self).__init__()
		loadUi("Schedule_OU.ui",self)
		self.UserType = s
		self.uid = uid
		self.pushButton_back.clicked.connect(self.Back_to_HP)

	########################Displaying Table##############################
		mydb = mysql.connector.connect(host="bzf2fyi4xvsv6xzguzrq-mysql.services.clever-cloud.com" ,user="uyag4sfjf0h8anbb", passwd="yn8qWQqO3pC6yHpWUhzq", database="bzf2fyi4xvsv6xzguzrq")
		mycurr = mydb.cursor()
		# mycurr.execute("SELECT Team_name,Matches,Won,Lost,Tied,Points FROM {}".format(team))
		mycurr.execute("SELECT Match_no,Match_Status,Team_1,Team_2 FROM schedule")

		result = mycurr.fetchall()
		self.tableWidget_scheduleOU.setRowCount(0)
		for row_number, row_data in enumerate(result):
			# print(row_number)
			self.tableWidget_scheduleOU.insertRow(row_number)
			for column_number, data in enumerate(row_data):
				self.tableWidget_scheduleOU.setItem(row_number, column_number, QTableWidgetItem(str(data)))

		mydb.commit()
		#####################################################################

		self.tableWidget_scheduleOU.cellClicked.connect(self.MatchDetails)

	def MatchDetails(self):
		try:
			rowCount = self.tableWidget_scheduleOU.rowCount()
			for row in range(rowCount):
				if self.tableWidget_scheduleOU.item(row,0).isSelected():
					rowNum = row + 1
					print(rowNum)
		except:
			print("Please click on match number.")

		mycurr = mydb.cursor()
		query = ("SELECT Match_no,Team_1,Team_2,Match_Status,Schedule_id FROM schedule WHERE Match_no = %s")
		mycurr.execute(query,(rowNum,))
		result = mycurr.fetchone()
		MatchDetail = []
		R = 0
		print(rowNum)
		for col in result:
			MatchDetail.append(result[R])
			R = R + 1
		print(MatchDetail)
		Match = MatchDetail[0]
		Team1 = MatchDetail[1]
		Team2 = MatchDetail[2]
		MS = MatchDetail[3]
		Sid = MatchDetail[4]

		md = MatchDetails_OU(self.UserType,self.uid,Match,Team1,Team2,MS,Sid)
		widget.addWidget(md)
		widget.setCurrentIndex(widget.currentIndex()+1)

	

	def Back_to_HP(self):
		if self.UserType == 'Owner':
			back = OwnerHP(self.uid)
		else:
			back = GeneralUserHP(self.uid)
		widget.addWidget(back)
		widget.setCurrentIndex(widget.currentIndex()+1)


######################### MATCHDETAILS ADMIN #################################
class MatchDetails_A(QtWidgets.QMainWindow):
	def __init__(self,uid, Match, Team1, Team2, MS, Sid):
		super(MatchDetails_A,self).__init__()
		loadUi("MatchDetails_A.ui",self)
		self.uid = uid
		self.Match = Match
		self.Team1 = Team1
		self.Team2 = Team2
		self.MS = MS
		self.Sid = Sid


		self.pushButton_save.setVisible(False)
		self.lineEdit.setVisible(False)
		self.radioButton_team1.setVisible(False)
		self.radioButton_team2.setVisible(False)
		self.frame_bg.setVisible(False)


		# self.MatchDetail = MatchDetail
		self.radioButton_team1.setText(self.Team1)
		self.radioButton_team2.setText(self.Team2)

		self.pushButton_back.clicked.connect(self.Back)
		self.pushButton_update.clicked.connect(self.Update)
		self.pushButton_eodp.clicked.connect(self.EODP)
		self.pushButton_save.clicked.connect(self.UPDATE_PT)

		self.pushButton_team1.setText(self.Team1)
		self.pushButton_team2.setText(self.Team2)
		# print(MatchDetails)
		# T1 = self.MatchDetail[1]
		# T2 = self.MatchDetail[2]




		if self.MS == 'Pending':
			### Table 1
			mycurr = mydb.cursor()
				# mycurr.execute("SELECT Team,Owner,Captian,Coach,Home_Ground FROM {}".format(team))
			query1 = ("SELECT Player_id,Name FROM currentplayers where Team = %s")
			# values = (self.Team1)
			mycurr.execute(query1,(self.Team1, )) 

			result = mycurr.fetchall()
			self.tableWidget_team1.setRowCount(0)
			for row_number, row_data in enumerate(result):
				print(row_number)
				self.tableWidget_team1.insertRow(row_number)
				for column_number, data in enumerate(row_data):
						self.tableWidget_team1.setItem(row_number, column_number, QTableWidgetItem(str(data)))

			mydb.commit() 

			### Table 2
			mycurr = mydb.cursor()
				# mycurr.execute("SELECT Team,Owner,Captian,Coach,Home_Ground FROM {}".format(team))
			query2 = ("SELECT Player_id,Name FROM currentplayers where Team = %s")
			mycurr.execute(query2, (self.Team2, ))

			result = mycurr.fetchall()
			self.tableWidget_team2.setRowCount(0)
			for row_number, row_data in enumerate(result):
				print(row_number)
				self.tableWidget_team2.insertRow(row_number)
				for column_number, data in enumerate(row_data):
						self.tableWidget_team2.setItem(row_number, column_number, QTableWidgetItem(str(data)))
			mydb.commit()
		elif self.MS == 'Played':
			self.pushButton_update.setVisible(False)
			self.pushButton_eodp.setVisible(False)
			self.pushButton_save.setVisible(False)
			self.lineEdit.setVisible(False)
			self.radioButton_team1.setVisible(False)
			self.radioButton_team2.setVisible(False)
			self.frame_bg.setVisible(False)

			### Table 1
			mycurr = mydb.cursor()
				# mycurr.execute("SELECT Team,Owner,Captian,Coach,Home_Ground FROM {}".format(team))
			query1 = ("SELECT Player_id,Name,Runs,Wickets FROM matchrecords where Team = %s AND Match_id = %s AND Shedule_id = %s")
			mycurr.execute(query1, (self.Team1,self.Match,self.Sid, ))

			result = mycurr.fetchall()
			self.tableWidget_team1.setRowCount(0)
			for row_number, row_data in enumerate(result):
				print(row_number)
				self.tableWidget_team1.insertRow(row_number)
				for column_number, data in enumerate(row_data):
						self.tableWidget_team1.setItem(row_number, column_number, QTableWidgetItem(str(data)))
			mydb.commit()

			### Table 2
			mycurr = mydb.cursor()
				# mycurr.execute("SELECT Team,Owner,Captian,Coach,Home_Ground FROM {}".format(team))
			query2 = ("SELECT Player_id,Name,Runs,Wickets FROM matchrecords where Team = %s AND Match_id = %s AND Shedule_id = %s")
			mycurr.execute(query2, (self.Team2,self.Match,self.Sid, ))

			result = mycurr.fetchall()
			self.tableWidget_team2.setRowCount(0)
			for row_number, row_data in enumerate(result):
				print(row_number)
				self.tableWidget_team2.insertRow(row_number)
				for column_number, data in enumerate(row_data):
						self.tableWidget_team2.setItem(row_number, column_number, QTableWidgetItem(str(data)))
			mydb.commit()	

	def Update(self):	
		#### UPDATE TABLE --->  currentplayers Team1	
		mycurr = mydb.cursor()
		rowCount = self.tableWidget_team1.rowCount()
		print(rowCount)
		columnCount = self.tableWidget_team1.columnCount()
		print(columnCount)
		for row in range(rowCount):
			rowNum = row + 1
			rowData = []
			for column in range(columnCount):
				widgetItem = self.tableWidget_team1.item(row,column)
				if(widgetItem and widgetItem.text()):
					rowData.append(widgetItem.text())
				else:
					rowData.append('NULL')
			rowData.append(self.Team1)		
			# rowData.append(rowNum)
			PID = rowData[0]
			rowData.append(PID)
			print(rowData)
			# query = "INSERT INTO team (Team, Owner, Captian, Coach, Home_Ground) VALUES(%s, %s, %s, %s, %s)"
			query = "UPDATE currentplayers SET Player_id = %s, Name = %s, Runs = %s, Wickets = %s WHERE Team = %s AND Player_id = %s"
			mycurr.execute(query, rowData)
		mydb.commit()

		#### UPDATE TABLE --->  currentplayers Team2	
		mycurr = mydb.cursor()
		rowCount = self.tableWidget_team2.rowCount()
		print(rowCount)
		columnCount = self.tableWidget_team2.columnCount()
		print(columnCount)
		for row in range(rowCount):
			rowNum = row + 1
			rowData = []
			for column in range(columnCount):
				widgetItem = self.tableWidget_team2.item(row,column)
				if(widgetItem and widgetItem.text()):
					rowData.append(widgetItem.text())
				else:
					rowData.append('NULL')
			rowData.append(self.Team2)		
			# rowData.append(rowNum)
			PID = rowData[0]
			rowData.append(PID)
			print(rowData)
			# query = "INSERT INTO team (Team, Owner, Captian, Coach, Home_Ground) VALUES(%s, %s, %s, %s, %s)"
			query = "UPDATE currentplayers SET Player_id = %s, Name = %s, Runs = %s, Wickets = %s WHERE Team = %s AND Player_id = %s"
			mycurr.execute(query, rowData)
		mydb.commit()


	def EODP(self):
		msg = QMessageBox()
		msg.setWindowTitle("Confirmation!")
		msg.setText("Are you sure to conclude the match?")
		msg.setIcon(QMessageBox.Question)
		msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		# msg.exec()
		returnValue = msg.exec()
		
		if returnValue == QMessageBox.Yes:
			print('YES clicked')
			self.pushButton_save.setVisible(True)
			self.lineEdit.setVisible(True)
			self.radioButton_team1.setVisible(True)
			self.radioButton_team2.setVisible(True)
			self.frame_bg.setVisible(True)

			#### INSERT TABLE --->  matchrecords Team1	
			mycurr = mydb.cursor()
			rowCount = self.tableWidget_team1.rowCount()
			print(rowCount)
			columnCount = self.tableWidget_team1.columnCount()
			print(columnCount)
			for row in range(rowCount):
				rowNum = row + 1
				rowData = []
				for column in range(columnCount):
					widgetItem = self.tableWidget_team1.item(row,column)
					if(widgetItem and widgetItem.text()):
						rowData.append(widgetItem.text())
					else:
						rowData.append('NULL')
				rowData.append('2021')
				rowData.append(self.Match)
				rowData.append(self.Team1)		
				
				print(rowData)
				query = "INSERT INTO matchrecords (Player_id, Name, Runs, Wickets,Shedule_id, Match_id, Team) VALUES(%s, %s, %s, %s, %s, %s, %s)"
				# query = "UPDATE currentplayers SET Players = %s, Runs = %s, Wickets = %s WHERE Team_ID = %s AND Player_id = %s"
				mycurr.execute(query, rowData)
			mydb.commit()

			# mycurr = mydb.cursor()
			# # query = "INSERT INTO matchrecords (Player_id, Name, Runs, Wickets,Shedule_id, Match_id, Team) VALUES(%s, %s, %s, %s, %s, %s, %s)"
			# query = "UPDATE schedule SET Match_Status = %s WHERE Team_1 = %s AND Schedule_id = %s"
			# # values = ('Played',self.Team1,self.Sid)
			# mycurr.execute(query, ('Played',self.Team1,self.Sid, ))
			# mydb.commit()


			#### INSERT TABLE --->  matchrecords Team2	
			mycurr = mydb.cursor()
			rowCount = self.tableWidget_team2.rowCount()
			print(rowCount)
			columnCount = self.tableWidget_team2.columnCount()
			print(columnCount)
			for row in range(rowCount):
				rowNum = row + 1
				rowData = []
				for column in range(columnCount):
					widgetItem = self.tableWidget_team2.item(row,column)
					if(widgetItem and widgetItem.text()):
						rowData.append(widgetItem.text())
					else:
						rowData.append('NULL')
				rowData.append('2021')
				rowData.append(self.Match)
				rowData.append(self.Team2)		
				
				print(rowData)
				query = "INSERT INTO matchrecords (Player_id, Name, Runs, Wickets,Shedule_id, Match_id, Team) VALUES(%s, %s, %s, %s, %s, %s, %s)"
				# query = "UPDATE currentplayers SET Players = %s, Runs = %s, Wickets = %s WHERE Team_ID = %s AND Player_id = %s"
				mycurr.execute(query, rowData)
			mydb.commit()


			mycurr = mydb.cursor()
			# query = "INSERT INTO matchrecords (Player_id, Name, Runs, Wickets,Shedule_id, Match_id, Team) VALUES(%s, %s, %s, %s, %s, %s, %s)"
			query = "UPDATE schedule SET Match_Status = %s WHERE Match_no = %s AND Schedule_id = %s"
			# values = ('Played',self.MS,self.Sid)
			mycurr.execute(query, ('Played',self.Match,self.Sid, ))
			mydb.commit()

		else:
			print("No clicked")
			pass


	def UPDATE_PT(self):
		
		### Team 1 PointsTable
		mycurr = mydb.cursor()
			# mycurr.execute("SELECT Team,Owner,Captian,Coach,Home_Ground FROM {}".format(team))
		query1 = ("SELECT Team_ID,Sch_ID,Team_name,Matches,Won,Lost,Points FROM pointstable where Team_name = %s AND Sch_id = %s")
		mycurr.execute(query1, (self.Team1,self.Sid, ))

		result = mycurr.fetchone()
		Points = []
		R = 0
		for col in result:
			Points.append(result[R])
			R = R + 1
		print(Points)

		Team1 = Points[2]
		Matches1 = Points[3]
		Won1 = Points[4]
		Lost1 = Points[5]
		Points1 = Points[6]
		
		mydb.commit()	

		### Team 2 PointsTable
		mycurr = mydb.cursor()
			# mycurr.execute("SELECT Team,Owner,Captian,Coach,Home_Ground FROM {}".format(team))
		query1 = ("SELECT Team_ID,Sch_ID,Team_name,Matches,Won,Lost,Points FROM pointstable where Team_name = %s AND Sch_id = %s")
		mycurr.execute(query1, (self.Team2,self.Sid, ))

		result = mycurr.fetchone()
		Points = []
		R = 0
		for col in result:
			Points.append(result[R])
			R = R + 1
		print(Points)

		Team2 = Points[2]
		Matches2 = Points[3]
		Won2 = Points[4]
		Lost2 = Points[5]
		Points2 = Points[6]
		
		mydb.commit()

		# try:
		if self.radioButton_team1.isChecked():
			Won1 += 1
			Points1 += 2
			Matches1 += 1
			Matches2 += 1
			Lost2 += 1
			
			mycurr = mydb.cursor()
			# mycurr.execute("SELECT Team,Owner,Captian,Coach,Home_Ground FROM {}".format(team))
			query1 = ("UPDATE pointstable SET Matches = %s ,Won = %s,Points = %s where Team_name = %s AND Sch_id = %s")
			mycurr.execute(query1, (Matches1,Won1, Points1,self.Team1,self.Sid,))

			query2 = ("UPDATE pointstable SET Matches = %s ,Lost = %s where Team_name = %s AND Sch_id = %s")
			mycurr.execute(query2, (Matches2, Lost2,self.Team2,self.Sid,))
			mydb.commit()

			msg = QMessageBox()
			msg.setWindowTitle("Success!")
			msg.setText("Thank you! Match has been concluded for the day.\nPoints Table Updated!")
			msg.setIcon(QMessageBox.Information)
			msg.setStandardButtons(QMessageBox.Ok)
			x = msg.exec_()


		elif self.radioButton_team2.isChecked():
			Won2 += 1
			Points2 += 2
			Matches1 += 1
			Matches2 += 1
			Lost1 += 1

			mycurr = mydb.cursor()
			# mycurr.execute("SELECT Team,Owner,Captian,Coach,Home_Ground FROM {}".format(team))
			query3 = ("UPDATE pointstable SET Matches = %s ,Won = %s,Points = %s where Team_name = %s AND Sch_id = %s")
			mycurr.execute(query3, (Matches2,Won2, Points2,self.Team2,self.Sid,))

			query4 = ("UPDATE pointstable SET Matches = %s ,Lost = %s where Team_name = %s AND Sch_id = %s")
			mycurr.execute(query4, (Matches1, Lost1,self.Team1,self.Sid,))
			mydb.commit()

			msg = QMessageBox()
			msg.setWindowTitle("Success!")
			msg.setText("Thank you! Match has been concluded for the day.\nPoints Table Updated!")
			msg.setIcon(QMessageBox.Information)
			msg.setStandardButtons(QMessageBox.Ok)
			x = msg.exec_()

		else:
			msg = QMessageBox()
			msg.setWindowTitle("Warning!")
			msg.setText("Please select the Winner Team!")
			msg.setIcon(QMessageBox.Warning)
			msg.setStandardButtons(QMessageBox.Ok)
			x = msg.exec_()


		# except:

		# print(Won1)
		# print(Points1)
		# print(Matches1)
		# print(Matches2)
		# print(Lost2)

		# print(Won2)
		# print(Points2)
		# print(Matches1)
		# print(Matches2)
		# print(Lost1)



	def Back(self):	
		Back = Schedule_A(self.uid)
		widget.addWidget(Back)
		widget.setCurrentIndex(widget.currentIndex()+1)
		

##################################  MATCH DETAILS OWNER/GENERALUSER PAGE  ##################################################
class MatchDetails_OU(QtWidgets.QMainWindow):
	def __init__(self,UT,uid, Match, Team1, Team2, MS, Sid):
		super(MatchDetails_OU,self).__init__()
		loadUi("MatchDetails_OU.ui",self)
		self.UserType = UT
		self.uid = uid
		self.Match = Match
		self.Team1 = Team1
		self.Team2 = Team2
		self.MS = MS
		self.Sid = Sid
		# self.MatchDetail = MatchDetail
		self.pushButton_back.clicked.connect(self.Back)
		# self.pushButton_update.clicked.connect(self.Update)
		# self.pushButton_eodp.clicked.connect(self.EODP)

		self.pushButton_team1.setText(self.Team1)
		self.pushButton_team2.setText(self.Team2)
		# print(MatchDetails)
		# T1 = self.MatchDetail[1]
		# T2 = self.MatchDetail[2]


		if self.MS == 'Pending':
			### Table 1
			mycurr = mydb.cursor()
				# mycurr.execute("SELECT Team,Owner,Captian,Coach,Home_Ground FROM {}".format(team))
			query1 = ("SELECT Name FROM currentplayers where Team = %s")
			# values = (self.Team1)
			mycurr.execute(query1,(self.Team1, )) 

			result = mycurr.fetchall()
			self.tableWidget_team1.setRowCount(0)
			for row_number, row_data in enumerate(result):
				print(row_number)
				self.tableWidget_team1.insertRow(row_number)
				for column_number, data in enumerate(row_data):
						self.tableWidget_team1.setItem(row_number, column_number, QTableWidgetItem(str(data)))

			mydb.commit() 

			### Table 2
			mycurr = mydb.cursor()
				# mycurr.execute("SELECT Team,Owner,Captian,Coach,Home_Ground FROM {}".format(team))
			query2 = ("SELECT Name FROM currentplayers where Team = %s")
			mycurr.execute(query2, (self.Team2, ))

			result = mycurr.fetchall()
			self.tableWidget_team2.setRowCount(0)
			for row_number, row_data in enumerate(result):
				print(row_number)
				self.tableWidget_team2.insertRow(row_number)
				for column_number, data in enumerate(row_data):
						self.tableWidget_team2.setItem(row_number, column_number, QTableWidgetItem(str(data)))
			mydb.commit()
		
		elif self.MS == 'Played':
			### Table 1
			mycurr = mydb.cursor()
				# mycurr.execute("SELECT Team,Owner,Captian,Coach,Home_Ground FROM {}".format(team))
			query1 = ("SELECT Name,Runs,Wickets FROM matchrecords where Team = %s AND Match_id = %s AND Shedule_id = %s")
			mycurr.execute(query1, (self.Team1,self.Match,self.Sid, ))

			result = mycurr.fetchall()
			self.tableWidget_team1.setRowCount(0)
			for row_number, row_data in enumerate(result):
				print(row_number)
				self.tableWidget_team1.insertRow(row_number)
				for column_number, data in enumerate(row_data):
						self.tableWidget_team1.setItem(row_number, column_number, QTableWidgetItem(str(data)))
			mydb.commit()

			### Table 2
			mycurr = mydb.cursor()
				# mycurr.execute("SELECT Team,Owner,Captian,Coach,Home_Ground FROM {}".format(team))
			query2 = ("SELECT Name,Runs,Wickets FROM matchrecords where Team = %s AND Match_id = %s AND Shedule_id = %s")
			mycurr.execute(query2, (self.Team2,self.Match,self.Sid, ))

			result = mycurr.fetchall()
			self.tableWidget_team2.setRowCount(0)
			for row_number, row_data in enumerate(result):
				print(row_number)
				self.tableWidget_team2.insertRow(row_number)
				for column_number, data in enumerate(row_data):
						self.tableWidget_team2.setItem(row_number, column_number, QTableWidgetItem(str(data)))
			mydb.commit()



	def Back(self):	
		back = Schedule_OU(self.UserType,self.uid)
		widget.addWidget(back)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Refresh(self):	
		refresh = MatchDetails_OU(self.uid)
		widget.addWidget(refresh)
		widget.setCurrentIndex(widget.currentIndex()+1)


##################################  QUALIFIER TABLE ADMIN PAGE  ##################################################
class Qualifier_A(QtWidgets.QMainWindow):
	def __init__(self,uid):
		super(Qualifier_A,self).__init__()
		loadUi("Qualifier_A.ui",self)
		self.uid = uid
		self.pushButton_back.clicked.connect(self.Home)
		self.pushButton_update.clicked.connect(self.Update)
		self.pushButton_final.clicked.connect(self.Final)

		mydb = mysql.connector.connect(host="bzf2fyi4xvsv6xzguzrq-mysql.services.clever-cloud.com" ,user="uyag4sfjf0h8anbb", passwd="yn8qWQqO3pC6yHpWUhzq", database="bzf2fyi4xvsv6xzguzrq")
		cursor = mydb.cursor()
		Teamname = []
		cursor.execute("Select Team_name from pointstable ORDER BY Points DESC LIMIT 4")
		result = cursor.fetchall()
		for row in result:
			Teamname.append(row[0])
		mydb.commit()

		self.pushButton_p1.setText(Teamname[0])
		self.pushButton_p2.setText(Teamname[1])
		self.pushButton_p3.setText(Teamname[2])
		self.pushButton_p4.setText(Teamname[3])


		
		mydb = mysql.connector.connect(host="bzf2fyi4xvsv6xzguzrq-mysql.services.clever-cloud.com" ,user="uyag4sfjf0h8anbb", passwd="yn8qWQqO3pC6yHpWUhzq", database="bzf2fyi4xvsv6xzguzrq")
		mycurr = mydb.cursor()
		Team = []	
		mycurr.execute("SELECT Qualifier1_Winner, Eliminator_Winner, Qualifier2_Team1,Qualifier2_Winner, Final_Winner FROM qualifier WHERE Schedule_ID = '2021'")
		result = mycurr.fetchone()

		RowNum = 0
		for row in result:
			Team.append(result[RowNum])
			RowNum = RowNum + 1
		mydb.commit()


		print(Team)
		self.pushButton_lq1.setText(Team[2])
		self.pushButton_we.setText(Team[1])
		self.pushButton_wq1.setText(Team[0])
		self.pushButton_wq2.setText(Team[3])
		self.pushButton_fw.setText(Team[4])
		
		mydb.commit()


		self.pushButton_p1.clicked.connect(self.Qualifier_1_B1)
		self.pushButton_p2.clicked.connect(self.Qualifier_1_B2)
		self.pushButton_p3.clicked.connect(self.Eliminator_B1)
		self.pushButton_p4.clicked.connect(self.Eliminator_B2)
		self.pushButton_lq1.clicked.connect(self.Qualifier_2_B1)
		self.pushButton_we.clicked.connect(self.Qualifier_2_B2)
		self.pushButton_wq1.clicked.connect(self.Final_B1)
		self.pushButton_wq2.clicked.connect(self.Final_B2)


		
		





	################ Winner of Qualifier-1 ######################
	def Qualifier_1_B1(self):
		self.pushButton_wq1.setText('')
		self.pushButton_lq1.setText('')
		if self.pushButton_p1.isChecked():
			winner_q1 = self.pushButton_p1.text()
			losser_q1 = self.pushButton_p2.text()
			self.pushButton_wq1.setText(winner_q1)
			self.pushButton_lq1.setText(losser_q1)

	def Qualifier_1_B2(self):
		self.pushButton_wq1.setText('')
		self.pushButton_lq1.setText('')
		if self.pushButton_p2.isChecked():
			winner_q1 = self.pushButton_p2.text()
			losser_q1 = self.pushButton_p1.text()
			self.pushButton_wq1.setText(winner_q1)
			self.pushButton_lq1.setText(losser_q1)
		

	################ Winner of Eliminator ######################
	def Eliminator_B1(self):
		self.pushButton_we.setText('')
		if self.pushButton_p3.isChecked():
			winner_eleminator = self.pushButton_p3.text()
			losser_eliminator = self.pushButton_p4.text()
			self.pushButton_we.setText(winner_eleminator)

	def Eliminator_B2(self):
		self.pushButton_we.setText('')
		if self.pushButton_p4.isChecked():
			winner_eliminator = self.pushButton_p4.text()
			losser_eliminator = self.pushButton_p3.text()
			self.pushButton_we.setText(winner_eliminator)
			# self.pushButton_lq1.setText(losser_q1)


	################ Winner of Qualifier-2 ######################
	def Qualifier_2_B1(self):
		# self.pushButton_wq2.setText('')
		if self.pushButton_lq1.isChecked():
			winner_q2 = self.pushButton_lq1.text()
			# losser_eliminator = self.pushButton_p4.text()
			self.pushButton_wq2.setText(winner_q2)

		
	def Qualifier_2_B2(self):
		# self.pushButton_wq2.setText('')
		if self.pushButton_we.isChecked():
			winner_q2 = self.pushButton_we.text()
			# losser_q1 = self.pushButton_p1.text()
			self.pushButton_wq2.setText(winner_q2)
			# self.pushButton_lq1.setText(losser_q1)


	################ Winner of FINAL ######################
	def Final_B1(self):
		self.pushButton_fw.setText('')
		if self.pushButton_wq1.isChecked():
			winner = self.pushButton_wq1.text()
			# losser_eliminator = self.pushButton_p4.text()
			self.pushButton_fw.setText(winner)

		
	def Final_B2(self):
		self.pushButton_fw.setText('')
		if self.pushButton_wq2.isChecked():
			winner = self.pushButton_wq2.text()
			# losser_q1 = self.pushButton_p1.text()
			self.pushButton_fw.setText(winner)
			# self.pushButton_lq1.setText(losser_q1)




	def Home(self):
		backbutton = PointsTable_A(self.uid)
		widget.addWidget(backbutton)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Update(self):
		

		Round = []

		####### Qualifier-1 #######
		place_1 = self.pushButton_p1.text()
		place_2 = self.pushButton_p2.text()
		winner_q1 = self.pushButton_wq1.text()

		Round.append(place_1)
		Round.append(place_2)
		Round.append(winner_q1)


		####### Eliminator #######
		place_3 = self.pushButton_p3.text()
		place_4 = self.pushButton_p4.text()
		winner_eliminator = self.pushButton_we.text()
		# Roound.append(place_3,place_4,winner_eliminator,'Eliminator')
		Round.append(place_3)
		Round.append(place_4)
		Round.append(winner_eliminator)

		
		####### Qualifier-2 #######
		losser_q1 = self.pushButton_lq1.text()
		winner_eliminator = self.pushButton_we.text()
		winner_q2 = self.pushButton_wq2.text()
		# Round.append(losser_q1,winner_eliminator,winner_q2,'Qualifier_2')
		Round.append(losser_q1)
		Round.append(winner_eliminator)
		Round.append(winner_q2)
	

		####### Final #######
		winner_q1 = self.pushButton_wq1.text()
		winner_q2 = self.pushButton_wq2.text()
		final_winner = self.pushButton_fw.text()
		if final_winner == winner_q1:
			runnerup = winner_q2
		elif final_winner == winner_q2:
			runner_up = winner_q1
		# Round.append(winer_q1,winner_q2,final_winner,'Final')
		Round.append(winner_q1)
		Round.append(winner_q2)
		Round.append(final_winner)
		Round.append(runner_up)

		Schedule_id = '2021'
		Round.append(Schedule_id)
		print(Round)

		mydb = mysql.connector.connect(host="bzf2fyi4xvsv6xzguzrq-mysql.services.clever-cloud.com" ,user="uyag4sfjf0h8anbb", passwd="yn8qWQqO3pC6yHpWUhzq", database="bzf2fyi4xvsv6xzguzrq")
		mycurr = mydb.cursor()	
		
		for row in range(4):
			query = "UPDATE qualifier SET Qualifier1_Team1 = %s, Qualifier1_Team2 = %s, Qualifier1_Winner = %s, Eliminator_Team1 = %s, Eliminator_Team2 = %s, Eliminator_Winner = %s, Qualifier2_Team1 = %s, Qualifier2_Team2 = %s, Qualifier2_Winner = %s, Final_Team1 = %s, Final_Team2 = %s, Final_Winner = %s, Runner_Up = %s WHERE Schedule_ID = %s"
			mycurr.execute(query, Round)
		mydb.commit()


		# call_page_again = Qualifier_A()
		# widget.addWidget(call_page_again)
		# widget.setCurrentIndex(widget.currentIndex()+1)

		# print(losser_eliminator)
		msg = QMessageBox()
		msg.setWindowTitle("Success!")
		msg.setText("Qualifier Table Updated Successfully!")
		msg.setIcon(QMessageBox.Information)
		msg.setStandardButtons(QMessageBox.Ok)
		x = msg.exec_()

	def Final(self):
		final_button = Final_A(self.uid)
		widget.addWidget(final_button)
		widget.setCurrentIndex(widget.currentIndex()+1)



###################################### QUALIFIER TABLE OWNER/GEN.USER PAGE  ############################################
class Qualifier_OU(QtWidgets.QMainWindow):
	def __init__(self, s,uid):
		super(Qualifier_OU,self).__init__()
		loadUi("Qualifier_OU.ui",self)
		self.UserType = s
		self.uid = uid
		self.pushButton_back.clicked.connect(self.Back)
		self.pushButton_final.clicked.connect(self.Final)


		mydb = mysql.connector.connect(host="bzf2fyi4xvsv6xzguzrq-mysql.services.clever-cloud.com" ,user="uyag4sfjf0h8anbb", passwd="yn8qWQqO3pC6yHpWUhzq", database="bzf2fyi4xvsv6xzguzrq")
		mycurr = mydb.cursor()
		Team = []	
		mycurr.execute("SELECT Qualifier1_Team1,Qualifier1_Team2,Eliminator_Team1,Eliminator_Team2,Qualifier1_Winner, Eliminator_Winner, Qualifier2_Team1,Qualifier2_Winner, Final_Winner FROM qualifier WHERE Schedule_ID = '2021'")
		result = mycurr.fetchone()

		RowNum = 0
		for row in result:
			Team.append(result[RowNum])
			RowNum = RowNum + 1
		mydb.commit()


		print(Team)
		self.pushButton_p1.setText(Team[0])
		self.pushButton_p2.setText(Team[1])
		self.pushButton_p3.setText(Team[2])
		self.pushButton_p4.setText(Team[3])
		self.pushButton_lq1.setText(Team[6])
		self.pushButton_we.setText(Team[5])
		self.pushButton_wq1.setText(Team[4])
		self.pushButton_wq2.setText(Team[7])
		self.pushButton_fw.setText(Team[8])
		
		mydb.commit()



	def Back(self):
		back = PointsTable_OU(self.UserType,self.uid)
		widget.addWidget(back)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Final(self):
		back = Final_OU(self.UserType,self.uid)
		widget.addWidget(back)
		widget.setCurrentIndex(widget.currentIndex()+1)





##################################  FINAL PAGE ADMIN PAGE  ##################################################
class Final_A(QtWidgets.QMainWindow):
	def __init__(self, uid):
		super(Final_A,self).__init__()
		loadUi("Final_A.ui",self)
		self.uid = uid
		self.pushButton_back.clicked.connect(self.Home)
		self.pushButton_save.clicked.connect(self.Save)
		
		mydb = mysql.connector.connect(host="bzf2fyi4xvsv6xzguzrq-mysql.services.clever-cloud.com" ,user="uyag4sfjf0h8anbb", passwd="yn8qWQqO3pC6yHpWUhzq", database="bzf2fyi4xvsv6xzguzrq")
		cursor1 = mydb.cursor()
		cursor2 = mydb.cursor()
		cursor3 = mydb.cursor()

		cursor1.execute("SELECT Final_Winner, Runner_Up FROM qualifier WHERE Schedule_ID = '2021'")
		record = cursor1.fetchone()
		winner = record[0]
		runnerup = record[1]

		cursor2.execute("SELECT Name,sum(Runs) FROM matchrecords GROUP BY Name order by sum(Runs) Desc LIMIT 1")
		rec1 = cursor2.fetchone()
		ocap_name = rec1[0]
		ocap_runs = rec1[1]

		cursor3.execute("SELECT Name,sum(Wickets) FROM matchrecords GROUP BY Name order by sum(Wickets) Desc LIMIT 1")
		rec2 = cursor3.fetchone()
		pcap_name = rec2[0]
		pcap_runs = rec2[1]

		mydb.commit()

		self.lineEdit_winner.setText(winner)
		self.lineEdit_runnerup.setText(runnerup)
		self.lineEdit_pcap.setText(pcap_name)
		self.lineEdit_ocap.setText(ocap_name)

	def Home(self):
		backbutton = Qualifier_A(self.uid)
		widget.addWidget(backbutton)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Save(self):
		msg = QMessageBox()
		msg.setWindowTitle("Success!")
		msg.setText("A special thanks from our team for using our application for this years IPL!")
		# msg.setIcon(QMessageBox.Information)
		msg.setStandardButtons(QMessageBox.Ok)
		x = msg.exec_()

		Home_Page = AdminHP(self.uid)
		widget.addWidget(Home_Page)
		widget.setCurrentIndex(widget.currentIndex()+1)



###################################### FINAL PAGE OWNER/GEN.USER PAGE  ############################################
class Final_OU(QtWidgets.QMainWindow):
	def __init__(self, s, uid):
		super(Final_OU,self).__init__()
		loadUi("Final_OU.ui",self)
		self.UserType = s
		self.uid = uid
		self.pushButton_back.clicked.connect(self.Back)
		self.pushButton_home.clicked.connect(self.Home_Page)

		mydb = mysql.connector.connect(host="bzf2fyi4xvsv6xzguzrq-mysql.services.clever-cloud.com" ,user="uyag4sfjf0h8anbb", passwd="yn8qWQqO3pC6yHpWUhzq", database="bzf2fyi4xvsv6xzguzrq")
		cursor1 = mydb.cursor()
		cursor2 = mydb.cursor()
		cursor3 = mydb.cursor()

		cursor1.execute("SELECT Final_Winner, Runner_Up FROM qualifier WHERE Schedule_ID = '2021'")
		record = cursor1.fetchone()
		winner = record[0]
		runnerup = record[1]

		cursor2.execute("SELECT Name,sum(Runs) FROM matchrecords GROUP BY Name order by sum(Runs) Desc LIMIT 1")
		rec1 = cursor2.fetchone()
		ocap_name = rec1[0]
		ocap_runs = rec1[1]

		cursor3.execute("SELECT Name,sum(Wickets) FROM matchrecords GROUP BY Name order by sum(Wickets) Desc LIMIT 1")
		rec2 = cursor3.fetchone()
		pcap_name = rec2[0]
		pcap_runs = rec2[1]

		mydb.commit()

		self.lineEdit_winner.setText(winner)
		self.lineEdit_runnerup.setText(runnerup)
		self.lineEdit_pcap.setText(pcap_name)
		self.lineEdit_ocap.setText(ocap_name)



	def Back(self):
		backbutton = Qualifier_OU(self.UserType,self.uid)
		widget.addWidget(backbutton)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Home_Page(self):
		msg = QMessageBox()
		msg.setWindowTitle("Success!")
		msg.setText("A special thanks from our team for using our application for this years IPL!")
		# msg.setIcon(QMessageBox.Information)
		msg.setStandardButtons(QMessageBox.Ok)
		x = msg.exec_()

		if self.UserType == 'Owner':
			back = OwnerHP(self.uid)
		else:
			back = GeneralUserHP(self.uid)
		widget.addWidget(back)
		widget.setCurrentIndex(widget.currentIndex()+1)


##################################  AUCTION ADMIN PAGE  ##################################################
class Auction_A(QtWidgets.QMainWindow):
	def __init__(self,uid):
		super(Auction_A,self).__init__()
		loadUi("Auction_A.ui",self)
		self.uid = uid
		self.pushButton_back.clicked.connect(self.Back_to_HP)
		self.pushButton_dpd.clicked.connect(self.PlayersDetails)
		self.pushButton_update.clicked.connect(self.UPDATE)

		mydb = mysql.connector.connect(host="bzf2fyi4xvsv6xzguzrq-mysql.services.clever-cloud.com" ,user="uyag4sfjf0h8anbb", passwd="yn8qWQqO3pC6yHpWUhzq", database="bzf2fyi4xvsv6xzguzrq")
		mycurr = mydb.cursor()
		# mycurr.execute("SELECT Team,Owner,Captian,Coach,Home_Ground FROM {}".format(team))
		mycurr.execute("SELECT Name,Team,Sold_For,Player_Status,DOB,Role,Batting_Style,Bowling_Style,Matches,Runs,Wickets,IPL_Debut FROM player")

		result = mycurr.fetchall()
		self.tableWidget_players.setRowCount(0)
		for row_number, row_data in enumerate(result):
			print(row_number)
			self.tableWidget_players.insertRow(row_number)
			for column_number, data in enumerate(row_data):
				self.tableWidget_players.setItem(row_number, column_number, QTableWidgetItem(str(data)))

		mydb.commit()

	def PlayersDetails(self):
		rowCount = self.tableWidget_players.rowCount()
		for row in range(rowCount):
			if self.tableWidget_players.item(row,0).isSelected():
				rowNum = row + 1
				print(rowNum)

		mycurr = mydb.cursor()
		query = ("SELECT Name,Team,Sold_For FROM player WHERE Player_id = %s")
		mycurr.execute(query,(rowNum,))
		result = mycurr.fetchone()
		PlayerBid = []
		R = 0
		for col in result:
			PlayerBid.append(result[R])
			R = R + 1

		self.lineEdit_pname.setText(PlayerBid[0])
		self.lineEdit_cbid.setText(PlayerBid[2])
		self.lineEdit_team.setText(PlayerBid[1])
		mydb.commit()
		# print(Data)

		mycurr = mydb.cursor()
		# mycurr.execute("SELECT Team,Owner,Captian,Coach,Home_Ground FROM {}".format(team))
		query = ("SELECT Player_id,Shedule_id,Name,Team,DOB,Nationality,Role,Batting_Style,Bowling_Style,Matches,Runs,Wickets,IPL_Debut FROM player WHERE Player_id = %s")
		mycurr.execute(query,(rowNum,))
		result = mycurr.fetchone()
		Data = []
		R = 0
		for row in result:
			Data.append(result[R])
			R = R + 1

		mydb.commit()
		print(Data)

		mycurr = mydb.cursor()
		# columnCount = self.tableWidget_player.columnCount()
		query = "UPDATE playerowner SET Player_id = %s, Shedule_id = %s, Name = %s, Team = %s, DOB = %s, Nationality = %s, Role = %s, Batting_Style = %s, Bowling_Style = %s, Matches = %s, Runs =  %s, Wickets = %s, IPL_Debut = %s WHERE Shedule_id = '2021'"
		mycurr.execute(query, Data)
		mydb.commit()
		print("Success!")

	# def Sell_to_KKR(self):
	# 	msg = QMessageBox()
	# 	msg.setWindowTitle("Alert!")
	# 	msg.setText("Are you sure?")
	# 	msg.setIcon(QMessageBox.Information)
	# 	msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Yes)
	# 	x = msg.exec_()


	def UPDATE(self):
		rowNum = 1
		rowCount = self.tableWidget_players.rowCount()
		for row in range(rowCount):
			if self.tableWidget_players.item(row,0).isSelected():
				rowNum = row + 1
				# print(rowNum)
		
		if bool(self.tableWidget_players.item(rowNum-1,1).isSelected()) == True:

			mycurr = mydb.cursor()
			query = ("SELECT Name,Team,Sold_For,Player_Status,Shedule_id,Team FROM player WHERE Player_id = %s")
			mycurr.execute(query,(rowNum,))
			result = mycurr.fetchone()
			Player = []
			R = 0
			for col in result:
				Player.append(result[R])
				R = R + 1
			print(Player)

			if bool(Player[1]) == True:
				if Player[3] == 'Unsold':
					mycurr = mydb.cursor()
					query = "UPDATE player SET Player_Status = 'Sold' WHERE Player_id = %s"
					mycurr.execute(query, (rowNum,))
					mydb.commit()

					msg = QMessageBox()
					msg.setWindowTitle("Confirmation!")
					msg.setText(f"{Player[0]} sold to {Player[1]} for ₹{Player[2]}.")
					msg.setIcon(QMessageBox.Information)
					msg.setStandardButtons(QMessageBox.Ok)
					r = None
					x = msg.exec_()

					mycurr = mydb.cursor()
					query = "INSERT INTO currentplayers (Shedule_id,Team,Player_id,Name,Runs,Wickets) VALUES(%s, %s, %s, %s, %s, %s)"
					values = (Player[4],Player[5],rowNum,Player[0],'0','0')
					mycurr.execute(query, values )
					mydb.commit()


				else:
					msg = QMessageBox()
					msg.setWindowTitle("Action can't performed!")
					msg.setText(f"{Player[0]} has already sold to {Player[1]}!")
					msg.setIcon(QMessageBox.Information)
					msg.setStandardButtons(QMessageBox.Ok)
					r = None
					x = msg.exec_()
			else:
				msg = QMessageBox()
				msg.setWindowTitle("Information!")
				msg.setText(f"{Player[0]} is still Unsold!")
				msg.setIcon(QMessageBox.Information)
				msg.setStandardButtons(QMessageBox.Ok)
				x = msg.exec_()
		else:
			msg = QMessageBox()
			msg.setWindowTitle("Information!")
			msg.setText(f"Please select a player to be sold!")
			msg.setIcon(QMessageBox.Information)
			msg.setStandardButtons(QMessageBox.Ok)
			x = msg.exec_()





		a = Auction_A(self.uid)
		widget.addWidget(a)
		widget.setCurrentIndex(widget.currentIndex()+1)	


	def Back_to_HP(self):
		back = AdminHP(self.uid)
		widget.addWidget(back)
		widget.setCurrentIndex(widget.currentIndex()+1)



##################################  AUCTION OWNER PAGE  ##################################################
class Auction_O(QtWidgets.QMainWindow):
	def __init__(self,uid):
		super(Auction_O,self).__init__()
		loadUi("Auction_O.ui",self)
		self.uid = uid
		self.pushButton_back.clicked.connect(self.Back)
		self.pushButton_placebid.clicked.connect(self.PlaceBid)
		self.pushButton_refresh.clicked.connect(self.Refresh)

		# self.pushButton_buy.clicked.connect(self.BUY)
		self.pushButton_teamname.setText(self.uid)
		# self.lineEdit_cbid.setText('0')

		mycurr = mydb.cursor()
		# mycurr.execute("SELECT Team,Owner,Captian,Coach,Home_Ground FROM {}".format(team))
		query = ("SELECT * FROM playerowner")
		mycurr.execute(query)
		result = mycurr.fetchone()
		Data = []
		R = 0
		for row in result:
			Data.append(result[R])
			R = R + 1

		mydb.commit()

		Value = str(Data[0])
		self.lineEdit_id.setText(Value)
		# self.lineEdit_name.setText(Data[1])
		self.lineEdit_name.setText(Data[2])		
		# self.lineEdit_id.setText(Data[3])
		self.lineEdit_dob.setText(Data[4])
		self.lineEdit_nat.setText(Data[5])
		self.lineEdit_role.setText(Data[6])
		self.lineEdit_batstyle.setText(Data[7])
		self.lineEdit_bowlstyle.setText(Data[8])
		self.lineEdit_matches.setText(Data[9])
		self.lineEdit_runs.setText(Data[10])
		self.lineEdit_wickets.setText(Data[11])
		self.lineEdit_ipldebut.setText(Data[12])

		pid = self.lineEdit_id.text()

		mycurr = mydb.cursor()
		query = "SELECT Team,Sold_For FROM player WHERE Player_id = %s"
		mycurr.execute(query, (pid,))
		result = mycurr.fetchone()
		PBid = []
		R = 0
		for row in result:
			PBid.append(result[R])
			R = R + 1

		mydb.commit()
		self.lineEdit_cbid.setText(PBid[1])
		
		team_max = PBid[0]
		print(PBid[0])
		team_name = self.pushButton_teamname.text()
		print(team_name)
		# if team_name == team_max:
		# 	self.pushButton_buy.setVisible(True)
		# else:
		# 	self.pushButton_buy.setVisible(False)


	# def BUY(self):
	# 	print("Player added to your team successfully!")


	def PlaceBid(self):
		pbid = self.lineEdit_pbid.text()
		cbid = self.lineEdit_cbid.text()
		team = self.uid
		pid = self.lineEdit_id.text()
		# try:
		# if pbid > cbid:
		self.lineEdit_cbid.setText(pbid)
		self.lineEdit_pbid.setText('')
		mycurr = mydb.cursor()
		query = "UPDATE player SET Sold_For = %s, Team = %s WHERE Player_id = %s"
		mycurr.execute(query, (pbid, team, pid))
		mydb.commit()
		# else:
		# 	msg = QMessageBox()
		# 	msg.setWindowTitle("Information")
		# 	msg.setText("Bid cannot placed!\nEntered amount is less than Current Bid")
		# 	msg.setIcon(QMessageBox.Warning)
		# 	msg.setStandardButtons(QMessageBox.Ok)
		# 	x = msg.exec_()
		# except:
		# 	print("Exception occured!")
			


		# bid = OwnerHP(self.uid)
		# widget.addWidget(bid)
		# widget.setCurrentIndex(widget.currentIndex()+1)


	def Back(self):
		back = OwnerHP(self.uid)
		widget.addWidget(back)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def Refresh(self):
		r = Auction_O(self.uid)
		widget.addWidget(r)
		widget.setCurrentIndex(widget.currentIndex()+1)




if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	mainwindow = MainClass()
	widget=QtWidgets.QStackedWidget()
	widget.addWidget(mainwindow)
	widget.setFixedWidth(870)
	widget.setFixedHeight(559)
	widget.show()
	app.exec_()
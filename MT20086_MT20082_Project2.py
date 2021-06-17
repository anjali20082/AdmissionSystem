import sqlite3

import time
import random
import getpass
import datetime

conn = sqlite3.connect('admission_database.db')
c = conn.cursor()


class Database_Interaction:

    def create_table(self):
        c.execute(
            'CREATE TABLE IF NOT EXISTS  fee_payment( student_id INTEGER REFERENCES candidates(candidateid) ON DELETE CASCADE UNIQUE NOT NULL, payment_status TEXT DEFAULT "...NP...", transaction_id INTEGER)')
        c.execute(
            'CREATE TABLE IF NOT EXISTS  results( resultid INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, candidateid INTEGER REFERENCES candidates(candidateid) ON DELETE CASCADE UNIQUE NOT NULL, selected INTEGER NOT NULL DEFAULT(0), score INTEGER NOT NULL)')
        c.execute(
            'CREATE TABLE IF NOT EXISTS admitted_students( student_id INTEGER REFERENCES candidates(candidateid) ON DELETE CASCADE UNIQUE NOT NULL, program_alloted TEXT, roll_no INTEGER UNIQUE)')
        c.execute(
            'CREATE TABLE IF NOT EXISTS vacancy_count(Seats_CSE INTEGER DEFAULT 5, Seats_ECE INTEGER DEFAULT 5, Seats_CB INTEGER DEFAULT 5)')

    def data_entries(self):
        # c.execute('INSERT INTO fee_payment VALUES( 2, "...confirmed..." , 456247)')
        # c.execute('INSERT INTO results VALUES( 103, 3, 1, 25)')
        # c.execute('INSERT INTO admitted_students VALUES( 2, "CSE", 1001)')
        c.execute('INSERT INTO vacancy_count VALUES( 5, 5, 5)')
        conn.commit()
        # c.close()
        # conn.close()

    def display_table(self):

        c.execute("SELECT * FROM candidates")
        rows1 = c.fetchall()
        for row1 in rows1:
            print(row1)
        conn.commit()
        c.execute("SELECT * FROM results")
        rows = c.fetchall()
        for row in rows:
            print(row)
        conn.commit()
        c.execute("SELECT * FROM fee_payment")
        rows2 = c.fetchall()
        for row2 in rows2:
            print(row2)
        conn.commit()
        c.execute("SELECT * FROM admitted_students")
        rows3 = c.fetchall()
        for row3 in rows3:
            print(row3)
        conn.commit()
        c.execute("SELECT * FROM vacancy_count")
        rows4 = c.fetchall()
        for row4 in rows4:
            print(row4)
        conn.commit()

    def drop_table(self):
        c.execute("DROP TABLE results")
        conn.commit()


class Fee_payment:
    def __init__(self):
        self.creditcard = None
        self.netbanking = None
        self.upi = None

    def enter_paymentdata(self, Studentid, paymentStatus, transactionId):
        student_id = Studentid
        payment_status = paymentStatus
        transaction_id = transactionId
        c.execute('INSERT INTO fee_payment( student_id, payment_status,transaction_id) VALUES (?, ?, ?)',
                  (student_id, payment_status, transaction_id))
        conn.commit()

    def pay_fees(self):

        self.creditcard = Credit_card()
        self.netbanking = Net_Banking()
        self.upi = UPI()
        print("============================= FEE PAYMENT PORTAL ==================================")
        Studentid = input(" Enter the Candidate ID : ")

        c.execute(
            " SELECT payment_status,student_id FROM fee_payment WHERE payment_status = 'confirmed'and student_id =?",
            (Studentid,))
        fee_status = c.fetchall()

        if not fee_status:
            print("Welcome to Payment Portal")
        elif fee_status[0][0] == "confirmed":
            print("Already Paid, go forward for program registration")
            return -1

        c.execute(" SELECT resultid FROM results WHERE selected = 1 and candidateid =?", (Studentid,))
        row = c.fetchall()

        if not row:
            print("Not selected, not eligible to pay")
            exit()

        else:
            Option = input(
                "Select a payment option :\n 1. Credit Card \n 2. Net Banking \n 3. UPI \n Enter numbers 1, 2 or 3\n")
            if Option == "1":
                self.creditcard.pay_creditcard(Studentid)

            elif Option == "2":
                self.netbanking.pay_netbanking(Studentid)

            elif Option == "3":
                self.upi.pay_UPI(Studentid)

            else:
                while (Option != "1" or Option != "2" or Option != "3"):
                    print("Enter correct options 1, 2 or 3")
                    Option = input(
                        "Select a payment option :\n 1. Credit Card \n 2. Net Banking \n 3. UPI \n Enter numbers 1, 2 or 3\n")
                if Option == "1":
                    self.creditcard.pay_creditcard(Studentid)

                elif Option == "2":
                    self.netbanking.pay_netbanking(Studentid)

                elif Option == "3":
                    self.upi.pay_UPI(Studentid)


class Credit_card:

    def __init__(self):
        self.payfee = None

    def pay_creditcard(self, Studentid):
        self.payfee = Fee_payment()
        card_number = input("Enter 12 digit card number : ")
        if (len(card_number) == 12):
            print("Proceed for payment\n" "Enter 4 digit OTP : \n")
            OTP = getpass.getpass(prompt='OTP: ')

            if len(OTP) == 4:
                print("Payment successful, receipt will be generated in a few seconds")
                time.sleep(2)
                transID = random.getrandbits(40)
                print(" Receipt : \n Transaction Id : ", transID, "\n Kindly save it for future reference")
                # insert record in table
                student_id = Studentid
                self.payfee.enter_paymentdata(student_id, "confirmed", transID)
            elif (len(OTP) != 4):
                while (len(OTP) != 4):
                    print("Wrong OTP, enter again")
                    OTP = getpass.getpass(prompt='OTP: ')
                print("Payment successful, receipt will be generated in a few seconds")
                time.sleep(2)
                transID = random.getrandbits(40)
                print(" Receipt : \n Transaction Id : ", transID, "\n Kindly save it for future reference")
                # insert record in table
                student_id = Studentid
                self.payfee.enter_paymentdata(student_id, "confirmed", transID)

        elif (len(card_number) != 12):
            while (len(card_number) != 12):
                print("enter correct number of digits  ")
                card_number = input("Enter 12 digit card number : ")
            print("Proceed for payment\n" "Enter 4 digit OTP : \n")
            OTP = getpass.getpass(prompt='OTP: ')

            if len(OTP) == 4:
                print("Payment successful, receipt will be generated in a few seconds")
                time.sleep(2)
                transID = random.getrandbits(40)
                print(" Receipt : \n Transaction Id : ", transID, "\n Kindly save it for future reference")
                # insert record in table
                student_id = Studentid
                self.payfee.enter_paymentdata(student_id, "confirmed", transID)
            elif (len(OTP) != 4):
                while (len(OTP) != 4):
                    print("Wrong OTP, enter again")
                    OTP = getpass.getpass(prompt='OTP: ')
                print("Payment successful, receipt will be generated in a few seconds")
                time.sleep(2)
                transID = random.getrandbits(40)
                print(" Receipt : \n Transaction Id : ", transID, "\n Kindly save it for future reference")
                # insert record in table
                student_id = Studentid
                self.payfee.enter_paymentdata(student_id, "confirmed", transID)


class Net_Banking:

    def __init__(self):
        self.payfee = None

    def pay_netbanking(self, Studentid):
        self.payfee = Fee_payment()
        cust_id = input("Enter 8 digit customerID : ")

        if (len(cust_id) == 8):
            print("Enter your password")
            password = getpass.getpass(prompt='Password: ')
            if (password == "12345"):
                print("Payment successful, receipt will be generated in a few seconds")
                time.sleep(2)
                transID = random.getrandbits(40)
                print(" Receipt : \n Transaction Id : ", transID, "\n Kindly save it for future reference")
                # insert record in table
                student_id = Studentid
                self.payfee.enter_paymentdata(student_id, "confirmed", transID)
            elif (password != "12345"):
                while (password != "12345"):
                    print("Wrong password, enter again")
                    password = getpass.getpass(prompt='Password: ')
                print("Payment successful, receipt will be generated in a few seconds")
                time.sleep(2)
                transID = random.getrandbits(40)
                print(" Receipt : \n Transaction Id : ", transID, "\n Kindly save it for future reference")
                # insert record in table
                student_id = Studentid

                self.payfee.enter_paymentdata(student_id, "confirmed", transID)


class UPI:
    def __init__(self):
        self.payfee = None

    def pay_UPI(self, Studentid):
        self.payfee = Fee_payment()
        UPI_Id = input(" Enter an alphanumeric 8 digit UPI ID")
        if (len(UPI_Id) == 8 and UPI_Id.isalnum()):
            print("Enter your 6 digit UPI PIN")
            password = getpass.getpass(prompt='Password: ')
            if (password == "123456"):
                print("Payment successful, receipt will be generated in a few seconds")
                time.sleep(2)
                transID = random.getrandbits(40)
                print(" Receipt : \n Transaction Id : ", transID, "\n Kindly save it for future reference")
                # insert record in table
                student_id = Studentid
                self.payfee.enter_paymentdata(student_id, "confirmed", transID)
            elif (password != "123456"):
                while (password != "123456"):
                    print("Wrong password, enter again")
                    password = getpass.getpass(prompt='Password: ')
                print("Payment successful, receipt will be generated in a few seconds")
                time.sleep(2)
                transID = random.getrandbits(40)
                print(" Receipt : \n Transaction Id : ", transID, "\n Kindly save it for future reference")
                # insert record in table
                student_id = Studentid

                self.payfee.enter_paymentdata(student_id, "confirmed", transID)


class Program_register:

    def __init__(self):
        self.admissionletter = None

    def enter_Allotmentdata(self, Studentid, seat_alloted, final_roll_no):
        student_id = Studentid
        program_alloted = seat_alloted
        roll_no = final_roll_no
        c.execute('INSERT INTO admitted_students( student_id, program_alloted,roll_no) VALUES (?, ?, ?)',
                  (student_id, program_alloted, roll_no))
        conn.commit()

    def generate_admission_letter(self):
        self.admissionletter = Admission_letter()

    def print_Admission_Letter(self):
        self.admissionletter.print_admission_letter()

    def register_for_program(self):

        print("============================= REGISTER FOR PROGRAM ==================================")

        Studentid = input(" Enter the Candidate ID : ")
        c.execute(" SELECT payment_status FROM fee_payment WHERE payment_status = 'confirmed'and student_id =?",
                  (Studentid,))
        row = c.fetchall()

        c.execute(" SELECT student_id FROM admitted_students WHERE student_id =?", (Studentid,))
        already_registered = c.fetchall()

        c.execute(" SELECT LAST_VALUE(Seats_CSE) OVER(ORDER by Seats_CSE desc) FROM vacancy_count")
        vacancy_CSE = c.fetchall()
        Seats_CSE = int(vacancy_CSE[0][0])

        c.execute(" SELECT LAST_VALUE(Seats_ECE) OVER(ORDER by Seats_ECE desc) FROM vacancy_count")
        vacancy_ESE = c.fetchall()
        Seats_ECE = int(vacancy_ESE[0][0])

        c.execute(" SELECT LAST_VALUE(Seats_CB) OVER(ORDER by Seats_CB desc) FROM vacancy_count")
        vacancy_CB = c.fetchall()
        Seats_CB = int(vacancy_CB[0][0])

        if not row:
            print("Fee not paid, you can register for programs only after fee payment")
            exit()

        elif already_registered:
            print("Already registered, nothing else required !")
            return -1
        else:

            seat_allotted = " "

            Option1 = input(
                "You get only two choices \n Fill choice number 1 \n Enter program choice number 1 from the listed choices\n 1. CSE \n 2. ECE \n 3. CB \nEnter the number corresponding to preferred choice : ")

            Option2 = input(
                "Fill choice number 2 \n Enter program choice number 2 from the listed choices\n 1. CSE \n 2. ECE \n 3. CB \nEnter the number corresponding to preferred choice, do not enter the one entered in choice number 1 : ")
            if (Option1 == Option2):
                Option2 = input("Fill a different choice  from choice number 1 \n   : ")

            print("The choices are recorded, once allotment is done you can view and download admission letter")

            if (Option1 == "1"):
                if (Seats_CSE != 0):
                    seat_allotted = "CSE"
                    Seats_CSE = Seats_CSE - 1
                    conn.execute("UPDATE vacancy_count set Seats_CSE = Seats_CSE - 1 ")
                    conn.commit()
                elif (Option2 == "2"):
                    if (Seats_ECE != 0):
                        seat_allotted = "ECE"
                        Seats_ECE = Seats_ECE - 1
                        conn.execute("UPDATE vacancy_count set Seats_ECE = Seats_ECE - 1 ")
                        conn.commit()
                elif (Option2 == "3"):
                    if (Seats_CB != 0):
                        seat_allotted = "CB"
                        Seats_CB = Seats_CB - 1
                        conn.execute("UPDATE vacancy_count set Seats_CB = Seats_CB - 1 ")
                        conn.commit()
            elif (Option1 == "2"):
                if (Seats_ECE != 0):
                    seat_allotted = "ECE"
                    Seats_ECE = Seats_ECE - 1
                    conn.execute("UPDATE vacancy_count set Seats_ECE = Seats_ECE - 1 ")
                    conn.commit()
                elif (Option2 == "1"):
                    if (Seats_CSE != 0):
                        seat_allotted = "CSE"
                        Seats_CSE = Seats_CSE - 1
                        conn.execute("UPDATE vacancy_count set Seats_CSE = Seats_CSE - 1 ")
                        conn.commit()
                elif (Option2 == "3"):
                    if (Seats_CB != 0):
                        seat_allotted = "CB"
                        Seats_CB = Seats_CB - 1
                        conn.execute("UPDATE vacancy_count set Seats_CB = Seats_CB - 1 ")
                        conn.commit()
            elif (Option1 == "3"):
                if (Seats_CB != 0):
                    seat_allotted = "CB"
                    Seats_CB = Seats_CB - 1
                    conn.execute("UPDATE vacancy_count set Seats_CB = Seats_CB - 1 ")
                    conn.commit()
                elif (Option2 == "1"):
                    if (Seats_CSE != 0):
                        seat_allotted = "CSE"
                        Seats_CSE = Seats_CSE - 1
                        conn.execute("UPDATE vacancy_count set Seats_CSE = Seats_CSE - 1 ")
                        conn.commit()
                elif (Option2 == "2"):
                    if (Seats_ECE != 0):
                        seat_allotted = "ECE"
                        Seats_ECE = Seats_ECE - 1
                        conn.execute("UPDATE vacancy_count set Seats_ECE = Seats_ECE - 1 ")
                        conn.commit()

            elif (seat_allotted == " "):
                if (Seats_CSE != 0):
                    seat_allotted = "CSE"
                    Seats_CSE = Seats_CSE - 1
                    conn.execute("UPDATE vacancy_count set Seats_CSE = Seats_CSE - 1 ")
                    conn.commit()
                elif (Seats_ECE != 0):
                    seat_allotted = "ECE"
                    Seats_ECE = Seats_ECE - 1
                    conn.execute("UPDATE vacancy_count set Seats_ECE = Seats_ECE - 1 ")
                    conn.commit()
                elif (Seats_CB != 0):
                    seat_allotted = "CB"
                    Seats_CB = Seats_CB - 1
                    conn.execute("UPDATE vacancy_count set Seats_CB = Seats_CB - 1 ")
                    conn.commit()

            c.execute(" SELECT LAST_VALUE(roll_no) OVER(ORDER by roll_no desc) FROM admitted_students")
            last_roll_no = c.fetchall()
            # final_roll_no = final_roll_no + 1
            if last_roll_no:
                new_roll_no = int(last_roll_no[0][0]) + 1
            else:
                new_roll_no = 1000
            self.enter_Allotmentdata(Studentid, seat_allotted, new_roll_no)


class Admission_letter:
    def print_admission_letter(self):
        print("=============================PRINT ADMISSION LETTER==================================")

        Studentid = input(" Enter the Candidate ID to download the admission letter : ")

        print("=============================ADMISSION LETTER==================================")

        c.execute(
            " SELECT admitted_students.program_alloted, admitted_students.roll_no, candidates.name, candidates.dob, candidates.fname, candidates.mname, candidates.gender, candidates.category, candidates.email, candidates.address  FROM admitted_students, candidates   WHERE candidates.candidateid=admitted_students.student_id and admitted_students.student_id =?",
            (Studentid,))
        row = c.fetchall()
        if not row:
            print(" You haven't registered for the program yet.")
            exit()
        else:
            admitted_data = row[0]
            admitted_data = list(admitted_data)

            print(" Program Alloted : ", admitted_data[0], " \n", " Roll Number : ", admitted_data[1], "\n Name : ",
                  admitted_data[2], "\n DOB : ", admitted_data[3], "\n Father's Name :", admitted_data[4],
                  "\n Mother's Name : ", admitted_data[5], "\n Gender : ", admitted_data[6], "\n Category : ",
                  admitted_data[7], "\n Email : ", admitted_data[8], "\n Address : ", admitted_data[9])
            print("============================================================================")
            print(" Download and save it for future reference")
            print("=============================END============================================")

        conn.commit()


class SelectionPortal:

    def __init__(self):
        self.vacantSeats = 15
        self.meritList = None
        self.shortList = None
        self.waitList = None
        self.selectionList = None

    def generateMeritList(self):
        try:
            sqliteConnection = sqlite3.connect("admission_database.db")
            cursor = sqliteConnection.cursor()

            sqlite_select_query = "SELECT T.candidateid, S.name, T.score FROM results AS T, candidates AS S WHERE T.candidateid = S.candidateid ORDER BY score DESC LIMIT 45"
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            self.meritList = records

            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

            return records

    def generateShortList(self):
        try:
            sqliteConnection = sqlite3.connect("admission_database.db")
            cursor = sqliteConnection.cursor()

            sqlite_select_query = "SELECT T.candidateid, S.name, T.score FROM results AS T, candidates AS S WHERE T.candidateid = S.candidateid ORDER BY score DESC LIMIT 23"
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            self.shortList = records

            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

            return records

    def generateWaitList(self):
        try:
            sqliteConnection = sqlite3.connect("admission_database.db")
            cursor = sqliteConnection.cursor()

            sqlite_select_query = "SELECT T.candidateid, S.name, T.final_score FROM results AS T, candidates AS S WHERE T.candidateid = S.candidateid AND waiting = 1 ORDER BY final_score DESC"
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            self.waitList = records

            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

            return records

    def generateSelectionList(self):
        try:
            sqliteConnection = sqlite3.connect("admission_database.db")
            cursor = sqliteConnection.cursor()

            sqlite_select_query = "SELECT T.candidateid, S.name, T.final_score FROM results AS T, candidates AS S WHERE T.candidateid = S.candidateid AND selected = 1 ORDER BY final_score DESC"
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            self.selectionList = records

            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

            return records

    def finalizeSelection(self):
        try:
            sqliteConnection = sqlite3.connect("admission_database.db")
            cursor = sqliteConnection.cursor()

            sqlite_select_query = "SELECT T.candidateid FROM results AS T, candidates AS S WHERE T.candidateid = S.candidateid ORDER BY final_score DESC LIMIT 23"
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()

            i = 0
            for row in records:
                if i <= 15:
                    sqlite_update_query = "UPDATE results SET selected=1 WHERE candidateid=" + str(row[0]) + ";"
                    cursor.execute(sqlite_update_query)
                else:
                    sqlite_update_query = "UPDATE results SET waiting=1 WHERE candidateid=" + str(row[0]) + ";"
                    cursor.execute(sqlite_update_query)

                i = i + 1

            sqliteConnection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

    def printMeritList(self):
        print("=========== MERIT LIST ================")
        print("REGISTRATION NO. - NAME - MARKS")
        records = self.generateMeritList()
        for row in records:
            print(str(row[0]) + " - " + str(row[1]) + " - " + str(row[2]))

    def printShortList(self):
        print("=========== SHORT LIST ================")
        print("REGISTRATION NO. - NAME - MARKS")
        records = self.generateShortList()
        for row in records:
            print(str(row[0]) + " - " + str(row[1]) + " - " + str(row[2]))

    def printWaitList(self):
        print("=========== WAIT LIST ================")
        print("REGISTRATION NO. - NAME - MARKS")
        records = self.generateWaitList()
        for row in records:
            print(str(row[0]) + " - " + str(row[1]) + " - " + str(row[2]))

    def printSelectionList(self):
        print("=========== SELECTION LIST ================")
        print("REGISTRATION NO. - NAME - MARKS")
        records = self.generateSelectionList()
        for row in records:
            print(str(row[0]) + " - " + str(row[1]) + " - " + str(row[2]))

    def getShortList(self):
        return self.shortList

    def storeFinalScores(self, interviewScores, finalScores):
        try:
            sqliteConnection = sqlite3.connect("admission_database.db")
            cursor = sqliteConnection.cursor()

            for candidateID, finalScore in finalScores.items():
                sqlite_update_query = "UPDATE results SET final_score=" + str(finalScore) + " WHERE candidateid=" + str(
                    candidateID) + ";"
                cursor.execute(sqlite_update_query)

            for candidateID, interviewScore in interviewScores.items():
                sqlite_update_query = "UPDATE results SET interview_score=" + str(
                    interviewScore) + " WHERE candidateid=" + str(candidateID) + ";"
                cursor.execute(sqlite_update_query)

            sqliteConnection.commit()
            cursor.close()

            self.finalizeSelection()

        except sqlite3.Error as error:
            print("Failed to update data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()


class AdmitCard:

    def __init__(self, candidateID, name, dob, fname, mname, programme):
        self.candidateID = candidateID
        self.name = name
        self.dob = dob
        self.fname = fname
        self.mname = mname
        self.programme = programme
        self.centerAddress = "iON Digital Zone iDZ Omaxe City SS Compuage, Omaxe Avenue Omaxe City, Bijnour Road, Near Baba Saheb, Bhimrao Ambedkar University, Lucknow, Uttar Pradesh Lucknow, Uttar Pradesh - 226025"
        self.instruction = [
            "1. A printed copy of this Admit Card must be presented for the verification along with at least one original (not photocopy or scanned copy) valid photo identification proof (For example: Passport, PAN Card, Voter ID, Aadhaar-UID, College ID, Employee ID, Driving License).",
            "2. The Admit Card is considered to be valid only if the photograph and signature are clear. To ensure this, print the admit card on an A4 sized paper using a laser printer, preferably a colour photo printer.",
            "3. Candidates will be permitted to appear for the examination ONLY after verification of their credentials by the centre officials."]

class QuestionPaper:

    def __init__(self):
        self.question_paper = {
            "UNIX: Which command is used to sort the lines of data in a file in reverse order.": "sort -r",
            "HARDWARE: From what location are the 1st computer instructions available on boot up.": "ROM BIOS",
            "AI: What is the term used for describing the judgemental or common sense part of problem solving?": "Heuristic",
            "AI: What was originally called the 'Imitation Game' by it's creator?": "The Turing Test",
            "Database: What is the full form of ER Diagram?": "Entity Relationship Diagram"}

        self.answer_sheet = []

class TestingPortal:

    def __init__(self):
        self.currentAdmitCard = None
        self.questionPaper = QuestionPaper()

    def generateAdmitCard(self, name, dob):
        if self.currentAdmitCard is None:
            records = self.fetchCandidateDetails(name, dob)
            if records is not None and len(records) == 1:
                self.currentAdmitCard = AdmitCard(records[0][0], name, dob, records[0][3], records[0][4], records[0][5])
                return self.currentAdmitCard
            else:
                print("=========== TESTING PORTAL ================")
                print("Couldn't find details, please fill application form first!")
                return None
        else:
            return self.currentAdmitCard

    def printAdmitCard(self):
        print("=========== ADMIT CARD FOR EXAMINATION ================")
        print("Date of Examination: 26/10/2020")
        print("Time of Examination: 14:30 to 17:30 Hrs")
        print("Registration Number: CS20S6502206" + str(self.currentAdmitCard.candidateID) + "")
        print("Name: " + self.currentAdmitCard.name)
        print("Date of Birth: " + self.currentAdmitCard.dob)
        print("Father name: " + self.currentAdmitCard.fname)
        print("Mother name: " + self.currentAdmitCard.mname)
        print("Examination for: " + self.currentAdmitCard.programme)
        print("Examination Centre: ")
        print(self.currentAdmitCard.centerAddress)
        print("\n")
        print("==== INSTRUCTIONS ====")
        print(self.currentAdmitCard.instruction[0])
        print(self.currentAdmitCard.instruction[1])
        print(self.currentAdmitCard.instruction[2])

    def fetchCandidateDetails(self, name, dob):
        try:
            sqliteConnection = sqlite3.connect("admission_database.db")
            cursor = sqliteConnection.cursor()

            sqlite_select_query = "SELECT candidateid, name, dob, fname, mname, programme FROM candidates WHERE name='" + name + "' AND dob='" + dob + "';"
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()

            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

            return records

    def conductTest(self):
        print("=========== ENTRANCE EXAMINATION ================")
        for question, v in self.questionPaper.question_paper.items():
            print(question)
            self.questionPaper.answer_sheet.append(input())

        self.evaluateTest()

    def evaluateTest(self):
        i = 0
        score = 0
        for k, answer in self.questionPaper.question_paper.items():
            if answer == self.questionPaper.answer_sheet[i]:
                score = score + 5
                i = i + 1

        self.storeCandidateScore(score)
        print("Final score: " + str(score) + "/25")

    def storeCandidateScore(self, score):
        try:
            sqliteConnection = sqlite3.connect("admission_database.db")
            cursor = sqliteConnection.cursor()

            sqlite_insert_query = "INSERT INTO results (candidateid, score) VALUES (" + str(
                self.currentAdmitCard.candidateID) + ", " + str(score) + ");"

            cursor.execute(sqlite_insert_query)
            sqliteConnection.commit()

            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()


class ApplicationForm:

    def __init__(self):
        self.fields_personal = {"Your full name: ": "name",
                                "Date of Birth: ": "dob",
                                "Father's name: ": "fname",
                                "Mother's name: ": "mname",
                                "Gender: ": "gender",
                                "Category: ": "category",
                                "Email: ": "email",
                                "Mobile Number: ": "mobile",
                                "Address: ": "address"}

        self.fields_programme = {"Programme applying for: ": "programme"}

        self.fields_school = {"Board: ": "board",
                              "Passing Year: ": "passing",
                              "Institute Name: ": "institute",
                              "Overall Percentage of marks: ": "percentage"}

        self.fields_signature = {"Candidate Signature: ": "sig"}

        self.user_input = {}


class ApplicationPortal:

    def __init__(self):
        self.currentApplicationForm = None

    def generateApplicationForm(self):
        if self.currentApplicationForm is None:
            self.currentApplicationForm = ApplicationForm()
            return self.currentApplicationForm
        else:
            return self.currentApplicationForm

    def showApplicationForm(self, details):
        print("=========== APPLICATION FOR ADMISSION ================")
        x = datetime.datetime.now()
        print("Date: " + x.strftime("%x"))

        print("\n")
        print("==== PERSONAL INFORMATION =====")
        k = 0
        for field, name in self.currentApplicationForm.fields_personal.items():
            print(field + details[k])
            self.currentApplicationForm.user_input[name] = details[k]
            k = k + 1

        print("\n")
        print("==== PROGRAMME INFORMATION ====")
        for field, name in self.currentApplicationForm.fields_programme.items():
            print(field)
            self.currentApplicationForm.user_input[name] = input()

        print("\n")
        print("==== SCHOOLING INFORMATION ====")
        for field, name in self.currentApplicationForm.fields_school.items():
            print(field)
            self.currentApplicationForm.user_input[name] = input()

        print("\n")
        print("==== DECLARATION ====")
        print("I have provided all the information to the best my knowledge. Withholding or misrepresenting of "
              "information will lead to cancellation of my candidature at any time during/after admission process.")
        print("Candidate Signature: ")
        self.currentApplicationForm.user_input["sig"] = input()

    def completenessChecker(self):
        flag = True
        for key, value in self.currentApplicationForm.user_input.items():
            if value is not None and len(value) == 0:
                flag = False

        if not flag:
            print("=========== APPLICATION PORTAL ================")
            print("Form not filled completely!")
            # stop timer

        return flag

    def storeApplicationForm(self):
        try:
            sqliteConnection = sqlite3.connect("admission_database.db")
            cursor = sqliteConnection.cursor()

            sqlite_insert_query = "INSERT INTO candidates (name, dob, fname, mname, gender, category, email, mobile, " \
                                  "address, programme, board, institute, passing, percentage, sig) VALUES (" \
                                  "'" + self.currentApplicationForm.user_input["name"] + "'," \
                                                                                         "'" + \
                                  self.currentApplicationForm.user_input["dob"] + "'," \
                                                                                  "'" + \
                                  self.currentApplicationForm.user_input["fname"] + "'," \
                                                                                    "'" + \
                                  self.currentApplicationForm.user_input["mname"] + "'," \
                                                                                    "'" + \
                                  self.currentApplicationForm.user_input["gender"] + "'," \
                                                                                     "'" + \
                                  self.currentApplicationForm.user_input["category"] + "'," \
                                                                                       "'" + \
                                  self.currentApplicationForm.user_input["email"] + "'," \
                                                                                    "'" + \
                                  self.currentApplicationForm.user_input["mobile"] + "'," \
                                                                                     "'" + \
                                  self.currentApplicationForm.user_input["address"] + "'," \
                                                                                      "'" + \
                                  self.currentApplicationForm.user_input["programme"] + "'," \
                                                                                        "'" + \
                                  self.currentApplicationForm.user_input["board"] + "'," \
                                                                                    "'" + \
                                  self.currentApplicationForm.user_input["institute"] + "'," \
                                                                                        "'" + \
                                  self.currentApplicationForm.user_input["passing"] + "'," \
                                                                                      "'" + \
                                  self.currentApplicationForm.user_input["percentage"] + "'," \
                                                                                         "'" + \
                                  self.currentApplicationForm.user_input["sig"] + "');"

            cursor.execute(sqlite_insert_query)
            sqliteConnection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

    def printApplicationForm(self):
        print("=========== APPLICATION FOR ADMISSION ================")
        x = datetime.datetime.now()
        print("Date: " + x.strftime("%x"))

        print("\n")
        print("==== PERSONAL INFORMATION =====")
        for field, name in self.currentApplicationForm.fields_personal.items():
            print(field + self.currentApplicationForm.user_input[name])

        print("\n")
        print("==== PROGRAMME INFORMATION ====")
        for field, name in self.currentApplicationForm.fields_programme.items():
            print(field + self.currentApplicationForm.user_input[name])

        print("\n")
        print("==== SCHOOLING INFORMATION ====")
        for field, name in self.currentApplicationForm.fields_school.items():
            print(field + self.currentApplicationForm.user_input[name])

        print("\n")
        print("==== DECLARATION ====")
        print("I have provided all the information to the best my knowledge. Withholding or misrepresenting of "
              "information will lead to cancellation of my candidature at any time during/after admission process.")
        print("Candidate Signature: " + self.currentApplicationForm.user_input["sig"])


class Administration:

    def __init__(self):
        self.currentShortList = None
        self.finalScores = {}
        self.interviewScores = {}

    def conductInterview(self, selectionPortal):
        self.currentShortList = selectionPortal.getShortList()

        print("=========== INTERVIEW IN PROGRESS ================")
        print("REGISTRATION NO. - NAME - MARKS")
        for row in self.currentShortList:
            print(str(row[0]) + " - " + str(row[1]) + " - " + str(row[2]))
            print("Interview Score?: (out of 10)")
            interviewScore = int(input())
            self.interviewScores[int(row[0])] = interviewScore
            self.finalScores[int(row[0])] = interviewScore + int(row[2])

        self.sendInterviewScores(selectionPortal)

    def sendInterviewScores(self, selectionPortal):
        selectionPortal.storeFinalScores(self.interviewScores, self.finalScores)


class Candidate:
    def __init__(self, name, dob, fname, mname, gender, category, email, mobile, address):
        self.name = name
        self.dob = dob
        self.fname = fname
        self.mname = mname
        self.gender = gender
        self.category = category
        self.email = email
        self.mobile = mobile
        self.address = address
        self.details = [name, dob, fname, mname, gender, category, email, mobile, address]

    def fillApplicationForm(self, applicationPortal):
        applicationPortal.generateApplicationForm()
        applicationPortal.showApplicationForm(self.details)

    def viewApplicationForm(self, applicationPortal):
        applicationPortal.printApplicationForm()

    def submitApplicationForm(self, applicationPortal):
        applicationPortal.storeApplicationForm()

    def printAdmitCard(self, testingPortal):
        admitCard = testingPortal.generateAdmitCard(self.name, self.dob)
        if admitCard is not None:
            testingPortal.printAdmitCard()

        return admitCard

    def takeTest(self, testingPortal):
        testingPortal.conductTest()

    def checkMeritList(self, selectionPortal):
        selectionPortal.printMeritList()

    def checkShortList(self, selectionPortal):
        selectionPortal.printShortList()

    def checkSelectionList(self, selectionPortal):
        selectionPortal.printSelectionList()

    def checkWaitingList(self, selectionPortal):
        selectionPortal.printWaitList()

    def payAdmissionFee(self, feePortal):
        feePortal.pay_fees()

    def registerForProgram(self, registrationPortal):
        registrationPortal.register_for_program()

    def printAdmissionLetter(self, registrationPortal):
        registrationPortal.generate_admission_letter()
        registrationPortal.print_Admission_Letter()

class UnknownUser:

    def registerUser(self):
        print("=========== REGISTER USER ================")

        print("\n")
        print("==== PERSONAL INFORMATION =====")
        print("Your full name: ")
        name = input()
        print("Date of Birth: ")
        dob = input()
        print("Father's name: ")
        fname = input()
        print("Mother's name: ")
        mname = input()
        print("Gender: ")
        gender = input()
        print("Category: ")
        category = input()
        print("Email: ")
        email = input()
        print("Mobile Number: ")
        mobile = input()
        print("Address: ")
        address = input()

        return Candidate(name, dob, fname, mname, gender, category, email, mobile, address)

if __name__ == '__main__':
    applicationPortal = ApplicationPortal()

    unknownUser = UnknownUser()

    candidate = unknownUser.registerUser()
    candidate.fillApplicationForm(applicationPortal)

    complete = applicationPortal.completenessChecker()
    while not complete:
        candidate.fillApplicationForm(applicationPortal)
        complete = applicationPortal.completenessChecker()

    candidate.viewApplicationForm(applicationPortal)
    candidate.submitApplicationForm(applicationPortal)

    testingPortal = TestingPortal()
    admitCard = candidate.printAdmitCard(testingPortal)
    if admitCard is not None:
        candidate.takeTest(testingPortal)

        selectionPortal = SelectionPortal()
        candidate.checkMeritList(selectionPortal)
        candidate.checkShortList(selectionPortal)

        administration = Administration()
        administration.conductInterview(selectionPortal)

        candidate.checkSelectionList(selectionPortal)
        candidate.checkWaitingList(selectionPortal)

        feePortal = Fee_payment()
        candidate.payAdmissionFee(feePortal)

        registrationPortal = Program_register()
        candidate.registerForProgram(registrationPortal)

        candidate.printAdmissionLetter(registrationPortal)

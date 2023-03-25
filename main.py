import requests
from bs4 import BeautifulSoup
import smtplib
import tkinter as tk
from datetime import datetime
from threading import Thread, Event

font = "Verdana", 10


# The purpose of this program is to scan the Estonian ARK website periodically for driving exam times and notify
# the user of an opening via email in a +1 month time range in the selected city

class ARKWBS:

    ##
    # Initializes the tkinter powered GUI for the application.
    # This function returns nothing and starts tkinter main loop.
    # @param    self    class instance
    # @return   None
    ##

    def __init__(self):
        self.thread = None
        self.TERM_FLAG = Event()
        self.state_running = False
        self.win = tk.Tk()
        self.win.title("ARKi eksamiajad")
        self.win.resizable(False, False)
        self.win.geometry("540x240")
        self.opmenval = ""
        self.cities = ["Tartu", "Viljandi", "Pärnu", "Rakvere", "Paide", "Haapsalu", "Kuressaare", "Narva", "Jõhvi",
                       "Rapla", "Tallinn", "Võru"]
        self.login_info = "", ""

        lab1 = tk.Label(self.win, text="ARKi webscraper release 0.2", font=font)
        lab1.place(x=10, y=10)
        lab2 = tk.Label(self.win, text="The following program is designed to aid people in\n"
                                       "pumping their driver's examination time up. The\n"
                                       "program scans the Estonian DMV website periodically\n"
                                       "for an examination time in the chosen city."
                        , font=("Verdana", 8), anchor='w')

        lab2.place(x=10, y=40)
        self.but1 = tk.Button(self.win, text="Run", font=font, width=20, command=lambda: self.main())
        self.but1.place(x=360, y=40)

        fname1 = tk.Label(self.win, text="User email", font=("Arial", 8))
        fname2 = tk.Label(self.win, text="Email address for SMTP server", font=("Arial", 8))
        fname3 = tk.Label(self.win, text="Password for SMTP email account", font=("Arial", 8))

        self.target_email = tk.Entry(self.win, width=40)
        self.email_serv = tk.Entry(self.win, width=40)
        self.pw_serv = tk.Entry(self.win, width=40)

        self.target_email.place(x=10, y=120)
        fname1.place(x=10, y=100)
        self.email_serv.place(x=10, y=160)
        fname2.place(x=10, y=140)
        self.pw_serv.place(x=10, y=200)
        fname3.place(x=10, y=180)

        variable = tk.StringVar(self.win)
        variable.set(self.cities[0])
        self.opmenval = self.cities[0]

        opmen = tk.OptionMenu(self.win, variable, *self.cities, command=lambda b: self.update(b))
        opmen.pack()
        opmen.place(x=270, y=140)
        fname5 = tk.Label(self.win, text="City", font=("Arial", 8))
        fname5.place(x=270, y=120)

        tk.mainloop()

    ##
    # Sends an email to the user specified email address containing the found exam time.
    # @param    aeg     custom time format in which the time is scraped from the ARK website
    # @return   None
    ##

    def saadameil(self, aeg):
        # Open a connection to the smtp server
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            # Use the user entered email account information to login
            self.login_info = self.email_serv.get(), self.pw_serv.get()
            try:
                smtp.login(self.login_info[0], self.login_info[1])
                subject = "ARKi aeg - " + aeg
                body = "ARKis on vabanenud parameetritele vastav sõidueksami aeg:\nLinn: " + \
                       str(self.opmenval) + "\nAeg: " + str(aeg) + "\n\n\nBrought to you by sygism"
                msg = f'Subject: {subject}\n\n{body}'
                smtp.sendmail(self.login_info[0], self.target_email.get(), msg.encode("utf-8"))
            except (smtplib.SMTPResponseException, Exception) as e:
                e = str(e).split(" ")
                length = int(len(e) / 3)
                out = ""
                for i in range(len(e)):
                    out += " " + str(e[i])
                    if i == length:
                        out += "\n"
                        length *= 2

    ##
    # Scrapes the free exam time website for suitable exam times in a +1 month period.
    # The function uses the bs4 library to achieve this.
    # @param    self    class instance
    # @return   None
    ##

    def fetch_info(self):
        # GET request the site
        result = requests.get("https://eteenindus.mnt.ee/public/vabadSoidueksamiajad.xhtml")
        soup = BeautifulSoup(result.content, features="html.parser")
        # Find the div containing all exam times sorted by earliest
        data = soup.find("div", {"id": "eksami_ajad:kategooriaBEksamiAjad"})
        h = ""
        # Extract the time string from div content
        if data is not None:
            for points in data:
                h = str(points.text)
            ind = h.find(self.opmenval)
            aeg = ""
            for i in range(ind + 5, ind + 15):
                aeg += h[i]
            f = aeg[3:5]
            today = datetime.today()
            kuu = today.month
            # If the month of the exam time is the current month or the next one, send an email to the user
            if int(float(f)) == kuu or int(float(f)) == kuu + 1:
                self.saadameil(aeg)

    ##
    # Starts or kills the main loop when 'Run' button is pressed.
    # @param    self    class instance
    # @return   None
    ##

    def main(self):
        # If the loop is not running start the periodic loop
        if not self.state_running:
            self.state_running = True
            self.but1.config(text="Press again to cancel")
            self.thread = RepeatTimer(self.TERM_FLAG)
            self.thread.start()
        # If the loop is running, kill it
        else:
            self.state_running = False
            self.but1.config(text="Run")
            self.TERM_FLAG.set()

    ##
    # Updates the option dropdown menu value according to the selection.
    # @param    self    class instance
    # @param    b       option menu value to be set
    # @return   None
    ##
    def update(self, b):
        self.opmenval = b


##
# Simple implementation of a repeated timer thread.
# @param    Thread  Python native threading library
# @param    ARKWBS  The webscraper app class
# @return   None
##

class RepeatTimer(Thread, ARKWBS):
    def __init__(self, flag):
        Thread.__init__(self)
        self.STOP_FLAG = flag

    def run(self):
        while not self.STOP_FLAG.wait(3):
            ARKWBS.fetch_info(self)


if __name__ == "__main__":
    instance = ARKWBS()

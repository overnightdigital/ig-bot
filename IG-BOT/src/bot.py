# 1. Import and explain selenium
from selenium import webdriver
# 2. Explain those two imports
import os
import time
import datetime
from datetime import timedelta

# 13. Add Later for Selenium Web Driver Wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 22. Import for GUI explain the library and so on
import tkinter as tk

# 38. Import Sched for creating jobs
from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()  
sched.start()

# 33. Create a class for our objects
class ScheduleObject:
    def __init__(self, username, password, amount, hashtag, date, label):
        self.username = username.get()
        self.password = password.get()
        self.amount = amount.get()
        self.hashtag = hashtag.get()
        self.date = date.get()
        self.label = label
        # 35. Save the timestamp
        self.timestamp = time.mktime(datetime.datetime.strptime(self.date, '%Y-%m-%d %H:%M').timetuple())

# 3. Explain how we will proceed and why we need a class
# 4. Explain the class just a little bit
class InstagramBot:
    # 5. Explain the definition
    def __init__(self, username, password, amount, hashtag):
        # 6. Explain self
        self.username = username
        self.password = password
        self.amount = amount
        self.hashtag = hashtag

        # 7. Explain where the driver comes from and what this line of code does
        # 8. Explain how to download the cgromedriver
        self.driver = webdriver.Chrome('./chromedriver.exe')

        # 14. Add Later as variables and exlpain the self thing
        self.webDriverWait = WebDriverWait
        self.ec = EC
        self.by = By

        # 9. Explain what this line does how it navigates to this page
        # 10. Explain also how the init is executed on class initialization and how it calls the login
        self.login()
        #self.driver.get('https://www.instagram.com/')

        # 16. Now lets search for hashtags also add sleep to wait for the page to load
        # self.inf_scroll()
        time.sleep(5)

        self.explore_hashtags(self.hashtag)

        time.sleep(2)

        self.like_posts(int(self.amount))

        time.sleep(3)
        self.driver.quit()

    def login(self):
        self.driver.get('https://www.instagram.com/accounts/login/')

        # 11. Explain how we need to wait for the element to be availible
        self.webDriverWait(self.driver, 20).until(self.ec.presence_of_element_located((self.by.NAME, 'username')))
        self.webDriverWait(self.driver, 20).until(self.ec.presence_of_element_located((self.by.NAME, 'password')))
        self.webDriverWait(self.driver, 20).until(self.ec.element_to_be_clickable((self.by.XPATH, '//*[contains(text(), "Log In")]')))

        # 12. Explain how those work and what send_keys does point to docu maybe
        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        # 15. Explain the search by xpath here
        self.driver.find_element_by_xpath('//*[contains(text(), "Log In")]').click()


    # 17. Explain method navigate to explore
    def explore_hashtags(self, hashtag):
        self.driver.get('https://www.instagram.com/explore/tags/' + hashtag)

    # 18. Like Posts explain the amount
    def like_posts(self, amount):
        # 19. Search by class name its consistent so we can use it here mention it could also be changed
        self.driver.find_element_by_class_name('v1Nh3').click()

        i = 1
        while i <= amount:
            # 20. Wait to load, then like the photo and then go to the next photo
            time.sleep(1)
            self.driver.find_element_by_class_name('fr66n').click()
            self.driver.find_element_by_class_name('coreSpriteRightPaginationArrow').click()
            i += 1

        # 21. Redirect back to the start when finished
        self.driver.get('https://instagram.com/')    
   

# 23. Explain best practice lets make a new class(Link: https://www.begueradj.com/tkinter-best-practices/)
class MainApplication(tk.Frame):
    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.gui = self.configure_gui()
        self.widgets = self.create_widgets()
        # 32. Add the list to keep track
        self.scheduleObjects = []
   
    def configure_gui(self):
        # 25. Explain the referencing from self.master to root
        self.master.geometry('1000x700')

    def create_widgets(self):
        # 26. Now lets add a button to run our program / explain the command to run
        scheduleRun = tk.Button(self.master, text="Schedule", font=("Helvetica", 18), padx=10, pady=5, fg="#FFF", bg="#3582e8", command=self.runBot)
        scheduleRun.grid(column=0, row=5, padx=10, pady=30)
        
        # 29. Add the widgets and lables one for amount the hashtag and time
        amountLabel = tk.Label(self.master, text="Amount", font=("Helvetica", 18))
        amountLabel.grid(column=0, row=2, padx=10, pady=10)

        # 30. Explain on the way how the system with the columns and rows works
        amountEntry = tk.Entry(self.master, width=15, font=("Helvetica", 18))
        amountEntry.grid(column=1, row=2, padx=10, pady=10)

        hashtagLabel = tk.Label(self.master, text="Hashtag", font=("Helvetica", 18))
        hashtagLabel.grid(column=0, row=3, padx=10, pady=10)

        hashtagEntry = tk.Entry(self.master, width=15, font=("Helvetica", 18))
        hashtagEntry.grid(column=1, row=3, padx=10, pady=10)

        dateLabel = tk.Label(self.master, text="Date (2018-06-22 08:15)", font=("Helvetica", 18))
        dateLabel.grid(column=0, row=4, padx=10, pady=10)

        dateEntry = tk.Entry(self.master, width=15, font=("Helvetica", 18))
        dateEntry.grid(column=1, row=4, padx=10, pady=10)

        usernameLabel = tk.Label(self.master, text="Username", font=("Helvetica", 18))
        usernameLabel.grid(column=0, row=0, padx=10, pady=10)

        usernameEntry = tk.Entry(self.master, width=15, font=("Helvetica", 18))
        usernameEntry.grid(column=1, row=0, padx=10, pady=10)

        passwordLabel = tk.Label(self.master, text="Password", font=("Helvetica", 18))
        passwordLabel.grid(column=0, row=1, padx=10, pady=10)

        passwordEntry = tk.Entry(self.master, width=15, show='*', font=("Helvetica", 18))
        passwordEntry.grid(column=1, row=1, padx=10, pady=10)

        # 31. Explain the return to be used then in the run function
        return amountEntry, hashtagEntry, dateEntry, usernameEntry, passwordEntry

    # 28. Here we need now to run our instageram bot from this class
    def runBot(self):
        amount, hashtag, date, username, password = self.widgets
        # 34. Add the object to the list
        # 36. Display the objects from the list by adding them to a new list of labels starting by highest row
        resultsLabel = tk.Label(self.master, anchor="e", justify=tk.LEFT, text=" * Hashtag: " + hashtag.get() + " | Amount: " + amount.get() + " | Date: " + date.get(), font=("Helvetica", 13))
        resultsLabel.grid(column=0, row=len(self.scheduleObjects) + 6, padx=10, pady=2)
        
        scheduleObject = ScheduleObject(username, password, amount, hashtag, date, resultsLabel)
        self.scheduleObjects.append(scheduleObject)
        
        # 37. Now we need to check for the time and run the script based on that
        sched.add_job(lambda: self.startBot(username, password, amount, hashtag), "date", next_run_time=date.get()+":00")
        print("Scheduled Bot")
		
    def startBot(self, username, password, amount, hashtag):
        # 39. Remove executed objects from the list
        ts = int(time.time())
        currentObj = None
        for o in self.scheduleObjects:
            if o.timestamp == ts:
                currentObj = o
                o.label.destroy()
                self.scheduleObjects.remove(o)

        print("Bot Started")
        ig_bot = InstagramBot(currentObj.username, currentObj.password, currentObj.amount, currentObj.hashtag)   


if __name__ == '__main__':
    # 24. Explain the root holds the entire app
    root = tk.Tk()
    root.title("IG BOT")
    # 27. Now lets run everything
    main_app = MainApplication(root)
    root.mainloop() 





# 0 - 21 Basic Functionality
# 22 - 31 GUI
# 32 - 39 Scheduling





# NOT USED
# # 17. Explain new method and way of scrolling
# def inf_scroll(self):
#     SCROLL_PAUSE_TIME = 5

#     # 18. Explain the process of last new height and how the driver can execute a script maybe reference docs
#     last_height = self.driver.execute_script("return document.body.scrollHeight")

#     while True:
#         # Scroll down to bottom
#         self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#         # 19. Explain we need to wait for page load
#         time.sleep(SCROLL_PAUSE_TIME)

#         # Calculate new scroll height and compare with last scroll height
#         new_height = self.driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             break
#         last_height = new_height          
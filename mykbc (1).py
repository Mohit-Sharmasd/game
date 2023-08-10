import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import os
import pandas as pd
import random
import pygame
import pyttsx3
import time
import urllib
import requests
import urllib.request
from io import BytesIO

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
from pygame import mixer

mixer.init()
def spech(text):
	engine = pyttsx3.init()
	engine.setProperty("rate",140)
	engine.setProperty("volume",10)
	engine.say(text)
	engine.runAndWait()
spech("Welcome to the KBC game!")

# Define the questions and answers

qa_file_path = 'https://github.com/yash2001181/kbc_game/raw/main/kbc_game_attachment/questions_answers.csv?raw=true'

# Read the CSV file into a DataFrame
df = pd.read_csv(qa_file_path, delimiter=',')

# Print the DataFrame
# print(df)

# column_name = 'Question'
# selected_column = df[column_name][:20]
# Access a specific column (e.g., 'Question')
# Access a specific column (e.g., 'Question')
get_question = df['Question'].tolist()
get_first_option = df['Option A'].tolist()
get_second_option = df['Option B'].tolist()
get_third_option = df['Option C'].tolist()
get_fourth_option = df['Option D'].tolist()
get_answer = df['Answer'].tolist()

# Generate 20 random unique indices to select random questions
random_indices = random.sample(range(len(get_question)), 20)
print(random_indices)

question = []
first_option = []
second_option = []
third_option = []
fourth_option = []
answer = []

# Print 20 random questions with their options and answers
for index in random_indices:
    inx_question = get_question[index]
    inx_first_option = get_first_option[index]
    inx_second_option = get_second_option[index]
    inx_third_option = get_third_option[index]
    inx_fourth_option = get_fourth_option[index]
    inx_answer = get_answer[index]

    # Append the selected values to their respective lists
    question.append(inx_question)
    first_option.append(inx_first_option)
    second_option.append(inx_second_option)
    third_option.append(inx_third_option)
    fourth_option.append(inx_fourth_option)
    answer.append(inx_answer)

x = pd.DataFrame({'Question': question, 'first_option': first_option, 'second_option': second_option,
                  'third_option': third_option, 'fourth_option': fourth_option, 'Answers': answer})

lifelines_used = {"50-50": False, "Call a Friend": False, "Audience Poll": False}

questionIndex = 0
# Initialize the current amount
current_amount = 1000

def reset_lifelines():
    global lifelines_used
    lifelines_used = {"50-50": False, "Call a Friend": False, "Audience Poll": False}
    lifeline50Button.config(state=tk.NORMAL)
    phoneAFriend52Button.config(state=tk.NORMAL)
    audiencePoll51Button.config(state=tk.NORMAL)


def select(event):
    global questionIndex, current_amount
    if lifelines_used["Audience Poll"]:
        audiencePoll51Button.config(state=tk.DISABLED)

    b = event.widget
    value = b['text']
    # Reset 50-50 lifeline buttons
    optionButton1.config(state=tk.NORMAL)
    optionButton2.config(state=tk.NORMAL)
    optionButton3.config(state=tk.NORMAL)
    optionButton4.config(state=tk.NORMAL)

    optionButton1.bind('<Button-1>', select)
    optionButton2.bind('<Button-1>', select)
    optionButton3.bind('<Button-1>', select)
    optionButton4.bind('<Button-1>', select)

    # Clear the Audience Poll result label
    audience_poll_result_label.config(text="")


    def handle_answer():
        global current_amount, questionIndex

        # Assuming 'answer' is a list containing the correct answers corresponding to each question index
        print(questionIndex)
        if value == answer[questionIndex]:
            questionIndex = (questionIndex + 1) % len(question)

            # Update the UI with the next question and options
            questionArea.delete(1.0, END)
            questionArea.insert(END, question[questionIndex])

            current_amount += 1000  # Increase the amount by $1000 (you can adjust the amount as needed)
            amount_label_value.set(f'Amount: ₹{current_amount}')  # Update the amount label text

            optionButton1.config(text=first_option[questionIndex])
            optionButton2.config(text=second_option[questionIndex])
            optionButton3.config(text=third_option[questionIndex])
            optionButton4.config(text=fourth_option[questionIndex])
        else:
            tryagain_window()

        return questionIndex

    def tryagain_window():
        def close():
            root1.destroy()
            root.destroy()

        def tryagain():
            global questionIndex, current_amount

            reset_lifelines()
            current_amount = 1000  # Reset the amount value to 0

            questionIndex = 0
            questionArea.delete(1.0, END)
            questionArea.insert(END, question[0])
            optionButton1.config(text=first_option[0])
            optionButton2.config(text=second_option[0])
            optionButton3.config(text=third_option[0])
            optionButton4.config(text=fourth_option[0])
            amount_label_value.set(f'Amount: ₹{current_amount}')
            root1.destroy()

        root1 = Toplevel()
        root1.config(bg='black')
        root1.geometry('1270x652+0+0')
        root1.title("Sorry, you gave the wrong answer and your game is ended now")

        imgLabel = Label(root1, image=kbc_logo, bg='black', bd=0, activebackground='black',
                         highlightbackground='black', highlightthickness=0, width=380, height=280)
        imgLabel.pack(pady=50)

        loseLabel = Label(root1, text=f'You lose and you win Amount: ₹{current_amount}',
                          font=('arial', 40, 'bold'),
                          bg='black', fg='white')
        
        loseLabel.pack()

        tryagainButton = tk.Button(root1, text='Try Again', font=('arial', 20, 'bold'), bg='black', fg='white',
                                   activebackground='black', activeforeground='white', bd=0, cursor='hand2',
                                   command=tryagain)
        tryagainButton.pack()

        closeButton = tk.Button(root1, text='Close', font=('arial', 20, 'bold'), bg='black', fg='white',
                                activebackground='black', activeforeground='white', bd=0, cursor='hand2',
                                command=close)
        closeButton.pack()

        root1.mainloop()

    # Assuming 'value' is the selected answer and 'questionIndex' is the current question index
    # Call the function to handle the answer and get the updated question index
    # Replace this with the actual method to get the selected answer
    handle_answer()


    def show_congratulations_window(current_amount):
        global questionIndex
        root2 = Toplevel()
        root2.config(bg='black')
        root2.geometry('1270x652+0+0')
        root2.title("Congratulations! You Won!")

        imgLabel = Label(root2, image=kbc_logo, bg='black', bd=0, activebackground='black',
                         highlightbackground='black', highlightthickness=0, width=380, height=280)
        imgLabel.pack(pady=50)

        winLabel = Label(root2, text=f'Congratulations! You Won! Amount: ₹{current_amount}', font=('arial', 40, 'bold'),
                         bg='black',
                         fg='white')
        winLabel.pack()

        # closeButton = tk.Button(root2, text='Close', font=('arial', 20, 'bold'), bg='black', fg='white',
        #                         activebackground='black', activeforeground='white', bd=0, cursor='hand2',
        #                         command=close)
        # closeButton.pack()

        root.after(4000, root.destroy)
        root2.mainloop()





    # Assuming 'questionIndex' is the current question index
    # Assuming 'value' is the selected answer
    # Replace this with the actual method to get the selected answer
    print(questionIndex)
    print(len(question))
    if questionIndex == len(question) - 1:
        show_congratulations_window(current_amount)



    if not lifelines_used["50-50"]:
        lifeline50Button.config(state=tk.NORMAL)
    if not lifelines_used["Call a Friend"]:
        phoneAFriend52Button.config(state=tk.NORMAL)
    if not lifelines_used["Audience Poll"]:
        audiencePoll51Button.config(state=tk.NORMAL)


def use_fifty_fifty():
    global lifelines_used, questionIndex

    if not lifelines_used["50-50"]:
        question_idx = questionIndex
        correct_option = answer[question_idx]
        options = [first_option[question_idx], second_option[question_idx], third_option[question_idx],
                   fourth_option[question_idx]]
        options.remove(correct_option)
        # Randomly select one incorrect option to keep
        incorrect_option_to_keep = random.choice(options)
        options.remove(incorrect_option_to_keep)

        # Disable the buttons corresponding to the removed options
        optionButton1.config(state=tk.DISABLED if first_option[question_idx] in options else tk.NORMAL)
        optionButton2.config(state=tk.DISABLED if second_option[question_idx] in options else tk.NORMAL)
        optionButton3.config(state=tk.DISABLED if third_option[question_idx] in options else tk.NORMAL)
        optionButton4.config(state=tk.DISABLED if fourth_option[question_idx] in options else tk.NORMAL)

        # Unbind click event for incorrect options
        if first_option[question_idx] in options:
            optionButton1.unbind('<Button-1>')
        if second_option[question_idx] in options:
            optionButton2.unbind('<Button-1>')
        if third_option[question_idx] in options:
            optionButton3.unbind('<Button-1>')
        if fourth_option[question_idx] in options:
            optionButton4.unbind('<Button-1>')

        lifelines_used["50-50"] = True
        lifeline50Button.config(state=tk.DISABLED)


def use_audience_poll():
    global lifelines_used, questionIndex

    if not lifelines_used["Audience Poll"]:
        question_idx = questionIndex
        correct_option = answer[question_idx]
        total_votes = 100  # Total number of votes for the audience poll

        # Randomly assign votes to options (including the correct option)
        votes_correct_option = random.randint(total_votes // 2, total_votes)
        votes_incorrect_option1 = random.randint(0, total_votes // 4)
        votes_incorrect_option2 = total_votes - votes_correct_option - votes_incorrect_option1
        votes_incorrect_option3 = 0  # Since we have only 3 incorrect options

        # # Update the text of the option buttons with the vote count
        # optionButton1.config(text=f"{first_option[question_idx]} - {votes_correct_option} votes", font=('arial', 14, 'bold'))
        # optionButton2.config(text=f"{second_option[question_idx]} - {votes_incorrect_option1} votes", font=('arial', 14, 'bold'))
        # optionButton3.config(text=f"{third_option[question_idx]} - {votes_incorrect_option2} votes", font=('arial', 14, 'bold'))
        # optionButton4.config(text=f"{fourth_option[question_idx]} - {votes_incorrect_option3} votes", font=('arial', 14, 'bold'))

        # Create a new label to show the Audience Poll result
        audience_poll_result_label.config(text=f"Audience Poll Result:\n"
                                               f"{first_option[question_idx]} - {votes_correct_option} votes\n"
                                               f"{second_option[question_idx]} - {votes_incorrect_option1} votes\n"
                                               f"{third_option[question_idx]} - {votes_incorrect_option2} votes\n"
                                               f"{fourth_option[question_idx]} - {votes_incorrect_option3} votes")

        # Disable the lifeline button and mark it as used
        lifelines_used["Audience Poll"] = True
        audiencePoll51Button.config(state=tk.DISABLED)


def use_phoneFriend():
    global lifeline_used, questionIndex, phone_friend_used
    # Load music from Google Drive link using pygame.mixer
    music_url = "https://github.com/yash2001181/kbc_game/blob/main/kbc_game_attachment/calling.mp3?raw=true"
    response = requests.get(music_url,stream = True)
    # Check if the request was successful
    if response.status_code == 200:
        # Create a BytesIO object to hold the music content
        music_content = response.content

        # Create a Sound object using the music content
        phone_friend_music = pygame.mixer.Sound(file=BytesIO(music_content))

        # Play the phone friend music
         # Check if the request was successful
    if response.status_code == 200:
        # Create a BytesIO object to hold the music content
        music_content = response.content

        # Create a Sound object using the music content
        phone_friend_music = pygame.mixer.Sound(file=BytesIO(music_content))

        # Play the phone friend music
        phone_friend_music.play()
    # Wait until the ringing sound finishes playing
    while pygame.mixer.get_busy():
         pygame.time.delay(400)  # Delay for 400 milliseconds

    for i in range(len(question)):
        if questionArea.get(1.0, 'end-1c') == question[i]:
            engine.say(f'the answer is {answer[i]}')
            engine.runAndWait()

        lifelines_used["Call a Friend"] = True
        phoneAFriend52Button.config(state=tk.DISABLED)


root = tk.Tk()
root.geometry('1270x652+0+0')
root.title('Kaun Banega Crorepati')
root.config(bg='black')

# Left frame settings
leftframe = tk.Frame(root, bg='black', padx=90)
leftframe.grid(row=0, column=0)

# Top frame settings
topframe = tk.Frame(leftframe, bg='black', pady=15)
topframe.grid()

# Centre frame settings
centerframe = tk.Frame(leftframe, bg='black', pady=15)
centerframe.grid(row=1, column=0)

# Bottom frame creation
bottomframe = tk.Frame(leftframe)
bottomframe.grid(row=2, column=0)

# Right frame settings
rightFrame = tk.Frame(root, pady=25, padx=50, bg='black')
rightFrame.grid(row=0, column=1)

# Create a label to display the Audience Poll result
audience_poll_result_label = tk.Label(leftframe, text="", font=('arial', 14, 'bold'), bg='black', fg='white')
audience_poll_result_label.grid(row=2, column=0)


def create_button(parent, image_path, row, column):
    image = ImageTk.PhotoImage(Image.open(image_path))
    button = tk.Button(parent, image=image, bg='black', bd=0, activebackground='black', highlightbackground='black',
                       highlightthickness=0, width=180, height=80, cursor='hand2')
    button.image = image
    button.grid(row=row, column=column)
    return button


# Button creation (50-50 lifeline button)
url = "https://github.com/yash2001181/kbc_game/blob/main/kbc_game_attachment/50-50.png?raw=true"
headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(url, headers=headers)

try:
    image50_path = urllib.request.urlopen(req)
    lifeline50Button = create_button(topframe, image50_path, 0, 0)
    # Create a button to use the 50-50 lifeline
    lifeline50Button.config(command=use_fifty_fifty)
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")

# Replace YOUR_AUDIENCE_POLL_IMAGE_ID with the actual ID of your audience poll image

url = "https://github.com/yash2001181/kbc_game/blob/main/kbc_game_attachment/audiencePole.png?raw=true"
headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(url, headers=headers)

try:
    image51_path = urllib.request.urlopen(req)
    audiencePoll51Button = create_button(topframe, image51_path, 0, 1)
    audiencePoll51Button.config(command=use_audience_poll)

except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")

# Button creation (phone a friend button)
# Replace YOUR_PHONE_FRIEND_IMAGE_ID with the actual ID of your phone a friend image

url = "https://github.com/yash2001181/kbc_game/blob/main/kbc_game_attachment/phoneAFriend.png?raw=true"
headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(url, headers=headers)

try:
    image52_path = urllib.request.urlopen(req)
    phoneAFriend52Button = create_button(topframe, image52_path, 0, 2)
    phoneAFriend52Button.config(command=use_phoneFriend)
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")

# Replace YOUR_LOGO_IMAGE_ID with the actual ID of your KBC logo image

url = "https://github.com/yash2001181/kbc_game/blob/main/kbc_game_attachment/kbc_logo.png?raw=true"
headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(url, headers=headers)

try:
    response = urllib.request.urlopen(req)
    kbc_logo = ImageTk.PhotoImage(Image.open(response))
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")

# KBC logo label
kbc_logo_label = tk.Label(centerframe, image=kbc_logo, bg='black', bd=0, activebackground='black',
                          highlightbackground='black', highlightthickness=0, width=380, height=280)
kbc_logo_label.pack()
# amount images update




# Create a label to display the current amount
amount_label_value = tk.StringVar()
amount_label_value.set(f'Amount: ₹{current_amount}')  # Set the initial value of the amount label

amount_label_label = tk.Label(rightFrame, textvariable=amount_label_value, font=('arial', 16, 'bold'),
                              bg='black', fg='white', bd=0, activebackground='black', activeforeground='white')
amount_label_label.pack()

# Replace YOUR_LAYOUT_IMAGE_ID with the actual ID of your layout image

url = "https://github.com/yash2001181/kbc_game/blob/main/kbc_game_attachment/lay.png?raw=true"
headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(url, headers=headers)

try:
    response = urllib.request.urlopen(req)
    layout_label = ImageTk.PhotoImage(Image.open(response))
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")

layout_label_label = tk.Label(bottomframe, image=layout_label, bg='black', bd=0, activebackground='black',
                              highlightbackground='black', highlightthickness=0)
layout_label_label.pack()
# Load the Question Bank (x) DataFrame


# question area
questionArea = Text(bottomframe, font=('arial', 14, 'bold'), width=34, height=2, wrap='word', bg='black', fg='white',
                    bd=0)
questionArea.place(x=70, y=10)
questionArea.insert(END, x['Question'][0])
# option setting
labelA = tk.Label(bottomframe, text='A:', bg='black', fg='white', font=('arial', 16, 'bold'))
labelA.place(x=60, y=110)
labelB = tk.Label(bottomframe, text='B:', bg='black', fg='white', font=('arial', 16, 'bold'))
labelB.place(x=330, y=110)
labelC = tk.Label(bottomframe, text='C:', bg='black', fg='white', font=('arial', 16, 'bold'))
labelC.place(x=60, y=190)
labelD = tk.Label(bottomframe, text='D:', bg='black', fg='white', font=('arial', 16, 'bold'))
labelD.place(x=330, y=190)
# create button for first option
option_list = x['first_option'][0].split(', ')  # Split the Options value into a list
optionButton1 = tk.Button(bottomframe, text=option_list[0], font=('arial', 16, 'bold'), bg='black', fg='white', bd=0,
                          activebackground='black', activeforeground='white', cursor='hand2')
optionButton1.place(x=100, y=100)
# option2
option_list = x['second_option'][0].split(', ')  # Split the Options value into a list
optionButton2 = tk.Button(bottomframe, text=option_list[0], font=('arial', 16, 'bold'), bg='black', fg='white', bd=0,
                          activebackground='black', activeforeground='white', cursor='hand2')
optionButton2.place(x=370, y=100)
# option3
option_list = x['third_option'][0].split(', ')  # Split the Options value into a list
optionButton3 = tk.Button(bottomframe, text=option_list[0], font=('arial', 16, 'bold'), bg='black', fg='white', bd=0,
                          activebackground='black', activeforeground='white', cursor='hand2')
optionButton3.place(x=100, y=180)
# option4
option_list = x['fourth_option'][0].split(', ')  # Split the Options value into a list
optionButton4 = tk.Button(bottomframe, text=option_list[0], font=('arial', 16, 'bold'), bg='black', fg='white', bd=0,
                          activebackground='black', activeforeground='white', cursor='hand2')
optionButton4.place(x=370, y=180)
optionButton1.bind('<Button-1>', select)
optionButton2.bind('<Button-1>', select)
optionButton3.bind('<Button-1>', select)
optionButton4.bind('<Button-1>', select)
# Create a button to start the game

root.mainloop()

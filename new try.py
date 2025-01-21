import tkinter
from tkinter import *
from tkinter import simpledialog, messagebox

# Main window function
def open_main_window():
    global root, task_list
    root = Tk()
    root.title("Daily-Dash")
    root.geometry("400x650+400+100")
    root.resizable(False, False)

    task_list = []  # Declare task_list as a global variable

    def addTask():
        task = task_entry.get("1.0", END).strip()  # Get the full content of Text widget
        task_entry.delete("1.0", END)  # Clear the Text widget
        if task:
            with open("tasklist.txt", 'a') as taskfile:
                taskfile.write(f" \n{task}")
            task_list.append(task)
            listbox.insert(END, task)

    def deleteTask():
        global task_list  # Access global task_list
        task = str(listbox.get(ANCHOR))
        if task in task_list:
            task_list.remove(task)
            with open("tasklist.txt", 'w') as taskfile:
                for task in task_list:
                    taskfile.write(task + "\n")
            listbox.delete(ANCHOR)

    def updateTask():
        task_index = listbox.curselection()[0]
        task = listbox.get(task_index)
        new_task = simpledialog.askstring("Update Task", "Enter new task")
        if new_task:
            listbox.delete(task_index)
            listbox.insert(task_index, new_task)
            with open("tasklist.txt", 'w') as taskfile:
                for i, task in enumerate(task_list):
                    if i == task_index:
                        taskfile.write(new_task + "\n")
                    else:
                        taskfile.write(task + "\n")
            task_list[task_index] = new_task

    def importantTask():
        task_index = listbox.curselection()[0]
        task = listbox.get(task_index)
        if task:
            if task.endswith("⭐"):
                listbox.delete(task_index)
                listbox.insert(task_index, task[:-1].strip())
                with open("tasklist.txt", 'w') as taskfile:
                    for i, task in enumerate(task_list):
                        if i == task_index:
                            taskfile.write(task[:-1].strip() + "\n")
                        else:
                            taskfile.write(task + "\n")
                task_list[task_index] = task[:-1].strip()
            else:
                listbox.delete(task_index)
                listbox.insert(task_index, task + "⭐")
                with open("tasklist.txt", 'w') as taskfile:
                    for i, task in enumerate(task_list):
                        if i == task_index:
                            taskfile.write(task + "*\n")
                        else:
                            taskfile.write(task + "\n")
                task_list[task_index] = task + "⭐"

    def openTaskFile():
        try:
            global task_list
            with open("tasklist.txt", "r") as taskfile:
                tasks = taskfile.readlines()
            for task in tasks:
                if task != '\n':
                    task_list.append(task.strip())  # strip to avoid trailing spaces/newlines
                    listbox.insert(END, task.strip())
        except:
            file = open('tasklist.txt', 'w')
            file.close()

    # Initialize icons and labels
    Image_icon = PhotoImage(file="image/task.png")
    root.iconphoto(False, Image_icon)

    TopImage = PhotoImage(file="image/topbar.png")
    Label(root, image=TopImage).pack()

    dockImage = PhotoImage(file="image/dock.png")
    Label(root, image=dockImage, bg="#32405b").place(x=30, y=25)

    noteImage = PhotoImage(file="image/task.png")
    Label(root, image=noteImage, bg="#32405b").place(x=340, y=25)

    heading = Label(root, text="ALL TASK", font="arial 20 bold", fg="white", bg="#32405b")
    heading.place(x=130, y=20)

    # Task input section with Text widget
    frame = Frame(root, width=400, height=50, bg="white")
    frame.place(x=0, y=180)

    task = StringVar()
    task_entry = Text(frame, width=20, height=3, font="arial 20", bd=0, wrap=WORD)  # Use Text widget here with wrap
    task_entry.place(x=10, y=7)
    task_entry.focus()

    button = Button(frame, text="ADD", font="arial 20 bold", width=6, bg="#4C0000", fg="#fff", bd=0, command=addTask)
    button.place(x=300, y=0)

    # Listbox for displaying tasks
    frame1 = Frame(root, bd=3, width=700, height=280, bg="#4C0000")
    frame1.pack(pady=(160, 0))

    listbox = Listbox(frame1, font=('arial 12 bold'), width=40, height=16, bg="#32405b", fg="white", cursor="hand2", selectbackground="#5a95ff")
    listbox.pack(side=LEFT, fill=BOTH, padx=2)
    scrollbar = Scrollbar(frame1)
    scrollbar.pack(side=RIGHT, fill=BOTH)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    openTaskFile()

    # Buttons for update, important and delete tasks
    button_frame = Frame(root)
    button_frame.pack(side=BOTTOM, pady=10)

    update_icon = PhotoImage(file="image/update.png")
    button_update = Button(button_frame, image=update_icon, bg="#5a95ff", bd=0, command=updateTask)
    button_update.image = update_icon
    button_update.pack(side=LEFT, padx=10)

    important_icon = PhotoImage(file="image/important.png")
    button_important = Button(button_frame, image=important_icon, bg="#5a95ff", bd=0, command=importantTask)
    button_important.image = important_icon
    button_important.pack(side=LEFT, padx=10)

    Delete_icon = PhotoImage(file="image/delete.png")
    Button(button_frame, image=Delete_icon, bd=0, command=deleteTask).pack(side=LEFT, padx=10)

    root.mainloop()

# Login window function
def login_window():
    login_root = Tk()
    login_root.title("Login")
    login_root.geometry("400x300")
    login_root.resizable(False, False)

    welcome_label = Label(login_root, 
                         text="Welcome to Daily-Dash", 
                         font=("Arial", 18, "bold"), 
                         fg="#ffffff",
                         bg="#3498db"
                        )
    welcome_label.pack(pady=50)

    password_label = Label(login_root, text="Enter Password", font="Arial 14")
    password_label.pack(pady=20)

    password_entry = Entry(login_root, font="Arial 14", show="*")
    password_entry.pack(pady=5)

    def check_password():
        if password_entry.get() == "Baloch":
            login_root.destroy()
            open_main_window()
        else:
            messagebox.showerror("Error", "Incorrect password!")

    login_button = Button(login_root, text="Login", font="Arial 14", command=check_password)
    login_button.pack(pady=20)

    login_root.mainloop()

# Start the login window
login_window()

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext, Button, Label, Entry, Frame, LabelFrame
import tkinter.messagebox as messagebox
from tkinter import filedialog

import configparser

from app_window.utils import center_window, shift_window
from data_process.committer import start_processing, item_start_processing
from db_interaction.DBConnection import login_connection

siAuthority = False    # set to True once login is successful
text_widget = None
main_window = None
channel_selection = None


def open_settings_window(config):
    """ open_settings_window() is used for creating SETTINGS on main window"""

    global siAuthority, main_window

    """ Setting 'SETTINGS' Window Screen """
    settings_window = tk.Toplevel(main_window)  # New settings window with main_window as parent
    settings_window.title("Settings")
    settings_window.geometry("720x600")  # 1.618 x 1 golden ratio
    settings_window.resizable(False, False)
    settings_window.transient(main_window)
    settings_window.grab_set()

    shift_window(main_window, settings_window, 30, 40)

    def browse_target_folder():
        """ browse_target_folder() is used for opening a folder dialog for the user to select a directory and selected folder path """
        # Target Folder
        folder_path = filedialog.askdirectory()
        importing_entry.delete(0, "end")  # target_entry
        importing_entry.insert(0, folder_path)  # target_entry
        settings_window.lift()

    def browse_processed_folder():
        """ browse_processed_folder() is used for opening a folder dialog for the user to select a directory and selected folder path """
        # Processed Folder
        folder_path = filedialog.askdirectory()
        processed_entry.delete(0, "end")
        processed_entry.insert(0, folder_path)
        settings_window.lift()

    def item_browse_target_folder():
        """ item_browse_target_folder() is used for items import to open a folder dialog for the user to select a directory and selected folder path """
        # Target Folder
        folder_path = filedialog.askdirectory()
        item_importing_entry.delete(0, "end")  # target_entry
        item_importing_entry.insert(0, folder_path)  # target_entry
        settings_window.lift()

    def item_browse_processed_folder():
        """ item_browse_processed_folder() is used for items import to open folder dialog for the user to select a directory and selected folder path """
        # Processed Folder
        folder_path = filedialog.askdirectory()
        item_processed_entry.delete(0, "end")
        item_processed_entry.insert(0, folder_path)
        settings_window.lift()

    """ Create Frames and Entry Boxes for the Following Groups as Below """
    # Directories group - Sales Order
    dir_label_frame = LabelFrame(settings_window, text="Sales Import Directories", padx=10, pady=10, font=("Arial Bold", 9))  # padding inside frame
    dir_label_frame.place(x=20, y=20, width=680, height=105)

    importing_label = Label(dir_label_frame, text="Target folder to import:")
    importing_label.place(x=0, y=0)
    importing_entry = Entry(dir_label_frame, width=70)  # width of entry box in characters
    importing_entry.place(x=140, y=3)
    importing_entry.insert(0, config['DIRECTORY']['importing'])
    importing_button = Button(dir_label_frame, text="Browse...", command=browse_target_folder)
    importing_button.place(x=580, y=0, width=70)

    processed_label = Label(dir_label_frame, text="Processed folder to store:")
    processed_label.place(x=0, y=35)
    processed_entry = Entry(dir_label_frame, width=70)
    processed_entry.place(x=140, y=38)
    processed_entry.insert(0, config['DIRECTORY']['processed'])
    processed_button = Button(dir_label_frame, text="Browse...", command=browse_processed_folder)
    processed_button.place(x=580, y=35, width=70)

    # Directories group - Items Import
    dir_label_frame = LabelFrame(settings_window, text="Items Import Directories", padx=10, pady=10,
                                 font=("Arial Bold", 9))  # padding inside frame
    dir_label_frame.place(x=20, y=140, width=680, height=105)

    item_importing_label = Label(dir_label_frame, text="Target folder to import:")
    item_importing_label.place(x=0, y=0)
    item_importing_entry = Entry(dir_label_frame, width=70)  # width of entry box in characters
    item_importing_entry.place(x=140, y=3)
    item_importing_entry.insert(0, config['ITEM DIRECTORY']['importing'])
    item_importing_button = Button(dir_label_frame, text="Browse...", command=item_browse_target_folder)
    item_importing_button.place(x=580, y=0, width=70)

    item_processed_label = Label(dir_label_frame, text="Processed folder to store:")
    item_processed_label.place(x=0, y=35)
    item_processed_entry = Entry(dir_label_frame, width=70)
    item_processed_entry.place(x=140, y=38)
    item_processed_entry.insert(0, config['ITEM DIRECTORY']['processed'])
    item_processed_button = Button(dir_label_frame, text="Browse...", command=item_browse_processed_folder)
    item_processed_button.place(x=580, y=35, width=70)

    # API group
    api_frame = LabelFrame(settings_window, text="API", padx=10, pady=10, font=("Arial Bold", 9))
    api_frame.place(x=20, y=260, width=680, height=105)

    api_url_label = Label(api_frame, text="URL:")
    api_url_label.place(x=0, y=0)
    api_url_entry = Entry(api_frame, width=35)
    api_url_entry.place(x=65, y=3)
    api_url_entry.insert(0, config['API']['url'])

    api_db_label = Label(api_frame, text="DB Name:")
    api_db_label.place(x=0, y=40)
    api_db_entry = Entry(api_frame, width=35)
    api_db_entry.place(x=65, y=40)
    api_db_entry.insert(0, config['API']['name'])

    api_username_label = Label(api_frame, text="Username:")
    api_username_label.place(x=300, y=0)
    api_username_entry = Entry(api_frame, width=35)
    api_username_entry.place(x=390, y=3)
    api_username_entry.insert(0, config['API']['username'])

    api_password_label = Label(api_frame, text="Password:")
    api_password_label.place(x=300, y=40)
    api_password_entry = Entry(api_frame, width=35, show="*")
    api_password_entry.place(x=390, y=40)
    api_password_entry.insert(0, config['API']['password'])

    # ERP Connection group
    erp_label_frame = LabelFrame(settings_window, text="ERP Connection", padx=10, pady=10, font=("Arial Bold", 9))
    erp_label_frame.place(x=20, y=380, width=220, height=140)

    url_label = Label(erp_label_frame, text="URL:")
    url_label.place(x=0, y=0)
    url_entry = Entry(erp_label_frame, width=20)
    url_entry.place(x=60, y=3)
    url_entry.insert(0, config['DATABASE']['url'])

    port_label = Label(erp_label_frame, text="Port:")
    port_label.place(x=0, y=35)
    port_entry = Entry(erp_label_frame, width=20)
    port_entry.place(x=60, y=38)
    port_entry.insert(0, config['DATABASE']['port'])

    db_label = Label(erp_label_frame, text="DB Name:")
    db_label.place(x=0, y=70)
    db_entry = Entry(erp_label_frame, width=20)
    db_entry.place(x=60, y=73)
    db_entry.insert(0, config['DATABASE']['name'])

    # LocalDB Connection group
    localdb_label_frame = LabelFrame(settings_window, text="LocalDB Connection", padx=10, pady=10, font=("Arial Bold", 9))
    localdb_label_frame.place(x=250, y=380, width=220, height=140)

    local_url_label = Label(localdb_label_frame, text="URL:")
    local_url_label.place(x=0, y=0)
    local_url_entry = Entry(localdb_label_frame, width=20)
    local_url_entry.place(x=60, y=3)
    local_url_entry.insert(0, config['LOCAL DATABASE']['url'])

    local_port_label = Label(localdb_label_frame, text="Port:")
    local_port_label.place(x=0, y=35)
    local_port_entry = Entry(localdb_label_frame, width=20)
    local_port_entry.place(x=60, y=38)
    local_port_entry.insert(0, config['LOCAL DATABASE']['port'])

    local_db_label = Label(localdb_label_frame, text="DB Name:")
    local_db_label.place(x=0, y=70)
    local_db_entry = Entry(localdb_label_frame, width=20)
    local_db_entry.place(x=60, y=73)
    local_db_entry.insert(0, config['LOCAL DATABASE']['name'])

    # User group
    login_label_frame = LabelFrame(settings_window, text="User", padx=10, pady=10, font=("Arial Bold", 9))
    login_label_frame.place(x=480, y=380, width=220, height=140)

    username_label = Label(login_label_frame, text="Username:")
    username_label.place(x=0, y=0)
    username_entry = Entry(login_label_frame, width=20)
    username_entry.place(x=65, y=3)
    username_entry.insert(0, config['USER']['username'])

    password_label = Label(login_label_frame, text="Password:")
    password_label.place(x=0, y=35)
    password_entry = Entry(login_label_frame, width=20, show="*")
    password_entry.place(x=65, y=38)
    password_entry.insert(0, config['USER']['password'])

    def click_login():
        """ click_login() is used for determining if ERP Connection connects successfully based on user's input """
        global siAuthority

        erp_info = {
            'url': url_entry.get(),
            'port': port_entry.get(),
            'database': db_entry.get(),
            'username': username_entry.get(),
            'password': password_entry.get()
        }

        if login_connection(erp_info):
            messagebox.showinfo('Success', 'Connection successful!')
            siAuthority = True
            update_logged_in_label()

        else:
            messagebox.showerror('Failure', 'Connection failed!')
            siAuthority = False
            update_logged_in_label()

    def click_localDB_login():
        """ click_localDB_login() is used for determining if LocalDB connects successfully based on user's input """
        global siAuthority

        erp_info = {
            'url': local_url_entry.get(),
            'port': local_port_entry.get(),
            'database': local_db_entry.get(),
            'username': username_entry.get(),
            'password': password_entry.get()
        }

        if login_connection(erp_info):
            messagebox.showinfo('Success', 'Connection Successful!')
            siAuthority = True
            update_logged_in_label()

        else:
            messagebox.showerror('Failure', 'Connection Failed!')
            siAuthority = False
            update_logged_in_label()

    def update_logged_in_label():
        """ update_logged_in_label() is used for checking if user clicked 'Login ERP' or 'Login Local' buttons
            and logged in successfully with given username and password
        """

        global siAuthority, logged_in_label

        if siAuthority:
            logged_in_label.config(text=f"Login with {username_entry.get()}", fg="black")
        # else:
            # logged_in_label.config(text="Login Required.", fg="red")

    def click_save():
        """ click_save() is used for saving all user's input to 'config.ini' file """

        config = configparser.ConfigParser()
        config.read('config.ini')

        xautomatic = config['PROCESS']['automatic']
        xinterval = config['PROCESS']['interval']
        xmode = config['DEBUG']['mode']

        config['DIRECTORY'] = {
            'importing': importing_entry.get(),
            'processed': processed_entry.get()
        }
        config['DATABASE'] = {
            'url': url_entry.get(),
            'port': port_entry.get(),
            'name': db_entry.get()
        }
        config['LOCAL DATABASE'] = {
            'url': local_url_entry.get(),
            'port': local_port_entry.get(),
            'name': local_db_entry.get()
        }
        config['API'] = {
            'url': api_url_entry.get(),
            'name': api_db_entry.get(),
            'username': api_username_entry.get(),
            'password': api_password_entry.get()
        }
        config['USER'] = {
            'username': username_entry.get(),
            'password': password_entry.get()
        }
        config['PROCESS'] = {
            'automatic': xautomatic,
            'interval': xinterval
        }
        config['ITEM DIRECTORY'] = {
            'importing': item_importing_entry.get(),
            'processed': item_processed_entry.get()
        }
        config['DEBUG'] = {
            'mode': xmode
        }

        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        messagebox.showinfo('Success', 'Settings saved successfully!')

    def update_config_data():
        """ update_config_data() is used for updating values in 'config.ini' when user makes changes """

        config = configparser.ConfigParser()
        config.read('config.ini')

        # Directories Group
        importing_entry.delete(0, "end")
        importing_entry.insert(0, config['DIRECTORY']['importing'])
        processed_entry.delete(0, "end")
        processed_entry.insert(0, config['DIRECTORY']['processed'])

        item_importing_entry.delete(0, "end")
        item_importing_entry.insert(0, config['ITEM DIRECTORY']['importing'])
        item_processed_entry.delete(0, "end")
        item_processed_entry.insert(0, config['ITEM DIRECTORY']['processed'])

        # API Group
        api_url_entry.delete(0, "end")
        api_url_entry.insert(0, config['API']['url'])
        api_db_entry.delete(0, "end")
        api_db_entry.insert(0, config['API']['name'])
        api_username_entry.delete(0, "end")
        api_username_entry.insert(0, config['API']['username'])
        api_password_entry.delete(0, "end")
        api_password_entry.insert(0, config['API']['password'])

        # ERP Connection Group
        url_entry.delete(0,"end")
        url_entry.insert(0, config['DATABASE']['url'])
        port_entry.delete(0, "end")
        port_entry.insert(0, config['DATABASE']['port'])
        db_entry.delete(0, "end")
        db_entry.insert(0, config['DATABASE']['name'])

        # LocalDB Connection Group
        local_url_entry.delete(0, "end")
        local_url_entry.insert(0, config['LOCAL DATABASE']['url'])
        local_port_entry.delete(0, "end")
        local_port_entry.insert(0, config['LOCAL DATABASE']['port'])
        local_db_entry.delete(0, "end")
        local_db_entry.insert(0, config['LOCAL DATABASE']['name'])

        # User Group
        username_entry.delete(0, "end")
        username_entry.insert(0, config['USER']['username'])
        password_entry.delete(0, "end")
        password_entry.insert(0, config['USER']['password'])

    """ Create Buttons in SETTINGS """
    # Login Button for ERP Connection
    login_button = Button(settings_window, text="Login ERP", command=click_login, width=10, height=2)
    login_button.place(x=100, y=540)

    # Login Button for LocalDB
    login_localDB_button = Button(settings_window, text="Login Local", command=click_localDB_login, width=11, height=2)
    login_localDB_button.place(x=320, y=540)

    # Save Button
    save_button = Button(settings_window, text="Save", command=click_save, width=10, height=2)
    save_button.place(x=520, y=540)

    # Exit Button
    exit_button = Button(settings_window, text="Exit", command=settings_window.destroy, width=10, height=2)
    exit_button.place(x=620, y=540)

    # Update config.ini stored data values after save_button pressed
    update_config_data()

    def on_settings_window_close():
        """ on_settings_window_close() is used for closing SETTINGS window after user clicked EXIT button"""
        main_window.deiconify()  # restore main window
        settings_window.destroy()  # close settings window

    settings_window.protocol("WM_DELETE_WINDOW", on_settings_window_close)

def click_start():
    """ click_start() is used for running Sales Import Importer Program """

    '''
    global siAuthority

    if not siAuthority:
        text_widget.tag_configure("warning_color", foreground="red")
        text_widget.insert(tk.END, "Warning: Cannot proceed. Login is required at Settings.\n", "warning_color")
        text_widget.see(tk.END)
        return
    '''

    global channel_selection
    sales_channel = channel_selection

    # Show Warning message if user has NOT selected any sales channel
    if sales_channel == None:
        warning_message = messagebox.showwarning(title="Warning", message="Please Select Sales Channel")
        return None

    # Ask user if user has selected the correct sales channel
    confirmation_message = messagebox.askyesno("Sales Channel", f"Have you selected {sales_channel}?")
    if confirmation_message:
        # User clicked "Yes"
        pass
    else:
        # User clicked "No"
        return None

    config = configparser.ConfigParser()
    config.read('config.ini')

    start_processing(config, on_message, sales_channel)

def click_start_item_import():

    config = configparser.ConfigParser()
    config.read('config.ini')

    item_start_processing(config, on_message)


def on_message(message):
    """ on_message() is used for showing message in main window scrollable text window widget frame """
    text_widget.insert(tk.END, message)
    text_widget.see(tk.END)


def click_exit():
    """ click_exit() is used for stop running Sales Import Importer Program """
    answer = messagebox.askyesno("Confirmation", "Are you sure to exit?")
    if answer:
        main_window.destroy()


def open_main_window(config):
    """ open_main_window() is used for opening a main window screen """
    global siAuthority, text_widget, main_window, logged_in_label, selection

    def update_logged_in_label():
        """ update_logged_in_label() is used for updating logged in status """
        if siAuthority:
            logged_in_label.config(text=f"Login with {config['USER']['username']}", fg="black")
        # else:
            # logged_in_label.config(text="Login Required.", fg="red")

    """ Setting Main Window Screen """
    main_window = tk.Tk()
    main_window.title("Sales Data Importer")
    main_window.geometry("647x400")
    main_window.resizable(False, False)
    center_window(main_window)

    # Scrollable text window widget
    text_widget = scrolledtext.ScrolledText(main_window, width=65, height=18, font="Monaco 11")
    text_widget.place(x=20, y=70)

    # text label for selecting sales channel
    sales_channel_label = Label(main_window, text="* Select Sales Channel *", fg="black")
    sales_channel_label.place(x=315, y=15)

    def dropdown_select(event):
        """ dropdown_select() is used for selecting sales channel that user picked """
        global channel_selection
        channel_selection = dropdown.get()

    """ Sales Channel List """
    # Dropdown sales channel list
    dropdown = ttk.Combobox(state="readonly", width=25, values=["FASHIONGO URBANISTA", "FASHIONGO OUTLET", "LASHOWROOM"])
    dropdown.place(x=290, y=38)

    # Bind the selected value changes
    global channel_selection
    channel_selection = None
    dropdown.bind('<<ComboboxSelected>>', dropdown_select)

    # Settings Buttons
    settings_button = Button(main_window, text="Settings", command=lambda: open_settings_window(config), width=10, height=2, font='sans 8 bold', fg="black")
    settings_button.place(x=20, y=20)

    # Start Buttons for Sales Import
    start_button = Button(main_window, text="Sales Start", command=click_start, width=10, height=2, font='sans 8 bold', fg="green")
    start_button.place(x=470, y=20)

    # Start Buttons for Items Import
    start_button_item = Button(main_window, text="Items Start", command=click_start_item_import, width=12, height=2, font='sans 8 bold', fg="blue")
    start_button_item.place(x=110, y=20)

    # Exit Buttons
    exit_button = Button(main_window, text="Exit", command=click_exit, width=10, height=2, font='sans 9 bold', fg="red")
    exit_button.place(x=555, y=20)

    # Logged-in label
    logged_in_label = Label(main_window, text="", fg="green", font="Arial 12 bold")
    logged_in_label.place(x=120, y=28)

    update_logged_in_label()  # initial update of the logged-in label

    main_window.mainloop()


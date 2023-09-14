from tkinter import *
import tkinter as tk
import tkinter.messagebox as messagebox
from app_window.utils import debug_print
from app_window.utils import center_window
from db_interaction.DBConnection import Local_DB


def matching_product_id_window(product_name, product_color, color_list, channel):
    """ matching_product_id_window() is used for matching style No. and Color names from user's selection
        and return to match correct product ID and Style No.
    """

    def submit():
        """ submit() is used for returning Product_id and Style # as tuple after user clicked the 'SUBMIT' button """
        debug_print("Start: submit()")
        window.return_value1 = radiobutton.get().strip("()").split(" ")[0]  # extract only product_id
        window.return_value2 = radiobutton.get().strip("()").split(" ")[1]  # extract only Style No.
        window.quit()  # destroy mismatch popup window
        debug_print(f"Submit Value1:{window.return_value1}")
        debug_print(f"Submit Value2:{window.return_value2}")

        return window.return_value1, window.return_value2  # return (product_id, Style No.)

    """ Setting Matching Product Popup Screen """
    window = tk.Toplevel()  # create a window on top of all other windows
    window.title("Matching Product")
    window.geometry("450x650")
    window.minsize(450, 680)  # set minimum window size
    window.maxsize(450, 860)  # set maximum window size
    center_window(window)

    def copy_text(text):
        """ copy_text() is used for copying text of Style # and Color in Entry Box """
        copytext = StringVar()
        copytext.set(text)
        text_entry = tk.Entry(message_frame, width=36, textvariable=copytext, bd=0, justify="center", state="readonly", background="lightgrey", font=("Arial Bold", 10))
        text_entry.pack(padx=5, pady=5)

    """ Create Frame to Show Style # and Color from Processing Excel Data """
    message_frame = tk.Frame(window, highlightbackground="dim gray", highlightthickness=2, background="lightgrey")
    message_frame.pack(padx=30, pady=30)

    #  Title Label
    excel_data = "       < From Processing Excel Data >       "
    message_label = tk.Label(message_frame, text=excel_data, background="lightgrey")
    message_label.pack(padx=5, pady=5)

    #  Style No. Label
    style_number = "Style #"
    message_label = tk.Label(message_frame, text=style_number, background="lightgrey", font=("Arial Bold", 9))
    message_label.pack()
    copy_text(product_name)

    #  Color Label
    color = "Color"
    message_label = tk.Label(message_frame, text=color, background="lightgrey", font=("Arial Bold", 9))
    message_label.pack()
    copy_text(product_color)

    def search_submit():
        """ search_submit() is used for returning Product_id and Style # as tuple after
            user clicked the 'SUBMIT' button and there is also 'SEARCH' button existed
        """
        debug_print("Start: Search()")
        window.return_value1 = window.new_button.get().strip("()").split(" ")[0]  # extract only product_id
        window.return_value2 = window.new_button.get().strip("()").split(" ")[1]  # extract only Style No.
        window.quit()
        debug_print(f"Submit Value 1:{window.return_value1}")
        debug_print(f"Submit Value 2:{window.return_value2}")

        return window.return_value1, window.return_value2  # return (product_id, Style No.)

    def clear_radio_buttons(frame):
        """ clear_radio_buttons() is used for resetting radio button selections inside of frame each time
            when user clicked search button
        """
        for widget in frame.winfo_children():
            widget.destroy()

    def search_entry_box():
        """ search_entry_box() is used for searching correct Style # based on user's input in entry box """

        debug_print("Start: search_entry_box()")
        window.return_value_entry_box = entry_box.get()  # Store Style No. that user typed
        debug_print(f" Search entry_box value:{window.return_value_entry_box}")

        # FashionGo Urbanista
        if channel == 'FASHIONGO':
            local_db = Local_DB()
            local_db.connect()
            params = ('%' + window.return_value_entry_box + '%',)
            query = "select product_id, name, color from product_matching where name like name like %s"
            result = local_db.query(query, params)
            local_db.disconnect()
            if result:  # when Style # FOUND from DB
                clear_radio_buttons(canvas_frame)  # reset radio button selections
                window.new_button = create_radio_buttons(canvas_frame, result)  # Create radio button selections based on style #
                return window.new_button
            else:  # when Style # NOT found from DB
                messagebox.showerror("Notice", "Cannot find Style Number, Please type again")
                window.lift()

        # LAShowroom
        if channel == 'LASHOWROOM':
            local_db = Local_DB()
            local_db.connect()
            params = ('%' + window.return_value_entry_box + '%',)
            query = "select product_id, name, color from product_matching_lashowroom where name like %s"
            result = local_db.query(query, params)
            local_db.disconnect()
            if result:
                clear_radio_buttons(canvas_frame)
                window.new_button = create_radio_buttons(canvas_frame, result)
                return window.new_button
            else:
                messagebox.showerror("Notice", "Cannot find Style Number, Please type again")
                window.lift()

        # FashionGo Outlet
        if channel == 'FASHIONGO OUTLET':
            local_db = Local_DB()
            local_db.connect()
            params = ('%' + window.return_value_entry_box + '%',)
            query = "select product_id, name, color from product_matching_outlet where name like %s"
            result = local_db.query(query, params)
            local_db.disconnect()
            if result:
                clear_radio_buttons(canvas_frame)
                window.new_button = create_radio_buttons(canvas_frame, result)
                return window.new_button
            else:
                messagebox.showerror("Notice", "Cannot find Style Number, Please type again")
                window.lift()

    if color_list:  # Skip 'Search' Operation if Style # matches from LocalDB
        count = 0
        debug_print(f"Color List:{color_list}")
        pass

    else:  # Create 'Search' Entry Box if Style # does NOT match from LocalDB
        count = 1
        window.return_value_entry_box = None
        entry_box = create_entry_box(window)  # Create entry box for typing Style No.

        # Create 'Search' Button for Calling search_entry_box()
        search_button_entry_box = tk.Button(window, text="Search", command=search_entry_box, background="lightgrey")
        search_button_entry_box.pack(padx=20, pady=20)

    """ Create Frame to Show Color Lists & Scroll Bar """
    label_frame = LabelFrame(window, text="Select Correct Color Name")
    label_frame.pack(anchor='center')

    # Create a Canvas widget
    canvas = tk.Canvas(label_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a Scrollbar widget
    scrollbar = tk.Scrollbar(label_frame, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the Canvas widget to use the Scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a Frame inside the Canvas
    canvas_frame = tk.Frame(canvas)

    # Add radiobutton to the Frame
    radiobutton = create_radio_buttons(canvas_frame, color_list)

    # Configure the Frame as the scrollable region
    canvas.create_window((0, 0), window=canvas_frame, anchor='nw')

    def update_scroll_region(event):
        """ update_scroll_region() is used for update the Canvas scroll region """
        canvas.configure(scrollregion=canvas.bbox('all'))

    # Bind the update_scroll_region function to the Frame resize event
    canvas_frame.bind('<Configure>', update_scroll_region)

    empty_text = ""   # Make an Empty Space
    create_empty_label(window, empty_text)

    """ Submit Buttons """
    if count == 1:  # if Style No. does NOT match from DB
        # Create Submit button
        submit_button = tk.Button(window, text="Submit", command=search_submit, background="lightgrey")
        submit_button.pack()

    else:  # if Style No. DOES match from DB
        # Create Submit button
        submit_button = tk.Button(window, text="Submit", command=submit, background="lightgrey")
        submit_button.pack()

    """ Default Return Values """
    window.return_value1 = None  # Set default return value 1 (product_id)
    window.return_value2 = None  # Set default return value 2 (Style No.)

    """ End Program """
    window.mainloop()  # tells Python to run the Tkinter event loop
    window.destroy()  # terminates the mainloop process and destroys all the widgets inside the window

    return window.return_value1, window.return_value2  # (product_id, Style No.)


def create_radio_buttons(canvas_frame, color_list):
    """ create_radio_buttons() is used for creating radio buttons of all possible color lists based on Style # """

    selected_option = tk.StringVar()  # Store color_list as string
    selected_option.set("None")  # deselect all radio buttons before user select something

    for row in color_list:
        colors = row
        str_colors = str(colors)  # text = delete first and last parentheses and comma characters from 'colors'
        radio_var = tk.Radiobutton(canvas_frame, text=str_colors.lstrip(str_colors[0]).rstrip(str_colors[-1]).replace(",", "").replace("'", ""), variable=selected_option, value=colors)
        radio_var.pack(anchor='w', pady=3)

    return selected_option  # return radio button value that user picked


def create_entry_box(window):
    """ create_entry_box() is used for creating entry box to type Style # from user """

    input_label = tk.Label(window, text="Type Correct Style #")
    input_label.pack(padx=3, pady=3)

    input_value = tk.StringVar()  # Store input values as string
    input_entry = tk.Entry(window, textvariable=input_value)
    input_entry.pack()

    return input_value  # return input values from user typed


def create_empty_label(window, empty_text):
    """ create_empty_label() is used for creating empty spaces """

    message_label = tk.Label(window, text=empty_text)
    message_label.pack()



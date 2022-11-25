# Student Name - Rayan Aryaan
# Class        - DPS, XII/E
# Roll No      - 19

# importing python packages
import os                               # file, folder handling.
import tkinter as  tk                   # GUI
import tkinter.messagebox as messagebox # dialog box handling
from tkinter import scrolledtext        # display suggested medicines
import re                               # Regular expression to validate input
import datetime                         # Timestamp

# Global variables
# folder name to keep all patient records (Aadhar NO based file logging)
input_folder_name = "records"
record_file_extn = ".rec"
record_field_seperator = ":"
tk_main_window = None
# close main window
def close_mainwnd():
    global tk_main_window
    if tk_main_window is not None:
        tk_main_window.destroy()
        tk_main_window = None

# read patients record from file
# (local txt files are used to manage records)
# File record format:
# <Name>, <Address>, <Age>, <mobile>, <aadhar no>
# Treatment details
# <Date>, <Symptoms>, <Prescribed Medicine details>
def read_patients_records(patient_record_file_name):
    # Opening partient record file
    print('Opening patient record - {}'.format(patient_record_file_name))
    patient_record_file = open(patient_record_file_name)
    if patient_record_file is not None:
        # file open successfully
        pass
    pass

# retrieve patient name and update name entry info
def update_patient_info(name_ent, aadhar_no:str, show_record_flag:bool = False):
    if len(aadhar_no) != 12:
        messagebox.showinfo('Input Error', "Please enter 12 digit aadhar no.")
    name, _, mobile_no = retrieve_patient_information(aadhar_no)
    print('Retrive info for aadhar - {} -> name - {}, mobile no - {}'.format(aadhar_no, name, mobile_no))
    if name is None:
        name = "N/A"
    # twinker entry will NOT update contained if it's read ONLY.
    # to update, first change configuration to normal then update and disable again.
    name_ent.config(state=tk.NORMAL)
    name_ent.delete(0, tk.END)
    name_ent.insert(tk.END, name)
    name_ent.config(state=tk.DISABLED)
    if show_record_flag:
        show_patient_history(aadhar_no)

# Initialize records folder structure
def initialize_database():
    if os.path.isdir(input_folder_name):
        # input folder doesn't exist
        for folder_name in os.listdir(input_folder_name):
            if os.path.isdir(folder_name):
                read_patients_records(folder_name)
    else:
        # create input record room
        os.makedirs(input_folder_name)
    pass

# function to validate number entry
def only_numbers(char):
    return char.isdigit()

# Display proposed treatment details
def display_diagnosis(patient_name, treatments_list, important_msg = ""):
    print('Showing treatment details')
    print('Name - {}, Treatment - {}'.format(patient_name, treatments_list))
    tk_display_diag_window = tk.Tk()
    frame = tk.Frame(tk_display_diag_window, width=600, height=300, pady=5)
    frame.pack(pady=5, padx=5)
    tk_display_diag_window.title('Suggested Treatment')
    row_count = 0
    name_var = tk.StringVar(frame)
    name_var.set(patient_name)
    label = tk.Label(frame, text= "Name: ", font='arial 15 bold')
    label.grid(row = row_count, column = 0, sticky = tk.W, padx = 2, pady = 2)
    name_entry = tk.Entry(frame, state=tk.DISABLED, textvariable=name_var)
    name_entry.grid(row=row_count, column=1, padx=2, pady=2)
    row_count += 1

    label = tk.Label(frame, text="Medicine: ", font='arial 15 bold')
    label.grid(row=row_count, column=0, sticky=tk.W, padx=2, pady=2)
    treatment_text = scrolledtext.ScrolledText(frame, width=100, height=10, wrap=tk.WORD,
                                                font='arial 10 bold', state=tk.NORMAL)
    treatment_text.grid(row=row_count, column=1, padx=2, pady=2)
    for treatment in treatments_list:
        treatment_text.insert(tk.END, treatment)
        treatment_text.insert(tk.END, "\n")
    treatment_text.config(state=tk.DISABLED)
    row_count += 1
    if len(important_msg) > 0:
        label = tk.Label(frame, text="Message: ", font='arial 15 bold', background='red')
        label.grid(row=row_count, column=0, sticky=tk.W, padx=2, pady=2)
        treatment_text = scrolledtext.ScrolledText(frame, width=100, height=2, wrap=tk.WORD,
                                                    font='arial 10 bold', state=tk.NORMAL, background='light grey')
        treatment_text.grid(row=row_count, column=1, padx=2, pady=2)
        treatment_text.insert(tk.END, important_msg)
        treatment_text.config(state=tk.DISABLED)
        row_count += 1

    label = tk.Label(frame, text="Note: ", font='arial 15 bold')
    label.grid(row=row_count, column=0, sticky=tk.W, padx=2, pady=2)
    treatment_text = scrolledtext.ScrolledText(frame, width=100, height=2, wrap=tk.WORD,
                                                font='arial 10 bold', state=tk.NORMAL, background='grey')
    treatment_text.grid(row=row_count, column=1, padx=2, pady=2)
    msg = "Please note, this service is to address immediate problems. " \
          "If problem is not reduced, please contact nearby hospital/doctor immediately."

    treatment_text.insert(tk.END, msg)
    treatment_text.config(state=tk.DISABLED)
    row_count += 1

    ok_button = tk.Button(frame, text="Ok", font="arial 10 bold", width=10,
                            command=tk_display_diag_window.destroy) # Close the window
    ok_button.grid(row=row_count, column=1, padx=2, pady=2)
    tk_display_diag_window.resizable(False, False)
    tk_display_diag_window.mainloop()

# Generate record file name (aadhar based)
def generate_record_filename(aadhar_no:str):
    rec_file_name = input_folder_name + os.sep + aadhar_no + record_file_extn
    print("Record filename: {}".format(rec_file_name))
    return rec_file_name;

# retrieve patient information
def retrieve_patient_information(aadhar_no:str):
    rec_filename = generate_record_filename(aadhar_no)
    print("Searching patient information with aadhar no - {}".format(aadhar_no))
    if os.path.exists(rec_filename):
        file = open(rec_filename, "r")
        if file is not None:
            rec_data = file.readline()
            print('Read - {}'.format(rec_data))
            # parse the record.
            data_split = rec_data.split(record_field_seperator)
            print('Read split - {}, no of records - {}'.format(data_split, len(data_split)))
            file.close()
            # name, mobile no
            return data_split[1], data_split[3], data_split[4]
        else:
            print('Failed to read {} file.'.format(rec_filename))

    print("Patient information NOT found with aadhar no - {}".format(aadhar_no))
    return None, None, None

# process registration request
def process_registration_request(main_wnd, name, addr, age_yrs, age_months, mobile, aadhar):
    print("Registration Request: name - {}, addr - {}, age - {} yrs {} months, mob - {}, aadhar - {}"
          .format(name, addr, age_yrs, age_months, mobile, aadhar))
    # input validation.
    if len(aadhar) != 12:
        length = len(aadhar)
        messagebox.showinfo("Wrong Input",
                            "Please enter 12 digit aadhar no. Current len - {}".format(length))
        return
    if len(mobile) != 10:
        length = len(mobile)
        messagebox.showinfo("Wrong Input",
                            "Please enter 10 digit mobile no. Current len - {}".format(length))
        return
    age = int(age_yrs) * 12 + int(age_months)
    if age <= 0 or age >= 150 *12:
        messagebox.showinfo("Wrong Input", "Please enter valid age between 1 mth to 150 yrs")
        return
    regex_name = re.compile(r'^([a-z]+)( [a-z]+)*( [a-z]+)*$', re.IGNORECASE)
    if(not regex_name.search(name)):
        messagebox.showinfo("Wrong Input", "Please enter valid name.")
        return
    if len(addr) <= 0:
        messagebox.showinfo("Wrong Input", "Please enter valid address. can't be null.")
        return
    # check for duplicate aadhar entry.
    rec_filename = generate_record_filename(aadhar)
    if not os.path.exists(rec_filename):
        print("New user. Let's create.")
        main_wnd.destroy()
        file = open(rec_filename, "w")
        if file is not None:
            print('{} file created successfully'.format(rec_filename))
            data = "{}:{}:{}:{}:{}\n".format(aadhar, name, addr, age, mobile)
            print('Writing - {}'.format(data))
            file.write(data)
            file.close()
            messagebox.showinfo("Registration Request", "User name - {} added successfully".format(name))
        else:
            print('Failed to create {} file.'.format(rec_filename))
            messagebox.showinfo("Registration Request", "Failed to create user name - {}".format(name))
    else:
        # Patient already exist
        messagebox.showinfo("Registration Request", "Patient already registered with same aadhar no - {}".format(aadhar))


# Registrer patient
def patient_registration():
    # display form
    print('Showing partient registration form.')
    tk_registration_window = tk.Tk()
    validation = tk_registration_window.register(only_numbers)
    frame = tk.Frame(tk_registration_window, width=600, height=300, pady=5)
    frame.pack(pady=5, padx=5)
    row_count = 0
    tk_registration_window.title('Register patient')
    label = tk.Label(frame, text= "Name: ", font='arial 15 bold')
    label.grid(row = row_count, column = 0, sticky = tk.W, padx = 2, pady = 2)
    name_entry = tk.Entry(frame)
    name_entry.grid(row=row_count, column=1, padx=2, pady=2)
    row_count += 1
    address_label = tk.Label(frame, text="Address: ", font="arial 15 bold")
    address_label.grid(row=row_count, column=0, padx=2, pady=2, sticky = tk.W)
    address_entry = tk.Entry(frame)
    address_entry.grid(row=row_count, column=1, padx=2, pady=2)
    row_count += 1
    label = tk.Label(frame, text="Age: (Yrs)", font="arial 15 bold")
    label.grid(row=row_count, column=0, padx=2, pady=2, sticky = tk.W)
    age_yrs_entry = tk.Entry(frame, validate="key", validatecommand=(validation, '%S'))
    age_yrs_entry.insert(tk.END, "0")
    age_yrs_entry.grid(row=row_count, column=1, padx=2, pady=2)

    label = tk.Label(frame, text="Mth(s):", font="arial 15 bold")
    label.grid(row=row_count, column=2, padx=2, pady=2, sticky = tk.W)
    age_months_entry = tk.Entry(frame, validate="key", validatecommand=(validation, '%S'), width=5)
    age_months_entry.insert(tk.END, "0")
    age_months_entry.grid(row=row_count, column=3, padx=2, pady=2)

    row_count += 1

    mobile_label = tk.Label(frame, text="Mobile No: ", font="arial 15 bold")
    mobile_label.grid(row=row_count, column=0, padx=2, pady=2, sticky = tk.W)
    mobile_entry = tk.Entry(frame, validate="key", validatecommand=(validation, '%S'))
    mobile_entry.grid(row=row_count, column=1, padx=2, pady=2)
    aadhar_label = tk.Label(frame, text="Aadhar No: ", font="arial 15 bold")
    row_count += 1
    aadhar_label.grid(row=row_count, column=0, padx=2, pady=2, sticky = tk.W)
    aadhar_entry = tk.Entry(frame, validate="key", validatecommand=(validation, '%S'))
    aadhar_entry.grid(row=row_count, column=1, padx=2, pady=2)
    row_count += 1
    register_button = tk.Button(frame, text="Register", font="arial 10 bold",
                        command=(lambda name=name_entry,
                                 addr=address_entry,
                                 age_yrs=age_yrs_entry,
                                 age_months=age_months_entry,
                                 mobile=mobile_entry,
                                 aadhar=aadhar_entry,
                                 main_wnd=tk_registration_window:
                                 process_registration_request(main_wnd, name.get().strip(),
                                                              addr.get().strip(),
                                                              age_yrs.get().strip(),
                                                              age_months.get().strip(),
                                                              mobile.get().strip(),
                                                              aadhar.get().strip())))
    register_button.grid(row=row_count, column=1, padx=2, pady=2)
    back_button = tk.Button(frame, text="Back", font="arial 10 bold",
                            command=tk_registration_window.destroy) # Close the window
    back_button.grid(row=row_count, column=2, padx=2, pady=2)
    tk_registration_window.resizable(False, False)
    tk_registration_window.mainloop()

# retrieve treatment detail list
def retrieve_treatment_detail_list(aadhar_no):
    treatment_rec_list = []
    rec_file_name = generate_record_filename(aadhar_no)
    if os.path.exists(rec_file_name):
        # file exist.
        file = open(rec_file_name, "r")
        if file is not None:
            # ignore first line (patient personal record)
            file.readline()
            rec_data = file.readline()
            while rec_data is not None and len(rec_data) > 0:
                print('Read - {}'.format(rec_data))
                # parse the record.
                data_split = rec_data.split(record_field_seperator)
                treatment_rec_list.insert(len(treatment_rec_list), data_split)
                rec_data = file.readline().strip()
            file.close()
    # return empty list
    return treatment_rec_list

# Not supporting patient record update feature
def show_patient_history(aadhar_no:str = ""):
    # First take addhar no as input
    # Search records and display those records.
    print('Showing patient treatment history.')
    row_count = 0
    tk_patient_history_window = tk.Tk()
    validation = tk_patient_history_window.register(only_numbers)
    frame = tk.Frame(tk_patient_history_window, width=600, height=300, pady=5)
    frame.pack(pady=5, padx=5)
    tk_patient_history_window.title('Patient Treatment History')
    label = tk.Label(frame, text= "Aadhar No: ", font='arial 15 bold')
    label.grid(row = row_count, column = 0, sticky = tk.W, padx = 2, pady = 2)
    aadhar_entry = tk.Entry(frame, validate="key", validatecommand=(validation, '%S'))
    aadhar_entry.grid(row=row_count, column=1, padx=2, pady=2)
    retrieve_button = None
    if len(aadhar_no) > 0:
        # update aadhar no.
        aadhar_entry.insert(tk.END, aadhar_no)
        aadhar_entry.config(state=tk.DISABLED)
    else:
        # retrieve is allowed
        retrieve_button = tk.Button(frame, text="Retrieve", font="arial 10 bold")
        retrieve_button.grid(row=row_count, column=2, padx=2, pady=2)
    row_count += 1
    name_label = tk.Label(frame, text="Name:", font="arial 15 bold")
    name_label.grid(row=row_count, column=0, padx=2, pady=2)

    name_entry = tk.Entry(frame)
    name_entry.grid(row=row_count, column=1, padx=2, pady=2)
    name_entry.config(state=tk.DISABLED)
    if len(aadhar_no) <= 0:
        # retrieve is allowed
        back_button = tk.Button(frame, text="Back", font="arial 10 bold",
                                command=tk_patient_history_window.destroy, width=7)
        back_button.grid(row=row_count, column=2, padx=2, pady=2)

    row_count += 1
    if retrieve_button is not None:
        retrieve_button.config(command=(lambda name_ent=name_entry,
                                        aadhar_ent=aadhar_entry
                                        :update_patient_info(name_ent, aadhar_ent.get().strip(), True)))
    if len(aadhar_no) > 0:
        update_patient_info(name_entry, aadhar_no)
        name_label = tk.Label(frame, text="Date", font="arial 15 bold underline")
        name_label.grid(row=row_count, column=0, padx=2, pady=2)
        name_label = tk.Label(frame, text="Symptoms", font="arial 15 bold underline")
        name_label.grid(row=row_count, column=1, padx=2, pady=2)
        name_label = tk.Label(frame, text="Treatment", font="arial 15 bold underline")
        name_label.grid(row=row_count, column=2, padx=2, pady=2)
        name_label = tk.Label(frame, text="Message", font="arial 15 bold underline")
        name_label.grid(row=row_count, column=3, padx=2, pady=2)
        row_count += 1
        treatment_record_list = retrieve_treatment_detail_list(aadhar_no)
        for record in treatment_record_list:
            index = 0
            for y in record:
                width = 25
                if index == 2: # Treatment (need more space)
                    width = 75
                elif index == 1 or index == 3: # symptoms/message
                    width = 50
                entry = tk.Entry(frame, width=width)
                entry.grid(row=row_count, column=index, padx=2, pady=2)
                entry.insert(tk.END, record[index])
                entry.config(state=tk.DISABLED)
                index += 1
            row_count += 1
        ok_button = tk.Button(frame, text="Ok", font="arial 10 bold", width=10,
                                command=tk_patient_history_window.destroy) # Close the window
        ok_button.grid(row=row_count, column=1, padx=2, pady=2)
    tk_patient_history_window.resizable(False, False)
    tk_patient_history_window.mainloop()

# handle back button click
def handle_treatment_back_action(wnd):
    if wnd is not None:
        wnd.destroy()

    global tk_main_window
    if tk_main_window is not None:
        tk_main_window.deiconify()
    else:
        start_automated_hospital()

# Take treatment decission
def do_diagnosis(wnd, aadhar_no, name, fever:str, running_nose,
                 loose_motion, body_pain, stomach_pain, hyper_tenstion, bp, acidity):
    symptoms = ("fever - {}, running nose - {}, loose motion - {},"
          " body pain - {}, stomach pain - {}, hyper tenstion - {}, blood pressure - {}, acidity - {}"
          .format(fever, running_nose, loose_motion, body_pain,
                  stomach_pain, hyper_tenstion, bp, acidity))
    print(symptoms)
    name_ret, age, _ = retrieve_patient_information(aadhar_no)
    # patient information is not present.
    if name_ret is None:
        messagebox.showinfo('Error', "Please provide correct aadhar number and press retrieve button")
        return
    # validate fever and bp value
    # https://en.wikipedia.org/wiki/Human_body_temperature
    fever = int(fever)
    if fever < 98 or fever > 110: # we are taking safe value. Patient should go to hospital for other cases.
        messagebox.showinfo('Error', "Please enter correct body temperator (98-110). "
                                     "If more or less, please contact nearby hospital/doctors")
        return
    bp = int(bp)
    if bp < 100 or fever > 160: # we are taking safe value. Patient should go to hospital for other cases.
        messagebox.showinfo('Error', "Please enter correct blood pressure (100-160). "
                                     "If more or less, please contact nearby hospital/doctors")
        return
    treatment_list = []
    age = int(age)
    if fever > 99:
        if age >= 12: # Adult
            if body_pain:
                treatment_list.append("Dolo - 650, BDS, 2 Days")
            else:
                treatment_list.append("Calpol - 650, BDS, 2 Days")
            if running_nose:
                treatment_list.append("Okacet (Cetirizine), BD, 2 Days")
        else: # children
            treatment_list.append("Calpol Syrup 250mg, 5 ml BDS, 3 Days")
            treatment_list.append("Ascoril LS, 5 ml SOS")
            if running_nose:
                treatment_list.append("Nasivion Pediatric, SOS")
    if loose_motion:
        if age >= 12:  # Adult
            treatment_list.append("Eldoper, BDS, 2 Days")
            treatment_list.append("ORS, SOS, 2 Days")
        else: # children
            treatment_list.append("ORS, SOS, 2 Days")
            treatment_list.append("syp Vizylac 5 ml, BDS, 2 Days")
    if acidity:
        if age >= 12:
            treatment_list.append("PAN - D, Monrning (Empty Stomach), 3 Days")
        else: # children
            treatment_list.append("Cyclopam Suspension, Monrning (Empty Stomach), 3 Days")
    important_msg = "N/A"
    if hyper_tenstion:
        if age >= 20 and int(bp) < 160:  # Adult
            treatment_list.append("Concord 5 mg, Morning, 7 days")
        else:  # children
            treatment_list.append("Aspirin, SOS")
            important_msg = "Please contact nearby hospital/doctor immediately."
    print('Treatment: {}'.format(treatment_list))
    # update patient record.
    if len(treatment_list) > 0:
        # write to record
        timestamp = datetime.datetime.now()
        treatment_record = '{}:{}:{}:{}\n'.\
            format(timestamp.strftime("%a %d %b %Y-%H-%M.%S"),
                   symptoms, treatment_list, important_msg)
        file = open(generate_record_filename(aadhar_no), "a+")
        if file is not None:
            file.write(treatment_record)
            file.close()
            print('Patient records updated successfully with {} information'.format(treatment_record))
        else:
            print('Unable to update patient records for treatment {}'.format(treatment_record))
        display_diagnosis(name_ret, treatment_list, important_msg)
    else:
        messagebox.showinfo('Suggestion', "Please take rest. If problem persist, "
                                          "please contact nearby hospital/doctor.")

# Process treatment request
def process_treatment_request():
    print('Process treatment request.')
    close_mainwnd()
    row_count = 0
    tk_patient_treatment_window = tk.Tk()
    validation = tk_patient_treatment_window.register(only_numbers)
    frame = tk.Frame(tk_patient_treatment_window, width=600, height=300, pady=5)
    frame.pack(pady=5, padx=5)
    tk_patient_treatment_window.title('Patient Treatment')
    label = tk.Label(frame, text= "Aadhar No: ", font='arial 15 bold')
    label.grid(row = row_count, column = 0, sticky = tk.W, padx = 2, pady = 2)
    aadhar_entry = tk.Entry(frame, validate="key", validatecommand=(validation, '%S'))
    aadhar_entry.grid(row=row_count, column=1, padx=2, pady=2)
    retrieve_button = tk.Button(frame, text="Retrieve", font="arial 10 bold")
    retrieve_button.grid(row=row_count, column=2, padx=2, pady=2)
    row_count += 1
    name_label = tk.Label(frame, text="Name:", font="arial 15 bold")
    name_label.grid(row=row_count, column=0, padx=2, pady=2)
    name_entry = tk.Entry(frame, font="arial 10 bold")
    name_entry.grid(row=row_count, column=1, padx=2, pady=2)
    name_entry.config(state=tk.DISABLED)
    row_count += 1
    retrieve_button.config(command=(lambda name_ent=name_entry,
                                        aadhar_ent=aadhar_entry
                                        :update_patient_info(name_ent, aadhar_ent.get().strip())))
    label = tk.Label(frame, text="Symptoms", font="arial 15 bold underline")
    label.grid(row=row_count, column=1, padx=10, pady=2)
    row_count += 1
    label = tk.Label(frame, text="Fever (F): ", font="arial 10 bold")
    label.grid(row=row_count, column=0, padx=2, pady=2)
    fever_entry = tk.Entry(frame, validate="key", validatecommand=(validation, '%S'))
    fever_entry.insert(tk.END, "98")
    fever_entry.grid(row=row_count, column=1, padx=2, pady=2)
    label = tk.Label(frame, text="Running Nose:", font="arial 10 bold")
    label.grid(row=row_count, column=2, padx=2, pady=2)
    # global running_nose
    running_nose = tk.IntVar()
    running_nose_check = tk.Checkbutton(frame, variable=running_nose)
    running_nose_check.grid(row=row_count, column=3, padx=2, pady=2)
    row_count += 1
    loose_motion = tk.IntVar()
    label = tk.Label(frame, text="Loose Motion:", font="arial 10 bold")
    label.grid(row=row_count, column=2, padx=2, pady=2)
    loose_motion_check = tk.Checkbutton(frame, variable=loose_motion)
    loose_motion_check.grid(row=row_count, column=3, padx=2, pady=2)
    row_count += 1
    body_pain = tk.IntVar()
    label = tk.Label(frame, text="     Body Pain:", font="arial 10 bold")
    label.grid(row=row_count, column=2, padx=2, pady=2)
    body_pain_check = tk.Checkbutton(frame, variable=body_pain)
    body_pain_check.grid(row=row_count, column=3, padx=2, pady=2)
    row_count += 1
    stomach_pain = tk.IntVar()
    label = tk.Label(frame, text="Stomach Pain:", font="arial 10 bold")
    label.grid(row=row_count, column=2, padx=2, pady=2)
    stomach_pain_check = tk.Checkbutton(frame, variable=stomach_pain)
    stomach_pain_check.grid(row=row_count, column=3, padx=2, pady=2)
    row_count += 1
    label = tk.Label(frame, text="Blood Pressure: ", font="arial 10 bold")
    label.grid(row=row_count, column=0, padx=2, pady=2)
    bp_entry = tk.Entry(frame, validate="key", validatecommand=(validation, '%S'))
    bp_entry.insert(tk.END, "120")
    bp_entry.grid(row=row_count, column=1, padx=2, pady=2)
    label = tk.Label(frame, text="Hyper Tension:", font="arial 10 bold")
    label.grid(row=row_count, column=2, padx=2, pady=2)
    hyper_tension = tk.IntVar()
    hyper_tension_check = tk.Checkbutton(frame, variable=hyper_tension)
    hyper_tension_check.grid(row=row_count, column=3, padx=2, pady=2)
    row_count += 1
    acidity = tk.IntVar()
    label = tk.Label(frame, text="            Acidity:", font="arial 10 bold")
    label.grid(row=row_count, column=2, padx=2, pady=2)
    acidity_check = tk.Checkbutton(frame, variable=acidity)
    acidity_check.grid(row=row_count, column=3, padx=2, pady=2)
    row_count += 1
    submit_button = tk.Button(frame, text="Submit", font="arial 10 bold", width=10)
    submit_button.grid(row=row_count, column=1, padx=2, pady=2)
    submit_button.config(command=(lambda wnd=tk_patient_treatment_window,
                     aadhar_ent=aadhar_entry, name_ent=name_entry, fever_ent=fever_entry,
                     running_nose_status=running_nose, loose_motion_status=loose_motion,
                     body_pain_status=body_pain, stomach_pain_status=stomach_pain,
                     hyper_tenstion_status=hyper_tension, acidity_status=acidity,
                     bp_ent=bp_entry:
                                  do_diagnosis(wnd, aadhar_ent.get().strip(),
                                               name_ent.get().strip(), fever_ent.get().strip(),
                                               running_nose=running_nose_status.get(),
                                               loose_motion=loose_motion_status.get(),
                                               body_pain=body_pain_status.get(),
                                               stomach_pain=stomach_pain_status.get(),
                                               hyper_tenstion=hyper_tenstion_status.get(),
                                               bp=bp_ent.get().strip(),
                                               acidity=acidity_status.get()
                                               )))

    ok_button = tk.Button(frame, text="Back", font="arial 10 bold",
                            width=10, command=(lambda wnd=tk_patient_treatment_window:
                                                    handle_treatment_back_action(wnd))) # Close the window
    ok_button.grid(row=row_count, column=2, padx=2, pady=2)
    # hadle window close
    tk_patient_treatment_window.protocol("WM_DELETE_WINDOW", (lambda wnd=tk_patient_treatment_window:
                                                              handle_treatment_back_action(wnd)))
    tk_patient_treatment_window.resizable(False, False)
    tk_patient_treatment_window.mainloop()


# Start hospital user interface
def start_automated_hospital():
    global tk_main_window
    tk_main_window = tk.Tk()
    tk_main_window.title('Rural Automated Treatment System')
    title_label = tk.Label(tk_main_window, text="Welcome to automated treatment kiosk",
                     font="arial 25 bold", padx=30, pady=30)
    title_label.pack()
    add_button = tk.Button(tk_main_window, text="Registration",
                           font="arial 15", command=patient_registration)
    add_button.pack(side=tk.LEFT, ipadx=20, padx=5)
    history_button = tk.Button(tk_main_window, text="History",
                           font="arial 15", command=show_patient_history)
    history_button.pack(side=tk.LEFT, ipadx=20, padx=5)
    treatment_button = tk.Button(tk_main_window, text="Treatment",
                           font="arial 15", command=process_treatment_request)
    treatment_button.pack(side=tk.LEFT, ipadx=20, padx=5)
    exit_button = tk.Button(tk_main_window, text="Exit",
                           font="arial 15", command=tk_main_window.destroy)
    exit_button.pack(side=tk.RIGHT, ipadx=20, padx=10, pady=10)
    frame = tk.Frame(tk_main_window)
    frame.pack()
    tk_main_window.resizable(False, False)
    tk_main_window.mainloop()

# Top level code
if __name__ == '__main__':
    print('Welcome to rural automated interactive hospital');
    # initialize internal database
    initialize_database()
    # start hospital functionalities
    start_automated_hospital()


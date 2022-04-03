from datetime import datetime as dt
from datetime import timedelta
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import math
import re
import time
from tkinter import messagebox
#import pyaudio
#import wave
import pygame
from PIL import ImageTk, Image
#well this is a leson in why it is always a good idea to research the documeation first:
    #I think it was a big mistake using datime

#STOP USING CLASS VARIABLES AND CONSIDERING CHANGING THEM AND PASSING ARGUMENTS

#switch the way stop works to using wait_variable. this will
#add reset function
#I wonder if I can get the curser to move automatically after entering 2 characters



class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.running = False
        if self.check_settings_file(False) == True:
            self.set_vars()
            self.set_txt_vars()
            self.pack(fill = 'both', expand = True)
            self.create_widgets()
            self.master.geometry(('600x350+75+150')) #delete the + 35 etc and see what happens
            self.get_alm_file()
        else:
            self.settings_failure()


    def check_settings_file(self, rewritten): #rewritten is bool: determines if the settings_rewrite fn ran already
            settings_options = [
                "audio_file = ",
                "auto_off = ",
                "Warning_Tone_Play\? = "]
            for option in settings_options:
                if self.search_settings(option):
                    print(option, ' OK in check_settings_file')
                else:
                    print(option, 'CURRUPT in check_settings_file')
                    if rewritten == False:
                        self.settings_rewrite()
                    else:
                        return False
            return True

    def settings_rewrite(self):
        with open('settings.txt', 'w') as f_currupt:
            with open('settings_backup.txt', 'r') as f_backup:
                new_data = f_backup.read()
                f_currupt.write(new_data)
        self.check_settings_file(True)

    def settings_failure(self):
        if messagebox.askokcancel("ERROR", "The Settings File Is Currupt"):
          root.destroy()

    def set_txt_vars(self):
        self.sec_txt = self.txtvar_handler() # assigns stringvar and trace fnction
        self.min_txt = self.txtvar_handler()
        self.hr_txt = self.txtvar_handler()
        self.time_txt =tk.StringVar()
        self.time_txt.set('00:00:00')
        self.end_time_txt = tk.StringVar()
        self.end_time_txt.set('')
        self.add_sec = tk.StringVar()
        self.add_sec.set(0)
        self.alm_file_txt = tk.StringVar()

    def create_frames(self):
        #title
        self.winfo_toplevel().title("Timer")

        #create frames
        self.top_frame = tk.Frame(self, bg = 'Bisque4') #will have user input and clear button
        self.top_frame.pack(side="top",
            fill = 'both',
            expand=False )

        self.right_frame = tk.Frame(self, bg = 'Bisque4') #buttons
        self.right_frame.pack(side = 'right',
            fill = 'y',
            expand = False,
            anchor = 'n')

        self.mid_frame = tk.Frame(self,
            bg = 'green2',
            relief = 'raised',
            borderwidth = 4) #clock
        self.mid_frame.pack(side="top",
            fill="both",
            expand = True)

        self.bottom_most_frame = tk.Frame(self, bg = 'Gray16')
        self.bottom_most_frame.pack(side = "top",
            fill= "both",
            expand = False)
        #self.bottom_frame = tk.Frame(self,  bg = 'green2',
        #    expand=True)

    def top_frame_widgets(self):

        self.clear_bt = tk.Button(  self.top_frame,
            text = "   CLEAR   ",
            font = ('defualt', 12,),
            fg = 'black',
            command = self.clear_text)

        self.clear_bt.pack(side = 'right',
            anchor = 'w',
            padx = 40,
            pady = 5)
            #second box and label





        self.sec_entry = tk.Entry(self.top_frame,
            width = 3,
            textvariable=self.sec_txt)
        self.sec_entry.pack(side = 'right', padx = 2)

        self.colon_lbl = tk.Label(self.top_frame,
            text = ":",
            bg = 'Bisque4',
            font = ('defualt', 20))
        self.colon_lbl.pack(side = 'right',
            anchor = 's',
            ipady = 11)

        self.min_entry = tk.Entry(self.top_frame,
            width = 3,
            textvariable=self.min_txt, )
        self.min_entry.pack(side = 'right', padx = 2)
        self.min_entry.icursor(0)
            #minute box and label

        self.colon_lbl = tk.Label(self.top_frame,
            text = ":",
            bg = 'Bisque4',
            font = ('defualt', 20))
        self.colon_lbl.pack(side = 'right',
            anchor = 's',
            ipady = 11)

        self.hour_entry = tk.Entry(self.top_frame,
            width = 3,
            textvariable=self.hr_txt)
        self.hour_entry.pack(side = 'right',
            padx = 2,
            pady = 11)

        self.sec_lbl = tk.Label(self.top_frame,
            text = "SEC",
            bg = 'Bisque4',
            font = ('defualt', 12))

        self.sec_lbl.pack(side = 'right',
            ipady = 16,
            anchor = "s")
#minute box and lbl
        self.min_lbl = tk.Label(self.top_frame,
            text = "MIN :",
            bg = 'Bisque4',
            font = ('defualt', 12))
        self.min_lbl.pack(side = 'right',
            ipady = 16,
            anchor = "s")


        self.hr_lbl = tk.Label(self.top_frame,
            text = "HR :",
            bg = 'Bisque4',
            font = ('defualt', 12))
        self.hr_lbl.pack(side = 'right',
            anchor = 's',
            ipady = 16)



        new_order = (self.hour_entry, self.min_entry, self.sec_entry)
        for widget in new_order: #this changes the order of tab. so you can tab from hour to min to sec entry windows. thank you Brian Oakley (stackoverflow)
            widget.lift()

    def mid_frame_widgets(self):
        self.cntdwn_label = tk.Label(self.mid_frame,
            textvariable = self.time_txt,
            font = ("Arial", 38, "bold"),
            bg = 'green2')
        self.cntdwn_label.pack(side = 'top',
            pady = 60,
            padx = 10,
            expand = 'true')
        self.end_time_lbl = tk.Label(self.mid_frame,
            textvariable = self.end_time_txt,
            font = ("Courier New", 17),
            bg = 'green2')

        self.end_time_lbl.pack(side = 'top',
            pady = 0,
            expand = 'true')


    def bottom_most_widgets(self):

        self.warning_tone_var = tk.StringVar()
        self.warning_tone_txt = tk.StringVar()
        self.warning_tone_txt.set(self.get_warning_tone_txt())
        #self.warning_tone_var.trace('w', self.play_warning_tone)
        self.warning_tone_lbl = tk.Label(
            self.bottom_most_frame,
            textvariable = self.warning_tone_txt,
            font = ("Calibri", 13),
            fg = '#737373',
            bg = 'Gray16' ).pack(side = 'right',
            padx = 10,
            anchor = 'ne')
        self.alm_tone_lbl = tk.Label(self.bottom_most_frame,
            textvariable = self.alm_file_txt,
            font = ("Calibri", 13), fg = '#737373', bg = 'Gray16' )
        self.alm_file_txt.set("Alarm Tone: %s" % self.get_file_txt())
        self.alm_tone_lbl.pack(side = 'top',
            padx = 10,
            anchor = 'w')

        self.auto_off_txt = tk.StringVar()
        self.set_current_auto_off()
        #self.set_warning_tone()
        self.auto_off_txt.set(self.get_auto_off_txt(self.auto_off_sec))
        self.auto_off_dsp = tk.Label(self.bottom_most_frame,            ##It should be broken up and auto off should not be a class variable
            textvariable = self.auto_off_txt,
            font = ("Calibri", 13), fg = '#737373', bg = 'Gray16')
        self.auto_off_dsp.pack(side = 'top',
            padx = 10,
            anchor = 'w')

    def right_frame_widgets(self):

        self.start_bt = tk.Button(self.right_frame,
            text = "    START    ",
            font = ('defualt', 16, 'bold'),
            fg = 'black',
            bg = '#6DFF7D',
            relief = 'raised',
            borderwidth = 3,
            command = lambda: self.start(button_press = True
            ))
        self.start_bt.pack(side = 'top',
            padx = 5,
            pady = 5,
            anchor = 'n')


        self.add_min_bt = tk.Button(self.right_frame,
            text = "ADD 1 MINUTE",
            font = ('defualt', 12),
            command = lambda: self.add_min(1))

        self.add_min_bt.pack( side="top",
            anchor = 'n',
            pady = 5,
            padx = 5,
            ipadx = 7,
            expand = False)

        self.settings_bt = tk.Button(self.right_frame,
            text="Settings",
            font = ('defualt', 12),
            command= self.create_settings_wind)

        self.settings_bt.pack(side='top',
            anchor = 'n',
            padx = 5,
            pady =5,
            ipadx = 34)

        self.pause_bt = tk.Button(self.right_frame,
            text = "Pause",
            font = ('defualt', 12),
            command= self.pause_tmr)

        self.pause_bt.pack(side = 'top',
            anchor = 'n',
            padx = 5,
            pady = 5,
            ipadx = 39)

        self.stop_bt = tk.Button(self.right_frame,
            text = "STOP",
            font = ('defualt', 14,  'bold'),
            #fg = '#b3b3b3',
            bg = '#E43433',
            relief = 'raised',
            borderwidth = 3,
            command= self.stop_timer)

        self.stop_bt.pack(side="top",
            anchor = 'n',
            padx = 5,
            pady = 5,
            ipadx = 35)


    def create_widgets(self):

        self.create_frames()
        self.top_frame_widgets()
        self.right_frame_widgets()
        self.mid_frame_widgets()
        self.bottom_most_widgets()

    def set_vars(self):
        self.read_keys_list()
        self.pause_val = False
        self.alm_play = tk.StringVar()
        self.alm_play.set(False)
        self.alm_play.trace('w', self.play_alarm)
        self.warning_tone_play = False

        self.ask_b4cls = tk.IntVar()
        self.ask_b4cls.set(self.read_ask_b4cls())

        self.stop_val = tk.StringVar()
        self.stop_val.set(False)
        self.stop_val.trace('w', self.stop_alarm)
        self.auto_off_data = ['Never', '5', '10', '15', '20', '30', '45', '60', '90']

    def ask_on_close(self):
        print('the ask_b4cls variable is:', self.ask_b4cls.get())
        if self.running == True and self.ask_b4cls.get() == 1:
            if messagebox.askokcancel("Quit", "The Timer Is Running. Exit Anyway?"):
              root.destroy()
        else:
            root.destroy()

    def get_warning_tone_txt(self):
        value = self.read_warning_tone()
        if int(value) == 1:
            string = "Tone at 15 Seconds: ON"
        elif int(value) == 0:
            string = "Tone at 15 Seconds: OFF"
        else:
            self.print_error("ERROR: in get_warning_tone_txt\nBad warning_tone_var(%s)" % self.warning_tone_var.get())
            string = ''
        return string

    def read_warning_tone(self):
        search = self.search_settings('Warning_Tone_Play\? = ')
        try:
            if len(str(search)) > 1:
                self.warning_tone_var.set(int(search.group(1)))
            else:
                string = "ERROR: in Read_Warning_Tone:\n Search in settings failed"
                self.print_error(string)
                self.warning_tone_var.set(int(0))
        except AttributeError:
            self.print_error("Search Error: Settings file is likely currupt")

        return self.warning_tone_var.get()

    def write_to_settings(self, match, replacement):
        with open('settings.txt', 'r') as f:
            data = f.read()
        with open('settings.txt', 'w') as f:
            old = match
            print('replacing %s with %s write_to_settings' % (old, replacement))
            f.write(data.replace(old, replacement))
            #except:
            #f.write(data)

    def write_warning_tone(self):
            match = self.search_settings('Warning_Tone_Play\? = ')
            if match:
                old = match.group(1)
                self.write_to_settings('Warning_Tone_Play? = ' + match.group(1), 'Warning_Tone_Play? = ' + str(self.warning_tone_var.get()))

            else:
                old  = "None"
                string = 'ERROR in write warning tone,\nError reading file'
                self.print_error(string)



    def set_current_auto_off(self): #returns index
        search = self.search_settings('auto_off = ')
        if search:                                          #I don't think that was working as intended anyways
            self.auto_off_sec = search.group(1)
        else:
            string = "ERROR: set_current_auto_off:\n Search in settings failed"
            self.print_error(string)
        i = 0
        for time in self.auto_off_data:
            if time == str(self.auto_off_sec):
                return[i]
            i += 1



    def set_current_audio(self):
        alarm_file = self.get_alm_file()
        i = 0
        for file in self.alm_file_dict.values():
            if file == alarm_file:
                return(i)
            i += 1
    def browse(self):
        file_path = filedialog.askopenfilename(initialdir = "C:\\Users\\12035\\Music",
            title = 'Select An Audio File',
            filetype = (("audio files (mp3/wav)", "*.mp3 *.wav"), ("any file", "*.*")))
        if not re.search('^[\w\s\._:/\\@!?$%^&*]+$', file_path):
            tk.messagebox.showwarning(title='Incorrect Format', message='Filepath Must Only Contain Letters or Spaces')

        #label = ttk.Label(self, text = "open file")
        else:
            self.get_file_nickname(file_path)

    def get_file_nickname(self, file_path):

        self.nickname_window = tk.Toplevel(self)
        self.nickname_window.geometry('480x175+800+150')

        title_label = tk.Label(self.nickname_window,
            text = "Choose a Nickname",
            font = ("Courier New", 19)).grid(
            row = 0,
            column = 0,
            columnspan = 6,
            padx = 5,
            pady = 15)

        self.nickname = tk.StringVar()
        nickname_entry_lbl = tk.Label(self.nickname_window,
            text = "Enter a nickname for your file: ",
            font = ('default', 11)).grid(
            row = 2,
            column = 0,
            padx = 5,
            pady = 15
            )
        self.nickname_entry = tk.Entry(self.nickname_window,
            width = 40,
            textvariable = self.nickname)
        self.nickname_entry.grid(row = 2,
            column = 3,
            columnspan = 3,
            padx = 5,
            pady = 15)

        ok_button = tk.Button(self.nickname_window,
            text = "OK",
            command = lambda: self.nickname_command(
                skip = False,
                filepath = file_path),
            font =('defualt', 10))
        ok_button.grid(
            row = 4,
            column = 5,
            columnspan = 1,
            pady = 15,
            padx = 5,
            ipadx = 12,
            sticky = 'nesw'
            )

        skip_bt = tk.Button(self.nickname_window,
            text = "Skip",
            font =('defualt', 10),
            command = lambda: self.nickname_command(
                skip = True,
                filepath = file_path))
        skip_bt.grid(row = 4,
            column = 3,
            pady = 15,
            padx = 5,
            ipadx = 20,
            columnspan = 1,
            sticky = 'e')

    def nickname_command(self, skip, filepath):
        if filepath:
            if skip or len(self.nickname_entry.get()) < 1:
                new_key = re.search( '(?<=/).*/(.+)\..{3}' , filepath)
                new_key = new_key.group(1)
                print('The nickname for the new file is %s' % new_key)
            else:
                new_key = self.nickname_entry.get()

            if not all(char.isalpha() or char.isspace() or char.isnumeric() for char in new_key):
                tk.messagebox.showwarning(title='Incorrect Format', message='Please enter ONLY letters or spaces!')
            else:
                self.alm_file_dict[new_key] = str(filepath)
                self.audio_files_combox.set(new_key)

                keys_lst = []
                for key in self.alm_file_dict:
                    keys_lst.append(key)
                self.audio_files_combox.config(values = keys_lst)
                with open('settings.txt', 'r') as f:
                    data = f.read()
                match = re.search('(.+@.*\.\w{3}\n})', data)
                #this regex (above) creates a list of all keys. I'm not sure where I'm going with this though.
                #I think I need to start with creating alm_file_dict from settings file in sep. function
                #this should be yet another funcction to update settings

                if match:
                    self.write_to_settings(match.group(1), match.group(1).strip('}') + '\n' + new_key + ' @ ' + str(filepath) + '\n' + '}')
                else:
                    self.print_error("Search Fialed In Nickname Command")
                self.nickname_window.destroy()


    def assign_auto_off(self):
        seconds = self.auto_off_combo_sec.get()
        match = self.search_settings('auto_off = ')
        if match:
            self.write_to_settings('auto_off = ' + match.group(1), 'auto_off = ' + str(seconds))
            #with open('settings.txt', 'r+') as f:
            #    data = f.read()
            #    f.write(data.replace(old, seconds))
        else:
            old  = "None"
            print('ERROR in assign_auto_off,\nError reading file not found')
            string = 'ERROR in assign_auto_off,\nError reading file'
            self.print_error(string)

        self.set_window.destroy()
        self.set_current_auto_off()

        self.auto_off_txt.set(self.get_auto_off_txt(seconds))

    def get_key_frm_val(self, dict, val):
        key_list = list(dict.keys())
        val_list = list(dict.values())
#this is convoluted. We are taking the list of values,
        #getting the index and then getting that same
        #in the key list
        return(key_list[val_list.index(val)])
    def print_error(self, str):
        self.time_txt.set(str)
        self.cntdwn_label.config(font = ('default', 16))
        self.error_stop()

    def assign_alm_file(self):
        self.alm_file = self.alm_file_dict[self.audio_files_combox.get()]

        match = self.search_settings('audio_file = ')

        if match:
            self.write_to_settings('audio_file = ' + match.group(1), 'audio_file = ' + self.get_key_frm_val(self.alm_file_dict, self.alm_file))

        else:
            string = "ERROR: in assign_alm_file,\nSearching settings to write"
            self.print_error(str)


        self.set_window.destroy()
        self.alm_file_txt.set("Alarm Tone: %s" % self.get_file_txt())



    def create_settings_wind(self): #let's break this into smaller functions

        self.set_window = tk.Toplevel(self)
        self.set_window.title('Timer Settings')

        self.set_window.geometry('700x350+600+150')

        alm_file = tk.StringVar()

        #self.audio_file_window.grid()
        settings_lbl = tk.Label(self.set_window,
            text = 'Settings',
            font = ("Courier New", 19))
        settings_lbl.grid(row = 0,
            column = 0,
            columnspan = 8,
            pady = 15)

        af_combox_lbl = tk.Label(self.set_window,
            text = "Choose an alarm sound to play:",
            font =('defualt', 11))
        af_combox_lbl.grid(row = 1,
            column = 0,
            padx = 25, pady = 5,
            columnspan = 2,
            sticky = 'w'
            )
        keys_lst = []
        for key in self.alm_file_dict.keys():
            keys_lst.append(key)
        #print(keys_lst, 'keys lst')



        self.audio_files_combox = ttk.Combobox(
            self.set_window,
            width = 30,
            values = keys_lst)

        self.audio_files_combox.grid(
            row = 1,
            column = 2,
            pady = 5,
            columnspan = 3,
            sticky = 'w')
        self.audio_files_combox.set(
            self.get_key_frm_val(self.alm_file_dict,self.alm_file))
        #self.audio_files_combox.current(newindex = self.set_current_audio()) #new index selects the words to display in the text box

        browse_button = tk.Button(self.set_window,
            text = "Browse",
            command = self.browse,
            font =('defualt', 10))
        browse_button.grid(row = 1,
            column = 5,
            ipadx = 3,
            padx = 6)

        play_button = tk.Button(self.set_window,
            text = "Play",
            command = self.play_alarm_sample,
            font =('defualt', 10))
        play_button.grid(row = 1,
            column = 6,
            sticky = 'w',
            pady = 15,
            ipadx = 12)

        delete_button = tk.Button(self.set_window,
            text = "Delete",
            command = self.delete_audio,
            font =('defualt', 10))
        delete_button.grid(row = 1,
            column = 6,
            columnspan = 2,
            pady = 15,
            padx = 68,
            sticky = 'w',
            ipadx = 9)

        auto_off_lbl = tk.Label(self.set_window,
            text='Alarm auto off after (seconds)',
            font =('defualt', 11)).grid(row = 2,
            column = 0,
            columnspan = 2,
            padx = 5,
            pady = 15)

        self.auto_off_combo_sec = tk.StringVar()
        self.auto_off_combobox = ttk.Combobox(self.set_window,
            values = self.auto_off_data,
            textvariable = self.auto_off_combo_sec,
            width = 6,)
        self.auto_off_combobox.set(5)
        seconds = self.auto_off_combobox.get()
        self.auto_off_combobox.grid(row = 2,
            column = 2,
            sticky = 'w')
        self.auto_off_combobox.current(newindex = self.set_current_auto_off())

        self.warning_tone_var = tk.IntVar() #like StringVar but integer
        self.read_warning_tone()
        warning_tone_ck_box = tk.Checkbutton(self.set_window,
            text = "Play Warning Tone At 15 Seconds Left",
            font =('defualt', 11),
            variable = self.warning_tone_var)
        warning_tone_ck_box.grid(row = 4,
             column = 0,
             columnspan = 3,
             padx = 25,
             pady = 15,
             sticky = 'w')


        self.ask_b4cls.set(int(self.read_ask_b4cls()))
        ask_b4cl_ckbx = tk.Checkbutton(self.set_window,
            text = "Ask before close while alarm is running?",
            font =('defualt', 11),
            variable = self.ask_b4cls)
        ask_b4cl_ckbx.grid(row = 5,
             column = 0,
             columnspan = 3,
             padx = 25,
             pady = 15,
             sticky = 'w')


        ok_button = tk.Button(self.set_window,
            text = "OK",
            command = self.ok_settings_command,
            font =('defualt', 10))
        ok_button.grid(row = 6,
            column = 6,
            columnspan = 2,
            pady = 15,
            padx = 65,
            ipadx = 20,
            sticky = 'w')

        cancel_bt = tk.Button(self.set_window,
            text = "Cancel",
            font =('defualt', 10),
            command = self.set_window.destroy)
        cancel_bt.grid(row = 6,
            column = 5,
            pady = 15,
            padx = 30,
            ipadx = 14,
            columnspan = 2,
            sticky = 'w'
            )

    def read_ask_b4cls(self):
        match = self.search_settings('Accidental exit protection window = ')
        print('the match in read_ask_b4cls is %s' %match.group(1))
        return(match.group(1))

    def write_ask_b4cls(self):
        settings_str = 'Accidental exit protection window = '
        match = self.search_settings(settings_str)
        if match:
            old = match.group(1)
            self.write_to_settings(settings_str + match.group(1), settings_str + str(self.ask_b4cls.get()))

    def delete_audio(self):
        if not messagebox.askokcancel("Delete File?", "Remove %s alarm file?" % self.audio_files_combox.get()):
            return None
        key = self.audio_files_combox.get()
        with open('settings.txt', 'r') as f:
            data =  f.read()
        match = re.search(key + '\s*@.+\.\w{3}', data)
        if match:
            data = re.sub(match.group(), '', data)
            lines = data.split('\n')
            new_data = []
            for line in lines:
                if len(line) > 0:
                    new_data.append(line)
            new_data = '\n'.join(new_data)

            with open('settings.txt', 'w+') as f:
                f.write(new_data)
        else:
            self.print_error("Search in delete_audio failed")

        self.read_keys_list()
        self.audio_files_combox.set('Annoying Beep')
        keys_lst = []
        for key in self.alm_file_dict:
            keys_lst.append(key)
        self.audio_files_combox.config(values = keys_lst)





    def read_keys_list(self):

        with open('settings.txt', 'r') as f:
            search = re.search('(?:\$\$alm_file_dict = \{)([^\}]*)', f.read())

            if search:
                self.alm_file_dict = {}
                #dict_lst =
                for line in search.group(1).split('\n'):

                    if len(line) > 2:
                        line = line.lstrip().rstrip()
                        #line = line.replace('\'','')
                        line = line.split('@')
                        key = line[0].lstrip().rstrip()
                        value = line[1].lstrip().rstrip()
                        self.alm_file_dict[key] = value.strip(',')
                print('alm_file_dict is: ', self.alm_file_dict)
                #return search.group(1)

    def ok_settings_command(self):
        self.assign_alm_file()
        self.assign_auto_off()
        self.write_warning_tone()
        self.read_warning_tone()
        self.write_ask_b4cls()
        self.read_ask_b4cls()
        self.warning_tone_txt.set(self.get_warning_tone_txt())


    def rgb_to_hex(self, rgb): #thank you Reblochon Masque(stackoverflow) for this very helpful converter
        return "#%02x%02x%02x" % rgb


    def change_bg_color(self, window, r, g, b):
        #window.pack_forget()
        red = 65 + r
        green = 252 + g
        blue = 40 + b
        color_lst = [red, green, blue]
        i = 0
        for color in color_lst: #color represents a number for rgb (0-256)
            if color > 255:
                color_lst[i] = 255 #if color is greater>255 set it = to 256

            elif color < 0:
                color_lst[i] = 0

            i += 1
        window.config(bg = self.rgb_to_hex((color_lst[0], color_lst[1], color_lst[2])))
        #window.pack()

    def txtvar_handler(self):
        var = tk.StringVar()
        var.trace('w', self.limitSizeTxt)
        return var

    def limitSizeTxt(self, *args):

        hr_val = self.hr_txt
        min_val = self.min_txt
        sec_val = self.sec_txt
        list_val = [hr_val, min_val, sec_val]
        i = 0
        for var in list_val:   #finally works! takes var(class variable) from the list and
            val = var.get()    #gets a value from the text box
            if len(val) > 2:
                var.set(val[:2]) #sets the value as the value reduced to 2 chars
                #val.set(val[:2]

        #except:
    def pause_tmr(self):
        self.pause_val = True

        try:
            self.pause_time = self.time_left
        except AttributeError:
            self.pause_val = False
            return None
        print(self.pause_time, 'pause time')
        self.stop_val.set(True)
        self.timer = None
        self.running = False
        self.time_txt.set(self.pause_time)
        self.add_sec.set(0)

    def error_stop(self):
        self.pause_val = False
        self.stop_val.set(True)
        self.timer = None
        self.running = False
        self.end_time_txt.set('')
        self.cntdwn_label.config(bg = '#e60000')
        self.mid_frame.config(bg= '#e60000')
        #self.end_time_lbl.config(bg = '#e60000')
        self.add_sec.set(0)

    def stop_timer(self):
        root.attributes('-topmost', False)
        self.pause_val = False
        self.stop_val.set(True)
        self.timer = None

        if self.pause_val == True:
            self.time_txt.set(self.pause_time)
        else:
            self.running = False
            self.time_txt.set('00:00:00')
            self.end_time_txt.set('')
            self.cntdwn_label.config(bg = 'green2')
            self.mid_frame.config(bg= 'green2')
            self.end_time_lbl.config(bg = 'Green2')
        self.add_sec.set(0)



    def add_min(self, min):

        self.stop_val.set( False)

        self.add_sec.set(min * 60)
        print('running =', self.running)
        #if self.running == False:
        if self.running == False:
            self.start(button_press = False)
        else:
            self.timer.add_to_end_time()
        #else:



    def clear_text(self):
        self.hr_txt.set('')
        self.min_txt.set('')
        self.sec_txt.set('')

    def start(self, *args, button_press):
        if self.running == True:
            return None
        self.cntdwn_label.config(font = ("Arial", 38, "bold")) #this is because it may have been modified to print an error message in self.round_time
        self.running = True

        self.mid_frame.config(bg = 'green2')

        if button_press == True:
            self.add_sec.set(0) #resets this variable which probalby should not be a class variable
        self.stop_val.set(False)

        if self.pause_val == True:
            seconds = self.pause_time.seconds #this grabs the total seconds remaining
            minutes = 0 #total time is stored in seconds
            hours = 0
            self.pause_val = False
        else:
            hours = self.hr_txt.get()
            minutes = self.min_txt.get()
            seconds = self.sec_txt.get()

        time = [hours, minutes, seconds]
        i = 0
        for t in time: #this sets all none values = 0
            if t == '':
                time[i] = 0
            i += 1
        #time[2] += self.add_sec
        print(time[0], time[1], time[2], 'time[hr, min, sec]')

        self.timer = Timer(time[0], time[1], time[2])

        self.time_check()

    def time_at_end_setter(self):
        self.end_time_txt.set("Time At End = %s" % self.end_time.strftime('%I:%M:%S:%p'))

    def time_check(self):
        if self.running == False:
            return None
        if self.timer == None:
            print('no timer')
        else:
            self.end_time = self.timer.end_time
            day_end = self.end_time.day
            hour_end = self.end_time.hour
            minute_end = self.end_time.minute
            second_end = self.end_time.second

            #get hour/min/sec now
            day_now = dt.now().day
            hour_now = dt.now().hour
            minute_now = dt.now().minute
            second_now = dt.now().second
#get total seconds in current time and end time
            if day_now == day_end:

                seconds_in_hr_end = hour_end * 60 * 60
                seconds_in_min_end = minute_end * 60
                total_sec_end = seconds_in_hr_end + seconds_in_min_end + second_end

                seconds_in_hr_now = hour_now * 60 * 60
                seconds_in_min_now = minute_now * 60
                total_sec_now = seconds_in_hr_now + seconds_in_min_now + second_now
            else: #This prevents errors if it goes to the next day
                seconds_in_hr_end = (hour_end + 24) * 60 * 60
                seconds_in_min_end = minute_end * 60
                total_sec_end = seconds_in_hr_end + seconds_in_min_end + second_end

                seconds_in_hr_now = hour_now * 60 * 60
                seconds_in_min_now = minute_now * 60
                total_sec_now = seconds_in_hr_now + seconds_in_min_now + second_now

            self.time_left = (timedelta(0, (total_sec_end), 0)) - (timedelta(0, total_sec_now, 0)) #the zero are days? and microseconds
            zero_time = timedelta(hours = 0, minutes = 0, seconds = 0)
            sec_left_30 = timedelta(hours = 0, minutes = 0, seconds = 5)
            sec_left_30 = timedelta(hours = 0, minutes = 0, seconds = 30)


            if zero_time < self.time_left and self.stop_val.get() == '0':

                self.time_txt.set(self.time_left)

                for n in range(30):
                    if self.time_left.seconds < 30 - n:
                        self.change_bg_color(self.mid_frame, 20 + (n * 45), -50 - (n * 5), 0)
                    #    self.change_bg_color(self.bottom_frame, 20 + (n * 45), -50 - (n * 5), 0)
                        self.change_bg_color(self.cntdwn_label, 20 + (n * 45), -50 - (n * 5), 0)
                        self.change_bg_color(self.end_time_lbl, 20 + (n * 45), -50 - (n * 5), 0)

                    elif self.time_left.seconds > 30:
                            self.change_bg_color(self.mid_frame, 0, 0, 0)
                        #    self.change_bg_color(self.bottom_frame, 0, 0, 0)
                            self.change_bg_color(self.cntdwn_label, 0, 0, 0)
                            self.change_bg_color(self.end_time_lbl, 0, 0, 0)

                if self.time_left.seconds < 15 and int(self.warning_tone_var.get()) == 1:
                    if self.warning_tone_play == False:
                        self.warning_tone_play = True
                        self.play_warning_tone()

            elif self.stop_val.get() == '1': # i should break this up into smaller functions
                self.time_txt.set("00:00:00")
        #    elif self.time_left > timedelta
            elif self.stop_val.get() == '0' and zero_time >= self.time_left:
                self.time_txt.set("DING!!!!")

                if self.alm_play.get() == '0': #this is to avoid the play_alarm fn from being called every 300 miliseconds
                    self.alm_play.set(True) #The variable self.alm_play plays the alarm when it is changed.
        self.time_at_end_setter()
        self.after(300, self.time_check)

    def get_auto_off_txt(self, seconds):
        if seconds == 'Never':

            string = "Alarm Audio Will Loop" #% u"\u221E" #really cool loop char but its squished
            return string
        else:
            string = "Audio Runtime: %d seconds" % int(seconds)
            return string



    def get_file_txt(self, *args): #I don't want to have to turn the button that calls this into a lambda fuction to pass argument
        filename = ''
        for arg in args:
            filename = arg

        if len(filename) < 2: #if filename was not in args, we have to get it from settings
            filename = self.get_alm_file()
            print('filename is %s' % filename)
        else:
            pass #if it was in args. It is coming through args already stripped of mp3/wave
        return(self.get_key_frm_val(self.alm_file_dict, filename))

    def set_alm_text_color(self, file):
        if file == 'foghorn.mp3':
            self.alm_tone_lbl.config(fg = '#737373')

    def search_settings(self, search_str):
        with open('settings.txt', 'r') as f:
            search = re.search ('(?:\$\$%s)(.*)' %search_str, f.read())
            return search


    def get_alm_file(self):
        search = self.search_settings('audio_file = ')
        if search:
                try:
                    self.alm_file = self.alm_file_dict[search.group(1)]
                    self.set_alm_text_color(self.alm_file)
                    return(self.alm_file)
                except Exception as e:
                    string = str(e)
                    self.print_error(string)
                    return('')

        else:
                string = "ERROR: Audio File Not \nFound In Settings!"
                self.print_error(str)
                return('')


    def play_audio(self, file, repeat): #repeat is the same format as pygame -1 loop, 1 play once
        pygame.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(repeat)

    def play_warning_tone(self, *args):
        pygame.init()
        pygame.mixer.music.load('alarm10.wav')
        pygame.mixer.music.play(1)

    def play_alarm_sample(self):
        pygame.init()
        key = self.audio_files_combox.get()
        pygame.mixer.music.load(self.alm_file_dict[key])
        pygame.mixer.music.play(-1)
        self.after(9000, pygame.mixer.music.stop)

    def play_alarm(self, *args):
        root.lift()
        root.attributes('-topmost', True)
        root.attributes('-topmost', False)
        pygame.init()
        alm_file = self.get_alm_file()
        pygame.mixer.music.load(alm_file)
        self.set_current_auto_off()
        print(self.auto_off_sec, 'auto off secs1')
        if self.alm_play.get() == '1':
            pygame.mixer.music.play(-1)
        if self.auto_off_sec != "Never":
            self.after((int(self.auto_off_sec)*1000), pygame.mixer.music.stop)

    def stop_alarm(self, *args):
        self.alm_play.set(False)
        pygame.mixer.music.stop()




        #sound = playsound(alm_file)
        #time.sleep(min(4,sound.seconds()))

class Timer:
    def __init__(self, hours, minutes,  seconds):
        print('timer running')
        seconds = int(seconds)
        minutes = int(minutes)
        hours = int(hours)

        seconds_rnd = self.round_time(seconds, 'sec')
        minutes += self.min_carryover
        minutes_rnd = self.round_time(minutes, 'min')
        hours += self.hr_carryover
        hours_rnd = self.round_time(hours, 'hour')

        print(hours_rnd, minutes_rnd, seconds_rnd, 'hour_rnd, min_rnd, sec_rnd')

        time_delay = '01/','01/','1901,' ' ', str(hours_rnd), ":",str(minutes_rnd), ":", str(seconds_rnd)
        time_str = ''.join(time_delay)
        print(time_str, 'time-str') #this is not going to reflect carryover yet
        self.end_time = dt.strptime(time_str, "%m/%d/%Y, %H:%M:%S")


        now = dt.now()

        self.end_time = now.replace(              #glitch here. we are adding time. if the timer extends to next day, it will throw an error, >23hours total
            microsecond=0,
            second=self.add_time(self.end_time.time().second,
                now.time().second,
                'sec'),
            minute= self.add_time(self.end_time.time().minute,
                now.time().minute,
                self.min_carryover,
                'min'),
            hour= self.add_time(self.end_time.time().hour,
                now.time().hour,
                self.hr_carryover,
                'hr'),
            day=self.day_carryover + now.day
            )

        if app.add_sec.get() != 0: self.add_to_end_time()

    def add_to_end_time(self):

        self.end_time = self.end_time.replace(microsecond = self.end_time.microsecond,
            second = self.add_time(self.end_time.second, self.round_time(int(app.add_sec.get()), 'sec')),
            minute = self.add_time(self.end_time.minute, self.min_carryover, 'min'),
            hour= self.add_time(self.end_time.hour, self.hr_carryover, 'hr'), day = self.end_time.day)
         #this is not well done. min_carryover just changed because I re-ran round wiht seconds. it works, but i have to be careful

    def round_time(self, time, type):
        if type == 'sec':

            if int(time) > 59:
                time = self.carryover_fn(time, 'sec')

            else:
                self.min_carryover = 0
            #minutes = minutes + self.min_carryover
            return(time)

        if type == 'min':
            if time > 59:
                time = self.carryover_fn(time, 'min')
            else:
                self.hr_carryover = 0
            return(time)

        if type == 'hour':
            if time > 23:
                 #this is to fit the next line on the screen
                print('running!!!!!!!!!!!!!!!!!!!$$$$$')
                string = "Error: Timer duration \n must be under 24 hours"
                app.print_error(string) #this stops the timer too!
                app.play_audio('Windows Notify System Generic.wav', 1)
                 #this is something I did not directly right stop for and was surprised that I had it in my arsenal.
                return(1)#A dummy int that won't raise an error. I know there's risk, but the timer is being stopped


            else:
                return(time)

    def add_time(self, *argv):
        lst = []
        for arg in argv:
            lst.append(arg)
        time_type = lst.pop()
        sum_arg = sum(lst)
        sum_arg = self.carryover_fn(sum_arg, time_type)
        #self.time_at_end_setter()
        return(sum_arg)

    def carryover_fn(self, time, time_type):
        time = int(time)
        if time_type == "hr":
            if time > 23:
                carryover = math.floor(time / 24)
                time = time % 24
            else:
                carryover = 0
        else:
            if time > 59:
                carryover = math.floor(int(time) / 60) #returns the number of minutes if seconds was entered (vice versa)
                if carryover > 59:
                    self.carryover_fn(carryover, min)
                time = time % 60 #returns modulo which will be number of seconds if seconds was entered. Minutes if minutes was entered

            else:
                carryover = 0
        if time_type == 'sec':
            self.min_carryover = carryover
        elif time_type == 'min':
            self.hr_carryover = carryover

        elif time_type == 'hr':
            self.day_carryover = carryover
        else:
            print("unknown time type")
            print('the time type is: ', time_type)

        return(time)




root = tk.Tk()

app = Application(master=root)
root.bind('<Return>', lambda start: app.start(button_press = True))
root.protocol("WM_DELETE_WINDOW", app.ask_on_close)
#root.lift()
#root.attributes('-topmost', True)
#root.attributes('-topmost', False)


app.mainloop()

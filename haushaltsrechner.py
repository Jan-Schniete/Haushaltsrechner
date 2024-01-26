# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 17:09:08 2023

@author: jschn
"""

import tkinter as tk
from tkinter import filedialog as fd


class Haushaltsrechner(tk.Frame):
    def __init__(self, master):
        """
        Initialising the main window of the application and populating it with
        the menu, layout and widgets. Also sets default values and parameters
        for the application layout and content.

        Parameters
        ----------
        master : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        super().__init__(master)     
        self.pack()
        self.__makeMenu(master)
        self.__createLayout()
        self.__createWidgets()
        self.__textwidth
        self.__numwidth
        self.__padding
    
    __default_income_name = "Einkommen eintragen"
    __default_spending_name = "Ausgabe eintragen"
    __default_amount = 0.00
    __textwidth = 40
    __numwidth = 10
    __padding = 10
    
    def __makeMenu(self, master):
        """
        Function to create the drop-down menu of the application.

        Parameters
        ----------
        master : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.__menuBar = tk.Menu(master)
        master.config(menu=self.__menuBar)
        self.__menuFile = tk.Menu(self.__menuBar, tearoff=False)
        self.__menuFile.add_command(
            label="Neue Haushaltsrechnung", command=self.__reset)
        self.__menuFile.add_command(
            label="Rechnung aus Datei öffnen ...", command=self.__openFile)
        self.__menuFile.add_command(
            label="Rechnung in Datei speichern ...", command=self.__saveFile)
        self.__menuFile.add_command(
            label="Beenden", command=self.__closeProgram)
        self.__menuBar.add_cascade(label="Datei", menu=self.__menuFile)
    
    def __createLayout(self):
        """
        Creating the frame layout with all the nested frames

        Returns
        -------
        None.

        """
        self.__top_frame = tk.Frame()
        self.__bottom_frame = tk.LabelFrame(text="Überschuss")
        self.__left_hand_side = tk.LabelFrame(
            self.__top_frame, text="Einkommen")
        self.__right_hand_side = tk.LabelFrame(
            self.__top_frame, text="Ausgaben")
        self.__entry_frame_left = tk.Frame(self.__left_hand_side)
        self.__footerframe_left = tk.Frame(self.__left_hand_side)
        self.__centreframe_left = tk.Frame(self.__left_hand_side)
        self.__button_frame_left = tk.Frame(self.__left_hand_side)
        self.__entry_frame_right = tk.Frame(self.__right_hand_side)
        self.__button_frame_right = tk.Frame(self.__right_hand_side)
        self.__centreframe_right = tk.Frame(self.__right_hand_side)
        self.__footerframe_right = tk.Frame(self.__right_hand_side)
        self.__top_frame.pack(fill="both", expand=True)
        self.__bottom_frame.pack(
            fill="x", padx=self.__padding, pady=self.__padding)
        self.__left_hand_side.pack(
            side="left", fill="both", padx=self.__padding, pady=self.__padding)
        self.__right_hand_side.pack(
            side="right", fill="both", padx=self.__padding, pady=self.__padding
            )
        self.__entry_frame_left.pack(fill="x")
        self.__button_frame_left.pack(fill="x")
        self.__centreframe_left.pack(expand=True, fill="both")
        self.__footerframe_left.pack(fill="x")
        self.__entry_frame_right.pack(fill="x")
        self.__button_frame_right.pack(fill="x")
        self.__centreframe_right.pack(expand=True, fill="both")
        self.__footerframe_right.pack(fill="x")
        
    def __createWidgets(self):
        """
        Function to create all the application widgets, assigning them to their
        respective frames and packing everything together

        Returns
        -------
        None.

        """
        # Definding the default entries for the inputs
        self.__income_name = tk.StringVar(value=self.__default_income_name)
        self.__income_amount = tk.StringVar(value=self.__default_amount)
        self.__spending_name = tk.StringVar(value=self.__default_spending_name)
        self.__spending_amount = tk.StringVar(value=self.__default_amount)
        
        # Everything in the left and right entry frames
        self.__entry_income_entry = tk.Entry(
            self.__entry_frame_left, width=self.__textwidth)
        self.__entry_income_entry["textvariable"] = self.__income_name
        self.__entry_income_amount = tk.Entry(
            self.__entry_frame_left, width=self.__numwidth)
        self.__entry_income_amount["textvariable"] = self.__income_amount
        self.__entry_spending_entry = tk.Entry(
            self.__entry_frame_right, width=self.__textwidth)
        self.__entry_spending_entry["textvariable"] = self.__spending_name
        self.__entry_spending_amount = tk.Entry(
            self.__entry_frame_right, width=self.__numwidth)
        self.__entry_spending_amount["textvariable"] = self.__spending_amount
        
        # Everything in the centre frame with the listboxes
        self.__scb_income_scrollbar = tk.Scrollbar(
            self.__centreframe_left, orient="vertical")
        self.__lstbx_income_list = tk.Listbox(
            self.__centreframe_left,
            width=self.__textwidth, selectmode="extended")
        self.__lstbx_income_amount = tk.Listbox(
            self.__centreframe_left,
            width=self.__numwidth, selectmode="extended")
        self.__scb_spending_scrollbar = tk.Scrollbar(
            self.__centreframe_right, orient="vertical")
        self.__lstbx_spending_list = tk.Listbox(
            self.__centreframe_right,
            width=self.__textwidth, selectmode="extended")
        self.__lstbx_spending_amount = tk.Listbox(
            self.__centreframe_right,
            width=self.__numwidth, selectmode="extended")
        self.__lbl_income_result = tk.Label(
            self.__footerframe_left, text="Summe aller Einkommen:")
        self.__lbl_income_sum = tk.Label(
            self.__footerframe_left, text="0.00")
        self.__lbl_spending_result = tk.Label(
            self.__footerframe_right, text="Summe aller Ausgaben:")
        self.__lbl_spending_sum = tk.Label(
            self.__footerframe_right, text="0.00")
        self.__lbl_overall_balance_text = tk.Label(
            self.__bottom_frame, text="Einkommen minus Ausgaben:")
        self.__lbl_overall_balance_result = tk.Label(
            self.__bottom_frame, text = "0.00")
        
        # The buttons
        self.__btn_add_income = tk.Button(
            self.__button_frame_left,
            text="Einkommen hinzufügen", command=self.__addIncome)
        self.__btn_delete_income = tk.Button(
            self.__button_frame_left,
            text="Einkommen löschen", command=self.__deleteIncome)
        self.__btn_move_income_up = tk.Button(
            self.__button_frame_left,
            text="\u2191", command=self.__move_income_up)
        self.__btn_move_income_down = tk.Button(
            self.__button_frame_left,
            text="\u2193", command=self.__move_income_down)
        self.__btn_add_spending = tk.Button(
            self.__button_frame_right,
            text="Ausgabe hinzufügen", command=self.__addSpending)
        self.__btn_delete_spending = tk.Button(
            self.__button_frame_right,
            text="Ausgabe löschen", command=self.__deleteSpending)
        self.__btn_move_spending_up = tk.Button(
            self.__button_frame_right,
            text="\u2191", command=self.__move_spending_up)
        self.__btn_move_spending_down = tk.Button(
            self.__button_frame_right,
            text="\u2193", command=self.__move_spending_down)
        
        # Packing all widgets in their frames
        self.__entry_income_entry.pack(
            side="left", padx=self.__padding, pady=self.__padding)
        self.__entry_income_amount.pack(
            side="left", padx=self.__padding, pady=self.__padding)
        self.__entry_spending_entry.pack(
            side="left", padx=self.__padding, pady=self.__padding)
        self.__entry_spending_amount.pack(
            side="left", padx=self.__padding, pady=self.__padding)
        self.__btn_add_income.pack(
            side="left", padx=self.__padding, pady=self.__padding)
        self.__btn_move_income_up.pack(
            side="left", padx=self.__padding, pady=self.__padding)
        self.__btn_move_income_down.pack(
            side="left", padx=self.__padding, pady=self.__padding)
        self.__btn_delete_income.pack(
            side="right", padx=self.__padding, pady=self.__padding)
        self.__btn_add_spending.pack(
            side="left", padx=self.__padding, pady=self.__padding)
        self.__btn_move_spending_up.pack(
            side="left", padx=self.__padding, pady=self.__padding)
        self.__btn_move_spending_down.pack(
            side="left", padx=self.__padding, pady=self.__padding)
        self.__btn_delete_spending.pack(
            side="right", padx=self.__padding, pady=self.__padding)
        self.__lstbx_income_list.pack(
            side="left", fill="y", padx=self.__padding, pady=self.__padding)
        self.__lstbx_income_amount.pack(
            side="left", fill="y", padx=self.__padding, pady=self.__padding)
        self.__scb_income_scrollbar.pack(
            side="left", fill="y", padx=self.__padding, pady=self.__padding)
        self.__lstbx_spending_list.pack(
            side="left", fill="y", padx=self.__padding, pady=self.__padding)
        self.__lstbx_spending_amount.pack(
            side="left", fill="y", padx=self.__padding, pady=self.__padding)
        self.__scb_spending_scrollbar.pack(
            side="left", fill="y", padx=self.__padding, pady=self.__padding)
        self.__lbl_income_result.pack(
            side="left", padx=self.__padding, pady=self.__padding)
        self.__lbl_income_sum.pack(
            side="right", padx=self.__padding, pady=self.__padding)
        self.__lbl_spending_result.pack(
            side="left", padx=self.__padding, pady=self.__padding)
        self.__lbl_spending_sum.pack(
            side="right", padx=self.__padding, pady=self.__padding)
        self.__lbl_overall_balance_text.pack(
            side="left", padx=self.__padding, pady=self.__padding)
        self.__lbl_overall_balance_result.pack(
            side="right", padx=self.__padding, pady=self.__padding)
    
    def __addIncome(self):
        """
        Function to add an income name and amount to respective listboxes.
        Income name and amount are grabbed from the input fields and reset to
        default values after addition.

        Returns
        -------
        None.

        """
        try:
            name = self.__income_name.get()
            amount = float(self.__income_amount.get())
            if name == "":
                return None
        except ValueError:
            tk.messagebox.showerror(
                title="Kleiner Fehler!",
                message="Eingegebener Betrag wurde nicht als Zahl erkannt.")
            return None
        self.__lstbx_income_list.insert(tk.END, name)
        self.__lstbx_income_amount.insert(tk.END, "{:.2f}".format(amount))
        self.__income_name.set(self.__default_income_name)
        self.__income_amount.set(self.__default_amount)
        self.__updateResult()
    
    def __deleteIncome(self):
        """
        This Funtion deletes the items currently selected in the income listbox
        from both the income listbox and the income amount listbox. Selection
        is cleared after deletion.

        Returns
        -------
        None.

        """
        entries = self.__lstbx_income_list.curselection()
        self.__lstbx_income_list.selection_clear(0, tk.END)
        entries = list(entries)
        entries.reverse()
        for entry in entries:
            self.__lstbx_income_list.delete(entry)
            self.__lstbx_income_amount.delete(entry)
        self.__updateResult()
        
    def __move_income_up(self):
        """
        Moves the items currently selected in the income listbox up one spot.
        Also moves the respective income amounts in the income amount listbox.

        Returns
        -------
        None.

        """
        entries = self.__lstbx_income_list.curselection()
        self.__lstbx_income_list.selection_clear(0, tk.END)
        entries = list(entries)
        for i, entry in enumerate(entries):
            if entry == 0:
                break
            current_entry_name = self.__lstbx_income_list.get(entry)
            current_entry_amount = self.__lstbx_income_amount.get(entry)
            self.__lstbx_income_list.delete(entry)
            self.__lstbx_income_list.insert(entry-1, current_entry_name)
            self.__lstbx_income_amount.delete(entry)
            self.__lstbx_income_amount.insert(entry-1, current_entry_amount)
            entries[i] -= 1
            self.__lstbx_income_list.selection_set(entries[i])
        
    def __move_income_down(self):
        """
        Moves the items currently selected in the income listbox down one spot.
        Also moves the respective income amounts in the income amount listbox.

        Returns
        -------
        None.

        """
        list_size = self.__lstbx_income_list.size()
        entries = self.__lstbx_income_list.curselection()
        self.__lstbx_income_list.selection_clear(0, tk.END)
        entries = list(entries)
        entries.reverse()
        for i, entry in enumerate(entries):
            if entry == list_size - 1:
                break
            current_entry_name = self.__lstbx_income_list.get(entry)
            current_entry_amount = self.__lstbx_income_amount.get(entry)
            self.__lstbx_income_list.insert(entry+2, current_entry_name)
            self.__lstbx_income_list.delete(entry)
            self.__lstbx_income_amount.insert(entry+2, current_entry_amount)
            self.__lstbx_income_amount.delete(entry)
            entries[i] += 1
            self.__lstbx_income_list.selection_set(entries[i])
            
    def __addSpending(self):
        """
        Function to add a spending name and amount to respective listboxes.
        Spending name and amount are grabbed from the input fields and reset to
        default values after addition.

        Returns
        -------
        None.

        """
        try:
            name = self.__spending_name.get()
            amount = float(self.__spending_amount.get())
            if name == "":
                return None
        except ValueError:
            tk.messagebox.showerror(
                title="Kleiner Fehler!",
                message="Eingegebener Betrag wurde nicht als Zahl erkannt.")
            return None
        self.__lstbx_spending_list.insert(tk.END, name)
        self.__lstbx_spending_amount.insert(tk.END, amount)
        self.__spending_name.set(self.__default_spending_name)
        self.__spending_amount.set(self.__default_amount)
        self.__updateResult()
    
    def __deleteSpending(self):
        """
        This Funtion deletes the items currently selected in the spending
        listbox from both the income listbox and the income amount listbox.
        Selection is cleared after deletion.

        Returns
        -------
        None.

        """
        entries = self.__lstbx_spending_list.curselection()
        self.__lstbx_spending_list.selection_clear(0, tk.END)
        entries = list(entries)
        entries.reverse()
        for entry in entries:
            self.__lstbx_spending_list.delete(entry)
            self.__lstbx_spending_amount.delete(entry)
        self.__updateResult()
        
    def __move_spending_up(self):
        """
        Moves the items currently selected in the spending listbox up one spot.
        Also moves the respective spending amounts in the spending amount
        listbox.

        Returns
        -------
        None.

        """
        entries = self.__lstbx_spending_list.curselection()
        self.__lstbx_spending_list.selection_clear(0, tk.END)
        entries = list(entries)
        for i, entry in enumerate(entries):
            if entry == 0:
                break
            current_entry_name = self.__lstbx_spending_list.get(entry)
            current_entry_amount = self.__lstbx_spending_amount.get(entry)
            self.__lstbx_spending_list.delete(entry)
            self.__lstbx_spending_list.insert(entry-1, current_entry_name)
            self.__lstbx_spending_amount.delete(entry)
            self.__lstbx_spending_amount.insert(entry-1, current_entry_amount)
            entries[i] -= 1
            self.__lstbx_spending_list.selection_set(entries[i])
        
    def __move_spending_down(self):
        """
        Moves the items currently selected in the spending listbox down one
        spot. Also moves the respective income spending in the spending amount
        listbox.

        Returns
        -------
        None.

        """
        list_size = self.__lstbx_spending_list.size()
        entries = self.__lstbx_spending_list.curselection()
        self.__lstbx_spending_list.selection_clear(0, tk.END)
        entries = list(entries)
        entries.reverse()
        for i, entry in enumerate(entries):
            if entry == list_size - 1:
                break
            current_entry_name = self.__lstbx_spending_list.get(entry)
            current_entry_amount = self.__lstbx_spending_amount.get(entry)
            self.__lstbx_spending_list.insert(entry+2, current_entry_name)
            self.__lstbx_spending_list.delete(entry)
            self.__lstbx_spending_amount.insert(entry+2, current_entry_amount)
            self.__lstbx_spending_amount.delete(entry)
            entries[i] += 1
            self.__lstbx_spending_list.selection_set(entries[i])
    
    def __updateResult(self):
        """
        Updates the result of the income minus spending calculation and sets
        the colour for positive (green) and negative (red) outcome.

        Returns
        -------
        None.

        """
        income_sum = sum(
            [float(item) for item in
             self.__lstbx_income_amount.get(0, tk.END)])
        spending_sum = sum(
            [float(item) for item in
             self.__lstbx_spending_amount.get(0, tk.END)])
        result = income_sum - spending_sum
        self.__lbl_income_sum["text"] = "{:.2f}".format(income_sum)
        self.__lbl_spending_sum["text"] = "{:.2f}".format(spending_sum)
        self.__lbl_overall_balance_result["text"] = "{:.2f}".format(result)
        self.__income_name.set(self.__default_income_name)
        self.__spending_name.set(self.__default_spending_name)
        self.__income_amount.set(self.__default_amount)
        self.__spending_amount.set(self.__default_amount)
        if result < 0:
            self.__lbl_overall_balance_result["foreground"] = "red"
        else:
            self.__lbl_overall_balance_result["foreground"] = "green"
            
    def __reset(self):
        """
        Deletes all income and spending entries, resetting the application to
        its original state.

        Returns
        -------
        None.

        """
        self.__lstbx_income_list.delete(0, tk.END)
        self.__lstbx_income_amount.delete(0, tk.END)
        self.__lstbx_spending_list.delete(0, tk.END)
        self.__lstbx_spending_amount.delete(0, tk.END)
        self.__updateResult()
        
    def __openFile(self):
        """
        Opens a .txt file with income and spending names and their amounts.
        Format should be thus: Any line in the file should have income first
        with amount and then spending, 4 entries total with tab delimitatin.
        The below line serves as illustration.
        
        'income name'/t'income amount'/t'spending name'/t'spending amount'/n
        
        The contents of the file are added to the income and spending listboxes
        with the amounts and the result is calculated.
        
        Returns
        -------
        None.

        """
        file = fd.askopenfile(mode="r", filetypes=[("Text files", ".txt")])
        content = file.readlines()
        content = [line.split(sep="\t") for line in content]
        while content:
            self.__income_name.set(content[0][0])
            self.__income_amount.set(content[0][1])
            self.__addIncome()
            self.__spending_name.set(content[0][2])
            self.__spending_amount.set(content[0][3])
            self.__addSpending()
            content.pop(0)
        file.close()
                
    def __saveFile(self):
        """
        Saves the current items and amounts for income and spending in a .txt
        file with four tab delimited items per line. The below line serves as
        illustration.
        
        'income name'/t'income amount'/t'spending name'/t'spending amount'/n

        Returns
        -------
        None.

        """
        file = fd.asksaveasfile("w", filetypes=[("Text files", ".txt")])
        longest_lstbx = max(
            self.__lstbx_income_list.size(), self.__lstbx_spending_list.size())
        i = 0
        while i < longest_lstbx:
            if self.__lstbx_income_list.get(i):
                income_name = self.__lstbx_income_list.get(i)
                income_amount = str(self.__lstbx_income_amount.get(i))
            else:
                income_name = ''
                income_amount = '0'
            if self.__lstbx_spending_list.get(i):
                spending_name = self.__lstbx_spending_list.get(i)
                spending_amount = str(self.__lstbx_spending_amount.get(i))
            else:
                spending_name = ''
                spending_amount = '0'
            output_line = (
                "\t".join([income_name, income_amount,
                           spending_name, spending_amount]))
            i += 1
            file.write(output_line + "\n")
        file.close()
        
    def __closeProgram(self):
        """
        Shuts the program down and destroys the master window.

        Returns
        -------
        None.

        """
        self.master.quit()
        self.master.destroy()
            

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Haushaltsrechner")
    rechner = Haushaltsrechner(root)
    rechner.mainloop()
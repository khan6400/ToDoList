import re
import os
import sys

def handle_input():
    enteries = []
    i = 1
    use_bullets = input("Use bullet points: Yes/No? ").strip()
    if use_bullets.lower() in ["yes", "y"]:
        bullet_point = input("Enter bullet point style: ")
    else:
        print("Continuing without using bullet points")
        bullet_point = ""
    while True:
        usr_inp = input(f"Entry #{i}: ")
        if usr_inp.lower() in ["quit", "exit"]:
            break
        else:
            enteries.append(bullet_point + usr_inp)
        i += 1
    return enteries

def save_enteries(file_select, enteries):
    if file_select.isdigit():
        file_select = int(file_select)
        entry_files = list_notes()
        opened_file = entry_files[file_select]
        with open(opened_file, "a+") as file:
            for stuff in enteries:
                file.write(str(stuff + "\n"))
    else:
        if not file_select.lower().endswith(".txt"):
            file_select += ".txt"
        with open(file_select, "a+") as file:
            for stuff in enteries:
                file.write(str(stuff + "\n"))
    print(f"\n***Saved to {file_select}!***")

def notes_save():
        enteries = handle_input()
        list_notes()
        try:
            file_select = input("\nSelect file or enter filename to create new one: ")        
            if os.path.exists(file_select):
                save_enteries(file_select, enteries)
            else:
                save_notes_selector(file_select, enteries)
        except Exception as excp:
            print(f"ERROR= {excp}")

def save_notes_selector(file_select, enteries):
    while True:
        try:
            if_to_create_file = int(input("File doesnt exist...Press: '1' create new file with name entered or '2' to append to existing file: "))
            if if_to_create_file == 1:
                save_enteries(file_select, enteries)
                break
            elif if_to_create_file == 2:
                entry_files = list_notes()
                choice = int(input("Select which file to add to"))
                if 1 <= choice <= len(entry_files):
                    file_to_open = entry_files[choice - 1]
                    save_enteries(file_to_open, enteries)
                    break        
                else:
                    print(f"Please enter numbers only from 1 to {len(entry_files)} ")
            else:
                print("Please only enter 1 or 2") 
        except ValueError:
            print("Please enter only numbers")
        

def list_notes():
    lis = list(os.listdir())
    entery_files = []
    for file in lis:
        if file.lower().endswith(".txt"):
            entery_files.append(file)
    print("*************************************\nCurrent Notes:")
    number = 1
    for x in entery_files:
        print(f"{number}. {x}")
        number += 1
    print("\n*************************************")
    return entery_files

def append_to_file():
    entry_files = list_notes()
    while True: 
        try:
            choice = int(input("Select which file to add to: "))
            if 1 <= choice <= len(entry_files):
                file_to_open = entry_files[choice - 1]
                enteries = handle_input()
                save_enteries(file_to_open, enteries)
                break
            else:
                print(f"Please enter numbers only from 1 to {len(entry_files)} ")
        except ValueError:
            print("Please enter only numbers")

def delete_file():
    list_of_files = list_notes()
    while True:
        try:
            file_select = input("Select file to delete or 'back' to go back: ")
            if file_select.lower() in ["back", "exit", "quit"]:
                break
            elif file_select.isdigit():
                file_select = int(file_select)
                if 1<= file_select <= len(list_of_files):
                    os.remove(list_of_files[file_select - 1])
                    print(f"File no.{file_select} has been deleted!")
            else:
                if not file_select.lower().endswith(".txt"):
                    file_select += ".txt"
                os.remove(file_select)
                print(f"File '{file_select}' has been deleted!")
        except Exception as excp:
            print(f"ERROR: {excp}")

def read_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    print(content)

def view_notes_file():
    while True:
        try:
            files_list = list_notes()
            file_select = input("Select file to view: ")
            if file_select.isdigit(): 
                file_select_digit = int(file_select) - 1
                selected_file = files_list[file_select_digit]
                read_file(selected_file)
                view_again = input("View another file? (Y)es/(N)o: ")
                if view_again.lower() not in ["yes", "y"]:
                    break
            elif file_select == "":
                print("Please enter the number or name of file to view")
            else:
                if file_select.lower().endswith(".txt"):
                    selected_file = file_select
                else:
                    selected_file = file_select + ".txt"
                if os.path.exists(selected_file):
                    read_file(selected_file)
                view_again = input("View another file? (Y)es/(N)o: ")
                if view_again.lower() not in ["yes", "y"]:
                    break
                else:
                    print(f"{selected_file} doesnt exist!")
                    continue
        except Exception as exc:
            print(f"Error: {exc}")    

def search_in_file(called_from = None):
    results = []
    found_any = False
    result_num = 1
    directory = os.listdir()
    search_term = input("Enter term to search or 'back' to go back: ")
    print(f"Searching for {search_term}...")
    if search_term.lower() == "back":
                print("Going back...")
                main_program()
    with open("search_results.csv", "w") as clear_file:
        clear_file.write("")
    for file in directory:
        if file.lower().endswith(".txt"):
            try:
                with open(file, "r") as open_file:
                    for line_no, line in enumerate(open_file, start=1):
                        if search_term.lower() in line.lower():
                            conclusion = (f"{result_num}) Search term '{search_term}' found at line number {line_no} in '{file}'")
                            if called_from == None:
                                print(conclusion)
                            results.append(conclusion)
                            result_num +=1
                            with open("search_results.csv", "a+") as search_results:
                                search_results.write(str(conclusion+"\n"))
                            found_any = True
            except Exception as e:
                print(f"Error: {e}")
    print("Results saved to 'search_results.csv'")
    
    if not found_any:
            print(f"Didn't find '{search_term}'")
    return results

def edit_entry():
    results = list(search_in_file())    
    select_result = input("Select result to edit or 'back' to go back: ")
    if select_result.lower() == "back":
                main_program()
    if select_result.isdigit():
        select_result = int(select_result) - 1
        selected = (results[select_result])
        filename = selected.split("'")[-2]
        line_to_edit = int(re.findall(r"\d+", selected)[-1]) - 1
        edited_line = input("Enter new task or Press enter to delete this task: ").strip()
        with open (filename, "r") as file:
            file_lines = file.readlines()
            if edited_line == "":
                del file_lines[line_to_edit]
                print(f"Entryhas been updated to {edited_line}")

            else:
                file_lines[line_to_edit] = edited_line
                print(f"Entry has been deleted!")
        with open (filename, "w") as file:
            file.writelines(file_lines)
    else:
        print("Please enter numbers to select the entry to edit")    

def main_program():
    while True:
            user_select = input("*************************************\nEnter Number to continue: \n '1' to make new file \n '2' to add to file \n '3' to delete a file \n '4' to view a file \n '5' to list all files \n '6' to search \n '7' to upadate/delete task \n Type exit or quit to exit\n*************************************\n Select= ").strip()
            if user_select.lower() in ["quit", "exit"]:
                print("Exiting...")
                sys.exit()
            if user_select.isdigit():
                user_select = int(user_select)
                if user_select == 1:
                    notes_save()
                elif user_select == 2:
                    append_to_file()
                elif user_select == 3:
                    delete_file()
                elif user_select == 4:
                    view_notes_file()
                elif user_select == 5:
                    list_notes()
                elif user_select == 6:
                    search_in_file()
                elif user_select == 7:
                    edit_entry()
                else:
                    print("Please only enter 1-7 numbers")
            
            else:
                print("Please Enter only numbers!")
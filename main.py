import os
import json


def cls():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def introduction():
    cls()
    print("""
                            ******************************************************
                                Welcome to Simple Grocery List Management Tool
                            ******************************************************
                      This tools helps to Add , View, Update , Delete an item and or clear entire items.
                      It also stores the items managed to file. You can sort those items by Name, Quantity,
                      filter by Category or availability.
    """)


def operations():
    print('''
                             List of Operations
                             --------------------
                              1. Add an Item
                              2. View Items
                              3. Update Item
                              4. Delete an Item
                              5. Search an Item
                              6. Sort Items
                              7. Notify Items
                              8. Clear ALL Items
                              9. Exit
    ''')


def check_item(item):
    return item in items


def display_category():
    print('\n\t\t\t\t Categories')
    print('\n\t\t\t\t------------')
    for index, category in enumerate(list(categories.items())):
        print(f'\t\t\t\t{index+1}. {category[0]}')
    print('')


def view_items(items_data):
    print('\n\t\t\t\t\t\t View Items')
    print('\t\t\t\t\t\t------------\n')
    print('\t\t\t\tS.No.  Name                 Qty  Category        Notify Qty')
    print('\t\t\t\t----- -------------------- ----- --------------- ----------')
    for index, item_details in enumerate(list(items_data.items())):
        print(f'\t\t\t\t{str(index+1).rjust(4)[:4]}  {str(item_details[0]).ljust(20)[:20]} '
              f'{str(item_details[1][0]).rjust(4)[:4]}   {get_category_name(item_details[1][1]).ljust(15)[:15]}   '
              f'{str(item_details[1][2]).rjust(4)[:4]}')
    print('')


def search_item():
    view_items(items)
    print()
    print('\n\t\t\t\t Search an Item')
    print('\t\t\t\t----------------')
    item_name = input('\t\t\t Enter the Item Name : ')
    if item_name not in items:
        print(f'\n\t\t\t\t {item_name} does not exist.')
    else:
        display_an_item(item_name)


def display_an_item(item_name):
    print('\n\t\t\t\t Name                 Qty  Category        Notify Qty')
    print('\t\t\t\t-------------------- ----- --------------- ----------')
    print(f'\t\t\t\t{item_name.ljust(20)[:20]} {str(items[item_name][0]).rjust(4)[:4]}  '
          f'{get_category_name(items[item_name][1]).ljust(15)[:15]}    {items[item_name][2]}')


def add_item():
    print('\n\t\t\t\t Add an Item')
    print('\t\t\t\t-------------')

    while True:
        item_name = input('\t\t\tEnter an Item Name/ (E) to Exit: ')
        if item_name.upper() == 'E':
            break
        if check_item(item_name):
            print(f'\t\t\t\t"{item_name}" already exists. Please enter any other Name.')
        else:
            break

    if item_name.upper() == 'E':
        return

    print()
    item_quantity = get_quantity()
    while True:
        category = get_category()
        if 0 < category <= len(categories):
            break
    item_category = categories[list(categories)[int(category) - 1]]
    print()

    while True:
        print('\t\t\tFor notification of the Item')
        item_notify = get_quantity()
        if item_notify <= item_quantity:
            break
        else:
            print(f'\t\t\t\tNotify quantity {item_notify} is more than Item quantity {item_quantity}')

    items[item_name] = [item_quantity, item_category, item_notify]
    database['Items'] = items
    write_data()
    print('\n\t\t\t\t*** Item added ***')


def update_item():
    view_items(items)
    print('\n\t\t\t\t Update an Item')
    print('\t\t\t\t----------------')

    while True:
        item_name = input('\t\t\t Enter an Item Name/ (E) to Exit: ')
        if item_name.upper() == 'E':
            break
        if check_item(item_name):
            print()
            display_an_item(item_name)
            print()
            break
        else:
            print(f'\t\t\t\t"{item_name}" does not exist. Please enter any other Name.')

    if item_name.upper() == 'E':
        return

    item_quantity = get_quantity()
    while True:
        category = get_category()
        if 0 < category <= len(categories):
            break
    item_category = categories[list(categories)[int(category) - 1]]

    print('\t\t\tFor notification of the Item')
    item_notify = get_quantity()

    items[item_name] = [item_quantity, item_category, item_notify]
    database['Items'] = items
    write_data()
    print('\n\t\t\t\t*** Item updated ***')


def delete_item():
    view_items(items)
    print('\n\t\t\t\t Delete an Item')
    print('\t\t\t\t-----------------')

    while True:
        item_name = input('\t\t\t Enter an Item Name/ (E) to Exit: ')
        if item_name.upper() == 'E':
            break
        if check_item(item_name):
            print()
            display_an_item(item_name)
            print()
            break
        else:
            print(f'\t\t\t\t"{item_name}" does not exist. Please enter any other Name.')

    if item_name.upper() == 'E':
        return

    confirm = input('\t\t\t DELETE Confirmation Y/N ? ').strip().upper()
    if confirm == 'Y':
        del items[item_name]
        database['Items'] = items
        write_data()
        print(f'\n\t\t\t\t*** Item "{item_name}" deleted ***')


def get_quantity():
    while True:
        quantity = input('\t\t\tEnter the quantity : ')
        if quantity.isdigit():
            quantity = int(quantity)
            break
        else:
            print('\t\t\t\t\tPlease enter a number.')
    return quantity


def get_category():
    display_category()
    while True:
        category = input('\t\t\tChoose the Category of the Item : ')
        if category.isdigit():
            category = int(category)
            break
    return category


def get_category_name(value):
    return list(categories.keys())[list(categories.values()).index(value)]


def read_data():

    with open('grocery_data.json') as f:
        dbase = json.load(f)
        if 'Items' not in dbase:
            dbase['Items'] = {}
        if 'Categories' not in dbase:
            dbase['Categories'] = {}

    return dbase


def write_data():
    json_object = json.dumps(database)

    with open("Grocery_data.json", "w") as outfile:
        outfile.write(json_object)


def clear_all_items():
    if not len(items):
        print(f'\n\t\t\t\t*** No Items available ***')
        return

    confirm = input('\n\t\t\tDELETE ALL ITEMS. Can not recover data!!!. Confirmation Y/N ? ').strip().upper()
    if confirm == 'Y':
        database['Items'] = dict()
        write_data()
        print(f'\n\t\t\t\t*** ALL Items are deleted ***')


def sort_items():
    print('\n\t\t\t\tSort all Items by')
    print('\t\t\t\t-----------------')
    print('\t\t\t\t1. Name')
    print('\t\t\t\t2. Quantity')
    print('\t\t\t\t3. Category')
    print('\t\t\t\t4. Exit')
    print('\n')

    while True:
        while True:
            option = input('\t\t\tChoose any option : ')
            if option.isdigit():
                option = int(option)
                break
        if option in [1, 2, 3, 4]:
            break

    if option == 1:
        print('\n\t\t\t\t\t\tSorted by Name\n')
        view_items(dict(sorted(items.items())))
    elif option == 2:
        print('\n\t\t\t\t\t\tSorted by Quantity\n')
        view_items(dict(sorted(items.items(), key=lambda x: x[1])))
    elif option == 3:
        print('\n\t\t\t\t\t\tSorted by Category\n')
        view_items(dict(sorted(items.items(), key=lambda x: x[1][1])))
    return


def notify_items():
    notify_dict = {item[0]: item[1] for item in items.items() if item[1][0] < item[1][2]}
    print('\n\t\t\t\t\t\tNotification Items')
    print('\t\t\t\t\t\t------------------')
    view_items(notify_dict)
    return notify_dict


if __name__ == '__main__':
    introduction()

    database = read_data()

    items = database['Items']
    categories = database['Categories']

    while True:
        operations()

        invalid = True
        op = ''
        while invalid:
            op = input('\t\t\tSelect any operation : ')
            invalid = not op.isdigit()

        op = int(op)

        if op == 9:
            break

        if op == 1:
            add_item()
        if op == 2:
            view_items(items)
        if op == 3:
            update_item()
        if op == 4:
            delete_item()
        if op == 5:
            search_item()
        if op == 6:
            sort_items()
        if op == 7:
            notify_items()
        if op == 8:
            clear_all_items()
            items = database['Items']

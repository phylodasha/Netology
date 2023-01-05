import re
import csv

with open("phonebook_raw.csv") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
new_contacts_list = [contacts_list[0]]

def reshape_phone(number):
    number = re.findall('[\d]+', number)

    number = ''.join(number)[1:]
    new_phone = '+7(' + number[:3] + ')' + number[3:6] + '-' + number[6:8] + '-' + number[8:10]
    if 'доб.' in phone[0]:
        new_phone += ' доб.' + (re.findall('[\d]+', number[10:]))[0]
    return new_phone

for contact in contacts_list[1:]:
    name = ' '.join([contact[0], contact[1], contact[2]])
    name = name.split(' ')
    lastname, firstname, surname = name[0], name[1], name[2]
    organization, position, phone, email = contact[3],contact[4],contact[5],contact[6]
    if len(phone) != 0:
        phone = reshape_phone(phone)
    new_contact = [lastname,firstname,surname,organization,position,phone,email]
    added = False
    for contact in range(len(new_contacts_list)):
        if new_contacts_list[contact][0] == new_contact[0]:
            for i in range(len(new_contacts_list[contact])):
                if len(new_contacts_list[contact][i]) == 0:
                    new_contacts_list[contact][i] = new_contact[i]
                    added = True
            break
    if not added:
        new_contacts_list.append(new_contact)

with open("phonebook.csv", "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(new_contacts_list)
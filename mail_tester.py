import requests
import uuid
import pypyodbc as odbc
import datetime


def generate_unique_id():
    random_uuid = uuid.uuid4()
    unique_id = "eml-" + str(random_uuid)
    return unique_id


def get_current_time():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_time_stripped = current_time.replace("-", "").replace(":", "").replace(" ", "")
    return current_time_stripped


def test_email(email):
    url = 'http://avatarapi.com/avatar.asmx/VerifyEmail'

    params = {'email': email}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.text
        print(data) 
        verification = data.strip()
        if 'FAIL' in verification:
            return 'FAIL'
        elif 'INCONCLUSIVE' in verification:
            return 'INCONCLUSIVE'
        elif 'SUCCESS' in verification:
            return 'SUCCESS'
    else:
        print(f'Request failed with status code {response.status_code}')


def create_email(first_name, last_name, domain):
    first_name = first_name.lower()
    last_name = last_name.lower()
    combinations=[
    first_name+'.'+ last_name+'@'+ domain,
    first_name +'@'+ domain,
    first_name[0]+'.'+last_name +'@'+ domain,
    first_name+last_name+'@'+ domain,
    first_name[0]+last_name[0]+'@'+ domain,
    first_name[0]+'.'+last_name[0]+'@'+ domain,
    first_name+last_name[0]+'@'+ domain,
    first_name[0]+last_name+'@'+ domain,
    first_name+'.'+last_name[0]+'@'+ domain,
    first_name[:4]+'.'+last_name+'@'+ domain,
    first_name[:4]+'@'+ domain,
    ]
    
    result = 'FAIL'
    for comb in combinations:
        result= test_email(comb)
        if result=='SUCCESS':
            print("Email found: ", comb)
            insert_data(first_name,comb)
            return comb
        else:
            print("No email found")
    
def insert_data(first_name,email):
    unique_id= generate_unique_id()
    current_time=get_current_time()
    query='INSERT INTO tblCompanyEmails (ID, ContactName, EmailAddress,IsActive,IsInValid,dtInsert,OwnerID) VALUES (?, ?, ?,1,0,?,CND7076Q5N)'
    cursor.execute(query,(unique_id,first_name,email,current_time))
    conn.commit()

DriverName = 'SQL Server'
ServerName = '192.168.0.207\CRM2017'
DatabaseName = 'KGNCRM'
Username = ''
Password = ''

connectionString = f"""
Driver={{{DriverName}}};
Server={ServerName};
Database={DatabaseName};
UID={Username};
PWD={Password};
"""

conn = odbc.connect(connectionString)

cursor = conn.cursor()

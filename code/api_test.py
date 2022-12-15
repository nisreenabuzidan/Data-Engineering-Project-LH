import os
import datetime

"""TEST_AUTHENTICATION = int(os.environ.get('TEST_AUTHENTICATION'))
TEST_AUTHORIZATION = int(os.environ.get('TEST_AUTHORIZATION'))
TEST_CONTENT = int(os.environ.get('TEST_CONTENT'))"""

#if (TEST_AUTHENTICATION ==1):
#import test_api


import os
import requests

# definition of the API address
 
api_address = os.environ.get("API_ADDRESS")  
api_port = os.environ.get("API_PORT")  

current_time=datetime.datetime.now()

#get log Env variable
print_log  =1 

# resquest
r = requests.get(
    url='http://{address}:{port}/'.format(address=api_address, port=api_port),
    
)
output = '''
============================
    Health Check at {current_time}
============================
request done at "/"
expected result = 200
actual restult = {status_code}
==>  {test_status}
'''

# query status
status_code = r.status_code

# display the results
if status_code == 200:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
    
print(output.format(current_time = current_time,status_code=status_code, test_status=test_status))
# printing in a file
if print_log == 1:
    with open('../logs/api_test.log', 'a') as file:
        file.write(output.format(current_time = current_time,status_code=status_code, test_status=test_status))



"=============================="
airport_code = ""
start_date = ""
end_date = ""


"==============================="
# resquest
r = requests.get(
    url='http://{address}:{port}/airport_latency_info?airport_code={airport_code}&start_date={start_date}&end_date={end_date}'.format(address=api_address, port=api_port,airport_code=airport_code,start_date=start_date,end_date=end_date),
    params= {
       "airport_code": 'FRA',
       "start_date": '2022-11-25',
       "end_date": '2022-12-01',
    }
    
)
output = '''
============================
    Get all flights and delayed flights between 2 dates
============================
request done at "/airport_latency_info"
airport_code ='FRA',
start_date ='2022-11-25',
end_date'= '2022-12-01',
expected result = 200
actual restult = {status_code}
==>  {test_status}
'''

# query status
status_code = r.status_code

# display the results
if status_code == 200:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
    
print(output.format(status_code=status_code, test_status=test_status))
# printing in a file
if print_log == 1:
    with open('../logs/api_test.log', 'a') as file:
        file.write(output.format(status_code=status_code, test_status=test_status))



"==============================="
# resquest
r = requests.get(
    url='http://{address}:{port}/airport_latency_info?airport_code={airport_code}&start_date={start_date}&end_date={end_date}'.format(address=api_address, port=api_port,airport_code=airport_code,start_date=start_date,end_date=end_date),
    params= {
       "airport_code": 'FRA',
       "start_date": '2022-12-01',
       "end_date": '2022-11-30',
    }
    
)
output = '''
============================
    Get all flights and delayed flights between 2 dates
============================
request done at "/airport_latency_info"
airport_code ='FRA',
start_date ='2022-12-01',
end_date'= '2022-11-30',
expected result = 400
actual restult = {status_code}
==>  {test_status}
'''

# query status
status_code = r.status_code

# display the results
if status_code == 400:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
    
print(output.format(status_code=status_code, test_status=test_status))
# printing in a file
if print_log == 1:
    with open('../logs/api_test.log', 'a') as file:
        file.write(output.format(status_code=status_code, test_status=test_status))

"==============================="
# resquest
r = requests.get(
    url='http://{address}:{port}/airport_latency_info?airport_code={airport_code}&start_date={start_date}&end_date={end_date}'.format(address=api_address, port=api_port,airport_code=airport_code,start_date=start_date,end_date=end_date),
    params= {
       "airport_code": 'FRA',
       "start_date": '2022-25-11',
       "end_date": '2022-12-01',
    }
    
)
output = '''
============================
    Get all flights and delayed flights between 2 dates
============================
request done at "/airport_latency_info"
airport_code ='FRA',
start_date ='2022-25-11',
end_date'= '2022-12-01',
expected result = 400
actual restult = {status_code}
==>  {test_status}
'''

# query status
status_code = r.status_code

# display the results
if status_code == 400:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
    
print(output.format(status_code=status_code, test_status=test_status))
# printing in a file
if print_log == 1:
    with open('../logs/api_test.log', 'a') as file:
        file.write(output.format(status_code=status_code, test_status=test_status))



"==============================="
# resquest
r = requests.get(
    url='http://{address}:{port}/airport_latency_info?airport_code={airport_code}&start_date={start_date}&end_date={end_date}'.format(address=api_address, port=api_port,airport_code=airport_code,start_date=start_date,end_date=end_date),
    params= {
       "airport_code": '',
       "start_date": '2022-11-25',
       "end_date": '2022-12-01',
    }
    
)
output = '''
============================
    Get all flights and delayed flights between 2 dates
============================
request done at "/airport_latency_info"
airport_code ='',
start_date ='2022-11-25',
end_date'= '2022-12-01',
expected result = 400
actual restult = {status_code}
==>  {test_status}
'''

# query status
status_code = r.status_code

# display the results
if status_code == 400:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
    
print(output.format(status_code=status_code, test_status=test_status))
# printing in a file
if print_log == 1:
    with open('../logs/api_test.log', 'a') as file:
        file.write(output.format(status_code=status_code, test_status=test_status))



"==============================="
# resquest
r = requests.get(
    url='http://{address}:{port}/airport_latency_info?airport_code={airport_code}&start_date={start_date}&end_date={end_date}'.format(address=api_address, port=api_port,airport_code=airport_code,start_date=start_date,end_date=end_date),
    params= {
       "airport_code": 'weared airport name',
       "start_date": '',
       "end_date": '',
    }
    
)
output = '''
============================
    Get all flights and delayed flights between 2 dates
============================
request done at "/airport_latency_info"
airport_code ='weared airport name',
start_date ='',
end_date'= '',
expected result = 200
actual restult = {status_code}
==>  {test_status}
'''

# query status
status_code = r.status_code

# display the results
if status_code == 200:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
    
print(output.format(status_code=status_code, test_status=test_status))
# printing in a file
if print_log == 1:
    with open('../logs/api_test.log', 'a') as file:
        file.write(output.format(status_code=status_code, test_status=test_status))




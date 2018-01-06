import json
import time
import os
import shutil
import sys
from os import listdir
from os.path import isfile, join
import requests
import traceback
import atexit


def exit_handler():
    try:
        os.rmdir("lock")
    except Exception as e:
        print("error")

def check_status_code(response,success_function):
    logging(" call  url {0} - {1} ".format(response.url, response.request.method))
    if response.status_code == 400:
        print("error {0} - bad request", response.status_code)
        print("\n\n {0} \n\n".format(response.text))
        logging("error {0} - bad request \n {1}".format(response.status_code,response.text))
        return False
    elif response.status_code == 404:
        print("error {0} - Not found", response.status_code)
        logging("error {0} - Not found".format(response.status_code))
        return False
    elif response.status_code == 401:
        print("error {0} - Unauthorized", response.status_code)
        logging("error {0} - Unauthorized".format(response.status_code))
        return False
    elif response.status_code == 408:
        print("error {0} - Request timeout", response.status_code)
        logging("error {0} - Request Timeout".format(response.status_code))
        return False
    elif response.status_code == 405:
        print("error {0} - Method not allowed", response.status_code)
        logging("error {0} - Method not allowed: url called with method {1}".format(response.status_code, response.method))
        return False
    elif response.status_code == 412:
        print("error {0} - Precondition Failed", response.status_code)
        logging("error {0} - Precondition Failed".format(response.status_code))
        return False
    elif response.status_code == 429:
        print("error {0} - Too Many requests", response.status_code)
        logging("error {0} - Too Many requests".format(response.status_code))
        return False
    elif response.status_code == 500:
        print("500 server error")
        logging("error {0} - Server error".format(response.status_code))
        return False
    else:
        if success_function is None:
            try:
                return response.json()
            except Exception as e:
                print("error occurred in response: {0} \n code: {1} ".format(response.text,response.status_code))
                print("error: ", e)
                exit(1)
        else:
           return success_function(response)

def write_json_to_file(filename,data):
    try:
        with open(filename, 'w') as file:
            file.write(json.dumps(data, default=lambda o: o.__dict__,
                                  sort_keys=False, indent=4))
            file.close()
    except:
        print("some error occurred while writing on file")
        print(data)



def write_to_file(filename,data,mod = "w"):
    try:
        with open(filename, mod) as file:
            file.write(data)
            file.close()
    except:
        print("some error occurred while writing on file")
        print(data)
        print(traceback.print_exc())
        exit(1)




def logging(data):
    logpath = "log/{0}.txt".format(time.strftime('%Y-%m-%d'))
    try:
        with open(logpath, "a") as file:
            file.write("{0} : {1} \n".format(time.strftime("%a, %d %b %Y %H:%M:%S"), data))
            file.close()
    except Exception as e:
        print("some error occurred while writing on log file\n {0}".format(logpath))
        print(e)
        exit(1)

def setup_folder(file_paths=[]):
    for path in file_paths:
        try:
            os.mkdir(path)
            print(" folder {} Created".format(path))
        except Exception as e:
            pass
            #print(" folder {} already exist".format(path))

def archive_old_file(file_paths=[]):
    path_to_copy = 'old/{}'.format(time.strftime('%Y-%m-%d %H:%M'))
    try:
        os.mkdir(path_to_copy)
    except Exception as e:
        print(e)

    for path in file_paths:
        try:
            shutil.copytree(path,os.path.join(path_to_copy, path))
            files = [f for f in listdir(path) if isfile(join(path, f))]
            for file in files:
                try:
                    os.remove(os.path.join(path, file))
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

def gmaps_geolocate(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}'.format(address)
    ret = requests.get(url)
    gmaps_return = check_status_code(ret,None)
    try:
        if gmaps_return:
            results = gmaps_return['results'][0]
            geometry = results['geometry']
            location = geometry['location']
            return [location['lat'], location['lng']]
        else:
            return None
    except Exception as e:
        return None


def make_dist_matrix( n, default, ijd_tuples ):
    """Utility function to make triangular distance matrices"""
    dist = [[default for j in xrange(i)]
             for i in xrange(n)]
    for i,j,d in ijd_tuples:
        if i<j :
            i,j = j,i
        dist[i][j] = d
    return dist

import subprocess
import json
import logging
import sys
import os
import time
import requests
import signal

logging.basicConfig(filename='./logs/automate.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


def get_properties(filename="./commands.json"):
    try:
        return json.loads(open(filename).read())
    except Exception as e:
        logging.exception(e)
        print("Error in reading json file")
        return 0


def install_cds(command):
    try:
        proc = subprocess.Popen(command.split(), shell=True)
        logging.info("Installing CDS: " + str(proc.pid))
        proc.wait()
        logging.info(proc.stdout)
        logging.error(proc.stderr)
        logging.info("process returned: " + str(proc.returncode))
        return proc.returncode
    except Exception as e:
        logging.exception(e)
        print("Failed to install cds")
        return -1


def create_project(command):
    try:
        proc = subprocess.Popen(command.split(), shell=True)
        logging.info("Process started for creating project: " + str(proc.pid))
        proc.wait()
        logging.info(proc.stdout)
        logging.error(proc.stderr)
        logging.info("process returned: " + str(proc.returncode))
        return proc.returncode
    except Exception as e:
        logging.exception(e)
        print("Failed to create project")
        return -1


def install_package(command):
    try:
        proc = subprocess.Popen(command.split(), shell=True)
        logging.info("Process started for installing packages: " + str(proc.pid))
        proc.wait()
        logging.info(proc.stdout)
        logging.error(proc.stderr)
        logging.info("process returned: " + str(proc.returncode))
        return proc.returncode
    except Exception as e:
        logging.exception(e)
        print("Failed to install package")
        return -1


def cds_run(**kwargs):
    try:
        keys = kwargs.keys()
        duration = kwargs['duration']
        book_url = kwargs['book_url']
        author_url = kwargs['author_url']
        command = kwargs['command']
        if 'query_url' in keys:
            proc = subprocess.Popen(command.split(), shell=True)
            logging.info("Process started for cds run, Process Id: " + str(proc.pid))
            time.sleep(duration)
            query_url = kwargs['query_url']
            logging.info("Getting Query Data")
            queryref = requests.get(query_url)
            if queryref.status_code == 200:
                logging.info(str(queryref.json()))
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(proc.pid)])
            # proc.send_signal(signal.CTRL_C_EVENT)
            # proc.send_signal(signal.CTRL_C_EVENT)
            return 0
        else:
            proc = subprocess.Popen(command.split(), shell=True)
            logging.info("Process started for cds run, Process Id: " + str(proc.pid))
            time.sleep(duration)
            logging.info("Getting Book Data")
            bookref = requests.get(book_url)
            if bookref.status_code == 200:
                logging.info(str(bookref.json()))

            logging.info("Getting Authors Data")
            authorref = requests.get(author_url)
            if authorref.status_code == 200:
                logging.info(str(authorref.json()))
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(proc.pid)])
            # proc.send_signal(signal.CTRL_C_EVENT)
            # proc.send_signal(signal.CTRL_C_EVENT)
            time.sleep(5)

            return 0
    except Exception as e:
        logging.exception(e)
        return -1


def create_cat_service_cds(path):
    try:
        command = "copy " + path + " my-bookshop\\srv\\cat-service.cds"
        status = subprocess.call(command, shell=True)
        logging.info("Creating cat-service cds file: " + str(status))
        return status
    except Exception as e:
        logging.exception(e)
        print("Failed to create file")
        return -1


def create_cat_service_js(path):
    try:
        command = "copy " + path + " my-bookshop\\srv\\cat-service.js"
        status = subprocess.call(command, shell=True)
        logging.info("Creating cat-service js file: " + str(status))
        return status
    except Exception as e:
        logging.exception(e)
        print("Failed to create file")
        return -1


def create_data_model(path):
    try:
        command = "copy " + path + " my-bookshop\\db\\data-model.cds"
        status = subprocess.call(command, shell=True)
        logging.info("Creating data-model.cds file: " + str(status))
        return status
    except Exception as e:
        logging.exception(e)
        print("Failed to create file")
        return -1


def overwrite_cat_service(path):
    try:
        command = "copy " + path + " my-bookshop\\srv\\cat-service.cds /y"
        status = subprocess.call(command, shell=True)
        logging.info("Overwriting cat-service.cds file: " + str(status))
        return status
    except Exception as e:
        logging.exception(e)
        print("Failed to overwrite file")
        return -1


def add_csv_data(path_book, path_author):
    try:
        os.mkdir("./my-bookshop/db/csv")
        command_book = "copy " + path_book + " my-bookshop\\db\\csv\\my.bookshop-Books.csv /y"
        command_author = "copy " + path_author + " my-bookshop\\db\\csv\\my.bookshop-Authors.csv /y"
        status_book = subprocess.call(command_book, shell=True)
        status_author = subprocess.call(command_author, shell=True)
        logging.info("Adding csv data: " + str(status_book) + str(status_author))
        return status_book, status_author
    except Exception as e:
        logging.exception(e)
        print("Failed to add data files")
        return -1


def add_persistent_db(command):
    try:
        proc = subprocess.Popen(command.split(), shell=True)
        logging.info("Process started for adding persistent database: " + str(proc.pid))
        proc.wait()
        logging.info(proc.stdout)
        logging.error(proc.stderr)
        logging.info("process returned: " + str(proc.returncode))
        return proc.returncode
    except Exception as e:
        logging.exception(e)
        print("Failed to add persistent database")
        return -1


def deploy_dataModel(command):
    try:
        proc = subprocess.Popen(command.split(), shell=True)
        logging.info("Process started for deploying to db: " + str(proc.pid))
        proc.wait()
        logging.info(proc.stdout)
        logging.error(proc.stderr)
        logging.info("process returned: " + str(proc.returncode))
        return proc.returncode
    except Exception as e:
        logging.exception(e)
        print("Failed to deploy to database")
        return -1


def open_sqlite(command):
    try:
        proc = subprocess.Popen(command.split(), shell=True)
        logging.info("Open sqlite to view database: " + str(proc.pid))
        time.sleep(5)
        logging.info(proc.stdout)
        logging.error(proc.stderr)
        logging.info("process returned: " + str(proc.returncode))
        subprocess.call(['taskkill', '/F', '/T', '/PID', str(proc.pid)])
        #proc.send_signal(signal.CTRL_BREAK_EVENT)
        return 0
    except Exception as e:
        logging.exception(e)
        print("Failed to open sqlite")
        return -1


def get_book(url):
    try:
        return requests.get(url)
    except Exception as e:
        logging.exception(e)
        return -1


def order_book(url, payload, header):
    try:
        return requests.post(url, data=payload, headers=header)
    except Exception as e:
        logging.exception(e)
        return -1


def final_cds_run(command):
    url = "http://localhost:4004/catalog/Orders"

    payload = "{\n  \"book_ID\": 201,\n  \"amount\": 1\n}"
    headers = {
        'Content-Type': 'text/plain'
    }
    try:
        proc = subprocess.Popen(command.split(), shell=True)
        time.sleep(10)
        get_book_res = get_book("http://localhost:4004/catalog/Books")
        if get_book_res.status_code == 200:
            logging.info("Getting book data")
            logging.info(str(get_book_res.json()))
        order_book_res = order_book(url, payload, headers)
        if order_book_res.status_code == 200:
            logging.info("Ordering book")
            logging.info(str(order_book_res.json()))
        get_book_res = get_book("http://localhost:4004/catalog/Books")
        if get_book_res.status_code == 200:
            logging.info("Getting book data again")
            logging.info(str(get_book_res.json()))
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(proc.pid)])
        return 0
    except Exception as e:
        logging.exception(e)
        return -1


def overwrite_cat_servicejs(path):
    try:
        command = "copy " + path + " my-bookshop\\srv\\cat-service.js /y"
        status = subprocess.call(command, shell=True)
        logging.info("Overwriting cat-service.js file: " + str(status))
        return status
    except Exception as e:
        logging.exception(e)
        print("Failed to overwrite file")
        return -1


if __name__ == "__main__":
    props = get_properties()
    #install_status = install_cds(props["install_cds"])
    project_status = create_project(props["create_project"])
    package_status = install_package(props["install_package"])
    file_catcds_status = create_cat_service_cds(props["cat_service_path"])
    cds_status = cds_run(command=props["cds_run"], book_url=props["book_url"], author_url=props["author_url"], duration=10)
    file_catjs_status = create_cat_service_js(props["cat_servicejs_path"])
    cds_status = cds_run(command=props["cds_run"], book_url=props["book_url"], author_url=props["author_url"], duration=10)
    file_data_model = create_data_model(props["data_model_path"])
    file_catcds_overwrite_status = overwrite_cat_service(props["new_cat_servicecds_path"])
    data_status = add_csv_data(props["my_bookshop_Books_csv_path"], props["my_bookshop_Authors_csv_path"])
    cds_status = cds_run(command=props["cds_run"], book_url=props["book_url"], author_url=props["author_url"], duration=10, query_url=props["query_url"])
    sqlitedb_status = add_persistent_db(props["install_sqlite"])
    deploy_status = deploy_dataModel(props["deploy_datamodel"])
    open_sqlite_status = open_sqlite(props["open_sqlite"])
    file_catjs_overwrite_status = overwrite_cat_servicejs(props["new_cat_servicejs_path"])
    final_status = final_cds_run(props["cds_run"])

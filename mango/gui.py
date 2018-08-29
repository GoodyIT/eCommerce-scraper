#!/usr/bin/python
try:
    from Tkinter  import * 
except:
    from tkinter import *

try:
    from tkFileDialog import *
except:
    from tkinter import filedialog

try:
    from tkMessageBox import *
except:
    from tkinter import messagebox

from os import path
from subprocess import check_output
from multiprocessing import Process
from threading import Thread
from time import sleep

import json

import csv

import os
import subprocess
import signal

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup as BSoup

import random
import redis

from lxml import etree

import requests
from bs4 import BeautifulSoup

import time
import sys

import pdb

root = Tk()

class Application(Frame):
    proxy_list_path = code_list_path = ''
    valid_code_cnt = expired_code_cnt = 0
        
    def createWidgets(self):
        self.frame=Frame(self, pady=3)
        self.frame.pack()
        self.frametwo=Frame(self, pady=3)
        self.frametwo.pack(side=BOTTOM)
        self.frameThree = Frame(self, pady=3)
        self.frameThree.pack(side=BOTTOM)
        self.frameFour = Frame(self, pady=3)
        self.frameFour.pack(side=BOTTOM)
       
        self.code_file=Button(self.frame,text="Load Code List",fg="black", command=self.openCodeList)
        self.code_file.pack(side=LEFT)
        self.proxy_file=Button(self.frame,text="Load Proxy List", fg="black", command=self.openProxyFileList)
        self.proxy_file.pack(side=LEFT)

        self.scan_btn = Button(self.frameFour, text="Scan code", fg="black", command=self.scanCode)
        self.scan_btn.pack(side=LEFT)
        self.stop_btn = Button(self.frameFour, text="Stop", fg="red", state=DISABLED,  command=self.stop_scraper)
        self.stop_btn.pack(side=LEFT)
        self.exit_btn = Button(self.frameFour, text="Exit", fg="red", command=self.close_window)
        self.exit_btn.pack(side=LEFT)
        
        self.concurrent=Label(self.frameThree,text="Concurrent Threads")
        self.concurrent.pack(side=LEFT)
        self.concurrent_thread = Spinbox(self.frameThree, from_=16, to=100, width=5, justify=RIGHT)
        self.concurrent_thread.pack(side=BOTTOM)
        var = StringVar(self.frameThree)
        var.set("50")
        self.concurrent_thread.config(textvariable=var)

        self.L1=Label(self.frametwo,text="# of valid code", fg="green")
        self.L1.pack(side=LEFT)
        self.valid_code=Label(self.frametwo,text="0")
        self.valid_code.pack(side=LEFT)
        
        self.L2=Label(self.frametwo,text="# of expired code", fg="green")
        self.L2.pack(side=LEFT)
        self.expired_code=Label(self.frametwo,text="0")
        self.expired_code.pack(side=LEFT)

        self.L3=Label(self.frametwo,text="Total scanned code", fg="red")
        self.L3.pack(side=LEFT)
        self.total_code=Label(self.frametwo,text="0")
        self.total_code.pack(side=LEFT)
        
    def openProxyFileList(self):
        try:
            file = askopenfilename(initialdir= path.dirname(__file__), filetypes = (("Text files","*.txt"),("all files","*.*")))
        except:
            file = filedialog.askopenfilename(initialdir= path.dirname(__file__), filetypes = (("Text files","*.txt"),("all files","*.*")))
   
        self.proxy_list_path = file

    def openCodeList(self):
        try:
            file = askopenfilename(initialdir= path.dirname(__file__), filetypes = (("Text files","*.txt"),("all files","*.*")))
        except:
            file = filedialog.askopenfilename(initialdir= path.dirname(__file__), filetypes = (("Text files","*.txt"),("all files","*.*")))
        
        self.code_list_path = file

    def scanCode(self):
        if self.code_list_path == '':
            showinfo("Warning", "Please select the file containing code list")
            return
        
        if self.proxy_list_path == '':
            showinfo("Warning", "Please select the file containing proxy list")
            return
        
        if  self.last_index != '':
            if not askyesno("Warning", "Are you going to resume the scraper"):
                open("data/pipeline.dat","w").close()

        self.thread_scan()
    
    def thread_scan(self):
        path =  "scrapy crawl mango -a _code_list_path=" + self.code_list_path + " -a _proxy_list_path=" + self.proxy_list_path + " -a _concurrent_requests=" + self.concurrent_thread.get() 
        # path += " -s JOBDIR=data/mango_1"
        print(path)
        subprocess.Popen(path)

    def initRedis(self):
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
        p = self.r.pubsub()
        p.subscribe(**{'scrapy-channel': self.my_handler})
        p.run_in_thread(sleep_time=0.001)

    def create_pipeline_for_resume(self):
        try:
            f = open("data/pipeline.dat", "r")
        except:
            f = open("data/pipeline.dat", "w+")
        self.last_index = f.read()
        f.close()

    def stop_scraper(self):
        # try: self.pro
        # except:
        #     return
        if not askyesno("Warning", "Are you going to stop scraper"):
            return
        # self.r.publish('scrapy-channel', json.dumps({'stop': '1'}))

        # put index to resume the spider
        f = open("data/pipeline.dat","w")
        f.write(str(self.valid_code_cnt)  + "," + str(self.expired_code_cnt)+ "," + str(self.last_index))
        f.close()

        self._stop()

    def _stop(self):
        self.r.publish('scrapy-channel', json.dumps({'stop': '1'}))
        # self.pro.send_signal(signal.CTRL_C_EVENT)

    def close_window(self):
        self.stop_scraper()

        os.kill(os.getpid(), 9)

        # root.destroy()

    def my_handler(self, message):
        try:
            self.valid_code_cnt = json.loads(message['data'])['valid_cnt']
            self.valid_code.config(text=(self.valid_code_cnt))
            self.expired_code_cnt = json.loads(message['data'])['expired_cnt']
            self.expired_code.config(text=(self.expired_code_cnt))
            self.total_code.config(text=(json.loads(message['data'])['total_cnt']))
            self.last_index = json.loads(message['data'])['index']
            print('-------- message from redis ----------', message['data'])
            
            if 'timestamp' in json.loads(message['data']):
                print('--&&&&&&&&&&&&&&&&& timestamp expired &&&&&&&&&&&&&')
                self.thread_scan()
        except:
            print('-------------- error in my_handler in gui --------------')

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.initRedis()
        self.create_pipeline_for_resume()

def disable_event():
    pass

class Worker(Thread):
    def __init__(self, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)
    def run(self):
        super(Worker, self).run()
        return

app = Application(master=root)
app.master.title("Mango Scrapy App")
app.master.minsize(600, 200)
root.protocol("WM_DELETE_WINDOW", disable_event)
app.mainloop()
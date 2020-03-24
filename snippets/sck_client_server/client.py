# Echo client program
import sys
from datetime import datetime, date 
import time

import select
import socket

# ----------------------------------------------------------------
def log_message(flog, msg):
    logmsg = str(datetime.now()) + ' - ' + msg + '\n'
    f.write(logmsg)
    f.flush()
    #prints also on stdout
    sys.stdout.write(logmsg)
    
# ----------------------------------------------------------------
def sck_connect(s,h,p,flog):
    connected = False
    while connected == False:
        try:
            s.connect((HOST, PORT))
            connected = True
            break
        except socket.error:
            if sys.exc_info()[1][0] == 10061:
                log_message(flog, 'Server not responding...')
            else:
                log_message(flog, 'unexpected socket error: ' + str(sys.exc_info()[1]) + '...')
        except:
            log_message(flog, 'unexpected exception...')

        log_message(flog, '... try again in ' + str(TIMEOUT) + ' seconds')
        time.sleep(TIMEOUT)


# ----------------------------------------------------------------
# MAIN -----------------------------------------------------------
###HOST = '127.0.0.1'    # The remote host
HOST = '10.107.124.34'    # The remote host
###HOST = 'fipc1278'    # The remote host
PORT = 50007          # The same port as used by the server

TIMEOUT=60

# open log file
f = open('sck_client'+str(date.today())+'_'+str(time.time())+'.log', 'w')
log_message(f, 'Client socket v. 1.0 - By F. Piantini 24/4/2008 - Selex Communications')

while True:

    # instantiate socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # try to connect to server
    sck_connect(s, HOST, PORT, f)
    log_message(f, 'Connected')

    cont=0
    conn_ok = True
    # sends hello string every TIMEOUT seconds
    while conn_ok:

        # --------------------- sends message to server ----------------------------
        rtread, rtwrite, inerror = select.select((), (s,), (s,), 4*TIMEOUT)
        if ((len(rtwrite) == 0) and (len(inerror) == 0)):
            # timeout
            log_message(f, 'select timeout trying to send data, closing connection with client')
            s.close()
            conn_ok = False
        for des in rtwrite:
            if des == s:
                log_message(f, 'sending hello message to server')
                s.send('Hello, world! (#' + str(cont) + ')\n')
                cont=cont+1
        if (len(inerror) > 0):
            log_message(f, 'select returns error, closing connection with client')
            s.close()
            conn_ok = False

        # -------------------- receives reply from server --------------------------
        rtread, rtwrite, inerror = select.select((s,), (), (s,), 4*TIMEOUT)
        if ((len(rtread) == 0) and (len(inerror) == 0)):
            # timeout
            log_message(f, 'select timeout trying to receive data, closing connection with client')
            s.close()
            conn_ok = False
        for des in rtread:
            if des == s:
                log_message(f, 'receiving answer from server')
                data = s.recv(1024)
                if data:
                    log_message(f, 'received: ' + str(repr(data)))
                elif data == '':
                    log_message(f, 'empty string received, closing connection with server')
                    s.close()
                    conn_ok = False
        for des in inerror:
            if des == s:
                log_message(f, 'select returns error, closing connection with server')
                s.close()
                conn_ok = False
                    



#        try:
#            s.send('Hello, world! (#' + str(cont) + ')\n')
#            log_message(f,'sent hello message')
#            cont=cont+1
#        except:
#            log_message(f,'exception sending hello message, close connection and retry')
#            s.close()
#            break

        # ----------------- sleeps some time -------------------------
        time.sleep(TIMEOUT)

# -------------------------------------------------------------
log_message(f, 'Connection closed, exiting')
f.close()
s.close()


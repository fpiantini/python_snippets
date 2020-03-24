#
# Echo server program
import sys
from datetime import datetime, date 
import time

import socket
import select

# ----------------------------------------------------------------
def log_message(flog, msg):
    logmsg = str(datetime.now()) + ' - ' + msg + '\n'
    f.write(logmsg)
    f.flush()
    #prints also on stdout
    sys.stdout.write(logmsg)


# ----------------------------------------------------------------
# MAIN -----------------------------------------------------------
# Per motivi al momento ignoti il codice qua sotto, seppur corretto, non funziona
# (i client non riescono a connettersi)
#####srv_host=socket.gethostname()
srv_host=''

PORT = 50007              # Arbitrary non-privileged port
TIMEOUT=60

f = open('sck_server'+str(date.today())+'_'+str(time.time())+'.log', 'w')
log_message(f, 'Server socket v. 1.0 - By F. Piantini 24/4/2008 - Selex Communications')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
log_message(f, 'socket created: ' + str(s))

s.bind((srv_host, PORT))
log_message(f, 'bind of socket on host \'' + str(srv_host) + '\' port ' + str(PORT) + ' successfull')

s.listen(1)
log_message(f, 'listening on host \'' + str(srv_host) + '\' port ' + str(PORT))

while 1:
    # accept a new connection
    log_message(f, 'waiting for client connection...')
    conn, addr = s.accept()
    log_message(f, 'Connected by ' + str(addr))
    conn_ok = True

    while conn_ok:

        # performs select
        ready_to_read, ready_to_write, in_error = select.select((conn,), (), (conn,), 6*TIMEOUT)

        # if everything is empty we are in timeout
        if (len(ready_to_read) == 0) and (len(in_error) == 0):
            # timeout
            log_message(f, 'client communication timeout, closing connection')
            conn.close()
            conn_ok = False

        for des in ready_to_read:
            if des == conn:
                log_message(f, 'Receiving from client...')
                data = conn.recv(1024)
                if data:
                    log_message(f, 'Received: ' + str(repr(data)))
		    # sends back data
		    conn.send(data)
                elif data == '':
                    log_message(f, 'connection with client lost')
                    conn.close()
                    conn_ok = False

        for des in in_error:
            if des == conn:
                log_message(f, 'exception, closing connection with client!')
                conn.close()
                conn_ok = False





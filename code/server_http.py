# ------------------------------
# This file is part of the BB-8 robot project.
# Created By : Killian Guillemot
# Created At : 2020-05-01
# Version : 1.0 
# ------------------------------
try:
    import usocket as socket
except:
    import socket

import esp
import network

from code.MoteurDC import MoteurDC

esp.osdebug(None)

import gc

gc.collect()

station = network.WLAN(network.AP_IF)
if station.active():
    station.active(False)

station.active(True)
station.config(essid='ynov', password='ynov')

while not station.isconnected():
    pass

print('Connection successful')
print(station.ifconfig())

moteur_droite = MoteurDC(12, 13)
moteur_gauche = MoteurDC(14, 27)


def web_page():
    html = """
    <html>
        <head> 
            <title>ESP Web Server</title> 
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="icon" href="data:,"> 
            <style>
            html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
            h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}
            .button{display: inline-block; background-color: #e7bd3b; border: none; border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
            .button2{background-color: #4286f4;}
            </style>
        </head>
        <body> 
            <h1>ESP Web Server</h1> 
            <p>Right Motor state: <strong>""" + moteur_droite.status + """</strong></p>
            <p>Left Motor state: <strong>""" + moteur_gauche.status + """</strong></p>
            <form action="" method="get">
                <input type="submit" name="button" value="fw" class="button">
                <input type="submit" name="button" value="rg" class="button">
                <input type="submit" name="button" value="lf" class="button">
                <input type="submit" name="button" value="bk" class="button">
                <input type="submit" name="button" value="st" class="button button2">
            </form>
        </body>
    </html>
    """
    return html


# import server_http as ht

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(2048)
        request = str(request)
        print('Content = %s' % request)
        button_fw = request.find('/?button=fw')
        button_rg = request.find('/?button=rg')
        button_lf = request.find('/?button=lf')
        button_bk = request.find('/?button=bk')
        button_st = request.find('/?button=st')
        if button_fw == 6:
            print('Moteur Avant')
            moteur_droite.avancer()
            moteur_gauche.avancer()
        elif button_lf == 6:
            print('Moteur Gauche')
            moteur_droite.avancer()
            moteur_gauche.reculer()
        elif button_rg == 6:
            print('Moteur Droite')
            moteur_droite.reculer()
            moteur_gauche.avancer()
        elif button_bk == 6:
            print('Moteur Arrière')
            moteur_droite.reculer()
            moteur_gauche.reculer()
        elif button_st == 6:
            print('Moteur Stop')
            moteur_droite.arreter()
            moteur_gauche.arreter()
        else:
            print('No action')
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
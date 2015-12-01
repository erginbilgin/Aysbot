#!/usr/bin/env python3

import re
import socket
import threading

# --------------------------------------------- Start Settings -----------------------------------------------------
HOST = "irc.twitch.tv"                          # Hostname of the IRC-Server in this case twitch's
PORT = 6667                                     # Default IRC-Port
CHAN = "#icepath1"                              # Channelname = #{Nickname}
NICK = "Aysbot"                                 # Nickname = Twitch username
PASS = "oauth:##############################"   # www.twitchapps.com/tmi/ will help to retrieve the required authkey
# --------------------------------------------- End Settings -------------------------------------------------------


# --------------------------------------------- Start Functions ----------------------------------------------------
def send_pong(msg):
    con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))


def send_message(chan, msg):
    con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))


def send_nick(nick):
    con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))


def send_pass(password):
    con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))


def join_channel(chan):
    con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))


def part_channel(chan):
    con.send(bytes('PART %s\r\n' % chan, 'UTF-8'))

# --------------------------------------------- End Functions ------------------------------------------------------


# --------------------------------------------- Start Helper Functions ---------------------------------------------
def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result


def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result


def parse_message(msg):
    if len(msg) >= 1:
        msg = msg.split(' ')
        options = {'!test': command_test,
                   '!asdf': command_asdf,
                   '!cool': command_cool,
                   '!troll': command_troll,
                   '!nays': command_nays,
                   '!youtube': command_youtube,
                   '!DogeCoine': command_doge,
                   '!yımırta': command_yumurta}
        if msg[0] in options:
            options[msg[0]]()
# --------------------------------------------- End Helper Functions -----------------------------------------------


# --------------------------------------------- Start Command Functions --------------------------------------------
def command_test():
    send_message(CHAN, 'testing some stuff')


def command_asdf():
    send_message(CHAN, 'asdfster')

def command_cool():
    send_message(CHAN, 'KappaPride')

def command_troll():
    send_message(CHAN, 'abi modluk verir misin?')

def command_nays():
    send_message(CHAN, 'nays botmuş hocam')

def command_youtube():
    send_message(CHAN, 'Dota rehberleri ve oyun incelemeleri için kanalımı ziyaret etmeyi unutmayın! http://tinyurl.com/hrkqdf3')

def comm_youtube():
    threading.Timer(600.0, comm_youtube).start()
    command_youtube()

def command_doge():
    send_message(CHAN, 'ShibeZ')

def command_yumurta():
    send_message(CHAN, 'CİZIS KIRAYST')

# --------------------------------------------- End Command Functions ----------------------------------------------

con = socket.socket()
con.connect((HOST, PORT))

send_pass(PASS)
send_nick(NICK)
join_channel(CHAN)

data = ""

comm_youtube()

while True:
    try:
        data = data+con.recv(1024).decode('UTF-8')
        data_split = re.split(r"[~\r\n]+", data)
        data = data_split.pop()

        for line in data_split:
            line = str.rstrip(line)
            line = str.split(line)

            if len(line) >= 1:
                if line[0] == 'PING':
                    send_pong(line[1])

                if line[1] == 'PRIVMSG':
                    sender = get_sender(line[0])
                    message = get_message(line)
                    parse_message(message)

                    print(sender + ": " + message)
                    if message[0:8] == '!intihar':
                        send_message(CHAN, '/timeout ' + sender + ' 30')
                        send_message(CHAN, sender + ' intihar etti.')

    except socket.error:
        print("Socket died")

    except socket.timeout:
        print("Socket timeout")
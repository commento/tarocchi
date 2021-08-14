#!/usr/bin/python3

import PySimpleGUI as sg
import datetime
import time

def time_as_int():
    return int(round(time.time() * 100))

layout = [[sg.Text("Tarocchi", font=("Helvetica", 55))], 
          [sg.Button("START", font=("Helvetica", 25)),
           sg.Text('', size=(8, 1), font=('Helvetica', 25),
                justification='center', key='text')],
          [sg.Text(size=(70,1), key='-start-', font=("Helvetica", 25))], 
          [sg.Button("STOP", font=("Helvetica", 25), disabled=True)], 
          [sg.Text(size=(70,1), key='-stop-', font=("Helvetica", 25))],
          [sg.Button("PRINT", font=("Helvetica", 25), disabled=True)], 
          [sg.Text(size=(70,10), key='-OUTPUT-', font=("Helvetica", 25))]]

# Create the window
sg.theme('DarkPurple')
window = sg.Window("tarocchi", layout)

l = []
start = None
start_program = datetime.datetime.today()

current_time, paused_time, paused = 0, 0, True
start_time = time_as_int()
# Create an event loop
while True:
    if not paused:
        event, values = window.read(timeout=10)
        current_time = time_as_int() - start_time
    else:
        event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED:
        break
    if event == "PRINT":
        stop_program = datetime.datetime.today()
        s = sum(l)
        s = (s % 3600) // 60
        window['-OUTPUT-'].update(f"hai fatto {s} minuti di chiamata con {len(l)} chiamate: \
                                    \
                                    \
                                  dalla data {start_program.isoformat()[:19]} \
                                    \
                                    \
                                  alla data {stop_program.isoformat()[:19]}")
        print(f"hai fatto {s} minuti di chiamata con {len(l)} chiamate: ")
        print(f"dalla data {start_program}")
        print(f"alla data {stop_program}")
    if event == "START":
        start = datetime.datetime.today()
        print(f'Inizio della telefonata: {start}')
        window['-start-'].update(f'Inizio della telefonata: {start.isoformat()[:19]}')
        window['START'].update(disabled=True)
        window['STOP'].update(disabled=False)
        window['PRINT'].update(disabled=True)
        paused_time = start_time = time_as_int()
        current_time = 0
        paused = not paused
    if event == "STOP":
        stop = datetime.datetime.today()
        print(f'Fine della telefonata: {stop}')
        window['-stop-'].update(f'Fine della telefonata: {stop.isoformat()[:19]}')
        seconds = (stop-start).seconds
        print(seconds)
        l.append(seconds)
        window['START'].update(disabled=False)
        window['STOP'].update(disabled=True)
        window['PRINT'].update(disabled=False)
        paused = not paused
    # --------- Display timer in window --------
    window['text'].update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
                                                        (current_time // 100) % 60,
                                                        current_time % 100))
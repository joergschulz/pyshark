#!/usr/bin/env python

import asyncio
import signal

import threading
import tkinter
import tkinter.ttk

import pyshark
from pyshark.capture.capture import Capture, StopCapture


#c = pyshark.LiveCapture(interface='bresp42', bpf_filter='icmp', debug=True)
c = Capture(interface='bresp42', capture_filter='icmp', debug=True)

def win_quit(root):
    def cmd():
        root.destroy()
        #signal.raise_signal( signal.SIGINT )
        #signal.pthread_kill( threading.main_thread().ident, signal.SIGINT )
        asyncio.run_coroutine_threadsafe(c.close_async(), c.eventloop)
    return cmd

def win():
    root = tkinter.Tk()
    frm = tkinter.ttk.Frame(root, padding=10)
    frm.grid()
    tkinter.ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    tkinter.ttk.Button(frm, text="Quit", command=win_quit(root)).grid(column=1, row=0)
    root.mainloop()

async def mystop(task):
    await asyncio.sleep(4)
    print('done sleep')
    #if task:
    #    task.cancel()
    #raise StopCapture()
    #raise KeyboardInterrupt()
    #signal.raise_signal( signal.SIGINT )
    #c.eventloop.stop()
    #c.eventloop.close()
    #c.close()
    # DAS GEHT !!!
    # await c.close_async()

i=0
async def packet_print(p):
    global i
    i=i+1
    print(f'packet {i}')
    #if i==2:
    #    raise StopCapture()


thread_gui = threading.Thread( target=win )
thread_gui.start()

#for i in c.sniff_continuously(2):
#    print(i)

c.apply_on_packets( packet_print )

# wie in apply_on_packets
#coro = c.packets_from_tshark( packet_print )
#async def foo():
#    await asyncio.gather( coro, mystop(None) )
#c.eventloop.run_until_complete( foo() )

thread_gui.join()

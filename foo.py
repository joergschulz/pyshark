#!/usr/bin/env python

import asyncio
import logging
import signal

import threading
import tkinter
import tkinter.ttk

import pyshark
from pyshark.capture.capture import Capture, StopCapture

#logging.basicConfig(level=logging.DEBUG)

#c = pyshark.LiveCapture(interface='bresp42', bpf_filter='icmp', debug=True)
c = Capture(interface='bresp42', capture_filter='icmp', debug=True)

#for i in c.sniff_continuously(2):
#    print(i)

#c.load_packets( packet_count=2 )
#for i in c:
#    print(i)

def win_quit(root):
    def cmd():
        root.destroy()
        #signal.raise_signal( signal.SIGINT )
        signal.pthread_kill( threading.main_thread().ident, signal.SIGINT )
    return cmd

def win():
    root = tkinter.Tk()
    frm = tkinter.ttk.Frame(root, padding=10)
    frm.grid()
    tkinter.ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    tkinter.ttk.Button(frm, text="Quit", command=win_quit(root)).grid(column=1, row=0)
    #print(root.mainloop)
    root.mainloop()
    #return root

async def mystop(t):
    await asyncio.sleep(3)
    print('done sleep')
    #print('close')
    #c.close()
    #await c.close_async()
    #print('fertig1')
    #c.eventloop.stop()
    #c.eventloop.close()
    #t.cancel()
    #print('fertig2')
    #raise StopCapture()
    #raise KeyboardInterrupt()
    #signal.raise_signal( signal.SIGINT )

i=0
async def packet_print(p):
    global i
    i=i+1
    print(f'packet {i}')
    #if i==2:
    #    raise StopCapture()


async def foo():
    t1 = asyncio.create_task( c.packets_from_tshark( packet_callback=packet_print, close_tshark=False ) )
    t2 = asyncio.create_task( mystop(t1) )
    print('a')
    #await t2
    print('b')
    #await t1
    try:
        await t1
    except asyncio.CancelledError:
        pass

async def foo2():
    try:
        await mystop(None)
        print('---0---')
        await c.packets_from_tshark( packet_callback=packet_print )
        print('---1---')
    except asyncio.CancelledError:
        print('---2---')
        pass
    print('======')

thread_gui = threading.Thread( target=win )
thread_gui.start()
#print('a')

#asyncio.run( c.packets_from_tshark( packet_callback=packet_print ) )
asyncio.run( foo() )

thread_gui.join()

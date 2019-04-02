# TODO: refactor and document this piece of shit

import signal
import os

data = {'filename': None, 'song_is_playing': False, 'seh': None, 'pid': None, 'load-flag': False}

def sighandler(signum, frame):
    if os.waitpid(data['pid'], os.WNOHANG) != (0, 0): # child is dead
        data['song_is_playing'] = False
        data['pid'] = None
        if not data['load-flag']:
            data['seh']()
        else:
            data['load-flag'] = False
            
def init(song_end_handler):
    data['seh'] = song_end_handler

def load(filename):
    if data['pid'] is not None:
        data['load-flag'] = True
        os.kill(data['pid'], signal.SIGKILL)
        while data['load-flag']:
            pass
    data['filename'] = filename

def unload():
    load(None)
    
def create_audio_playing_process():
    pid = os.fork()

    if pid == 0:
        os.execv('/usr/bin/mpg321', ['mpg321', data['filename'], '-q'])

    return pid

def play():
    if not is_loaded():
        return
    
    if not data['song_is_playing']:
        if data['pid'] is None:
            data['pid'] = create_audio_playing_process()
        else:            
            os.kill(data['pid'], signal.SIGCONT)
        data['song_is_playing'] = True

def pause():
    if not is_loaded():
        return
    
    if data['song_is_playing']:
        os.kill(data['pid'], signal.SIGSTOP)
        data['song_is_playing'] = False

def rewind():
    if not is_loaded():
        return
    
    # plays the current song from the beginning
    load(data['filename'])
    play()
    
def is_loaded():
    return data['filename'] is not None
    
def is_playing():
    return data['song_is_playing']
    
signal.signal(signal.SIGCHLD, sighandler)


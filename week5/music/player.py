import signal
import os

# useful metaphor:
# a Player is like a turntable
# Player.load puts the record on the turntable
# Player.play puts the needle on the record; does nothing if the needle is already on it
# Player.pause lifts the needle off the record; does nothing if the needle is not on it
# Player.unload removes the record; does nothing if there is no record

# TODO: how to handle audio playing process errors?
# TODO: only one instance of Player can exist. how to enforce this?

class Player:    
    def __init__(self, song_end_handler):
        # @song_end_handler must be a callabe which can be called with no arguments
        # everytime the song of @self ends, song_end_handler is called asynchronously

        # invariants:
        # - if self is not loaded:
        #    - self.pid filename should be None
        #    - self.song_is_playing should be None
        #    - self.pid should be None
        # - if self.filename is None, self is not loaded
        # - self.song_is_playing is True only when self.filname is not None and
        #   self.pid is not None
        
        self.filename = None
        self.song_is_playing = False
        self.song_end_handler = song_end_handler
        self.pid = None
        self.caused_the_termination = False # TODO: document

    @property
    def isloaded(self):
        return self.filename is not None

    @property
    def isplaying(self):
        return self.song_is_playing
    
    def create_audio_playing_process(self):
        # assumes self is loaded and self.pid is None
        # creates the process and starts playing it
        # TODO: think about how to handle fork and execve errors.
        #       maybe implement a custom exception PlayerError?
        
        pid = os.fork()
        if pid == 0:
            os.execv('/usr/bin/mpg321', ['mpg321', self.filename, '-q'])
            
        self.pid = pid
        self.song_is_playing = True
        
    
    def kill_audio_playing_process(self):
        # assumes self.pid is not None
        # kills the process
        # sets self.pid to None
        # sets self.song_is_playing to False
        self.send_signal_to_audio_process(signal.SIGKILL)
    
    def load(self, filename):
        if self.pid is not None:
            self.kill_audio_playing_process()
        self.filename = filename

    def play(self):
        if not self.song_is_playing:
            if self.isloaded:
                if self.pid is not None:
                    self.send_signal_to_audio_process(signal.SIGCONT)
                    self.song_is_playing = True
                else:
                    self.create_audio_playing_process()

    def send_signal_to_audio_process(self, signum):
        self.signal_received = False
        os.kill(self.pid, signum)
        while not self.signal_received:
            pass
                    
    def pause(self):
        if self.song_is_playing:
            self.send_signal_to_audio_process(signal.SIGSTOP)
            self.song_is_playing = False

    def unload(self):
        self.load(None)

    def _reset(self):
        self.pid = None
        self.song_is_playing = False

_player = None # the Player reference needed by child_handler. set up in init

def child_handler(signum, frame):
    # called when:
    #    - when the audio process resumes, because of play
    #    - the audio process suspends, because because of pause
    #    - the audio process terminates, because:
    #        - the song ended
    #        - a new song was loaded
    #        - the song was unloaded
    # !!! this function calls _player._reset() when the audio playing process terminates,
    #     so you don't have to do it

    pid, status = os.waitpid(-1, os.WNOHANG)
    
    if pid == 0: # the process was suspended or resumed
        _player.signal_received = True
        return
    
    if os.WIFSIGNALED(status):
        # an error occurred or _player killed it
        if  os.WTERMSIG(status) == signal.SIGKILL: # if was killed by the player
            _player.signal_received = True
            _player._reset()
        else:
            exit_status = os.WEXITSTATUS(status)
            # TODO: this does not work, handle errors from mpg321 better
            print('Audio process terminated with an error: {os.strerror(exit_status)}')
    elif os.WIFEXITED(status):
        # the song has ended
        # IMPORTANT: _player._reset() be called BEFORE the call to song_end_handler,
        # because the handler itself may modify them
        _player._reset()
        _player.song_end_handler()
            
def init(song_end_handler):
    signal.signal(signal.SIGCHLD, child_handler)
    global _player
    _player = Player(song_end_handler)
    return _player


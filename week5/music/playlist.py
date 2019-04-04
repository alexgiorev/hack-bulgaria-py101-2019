from song import Song
import random
import json
import os

# a playlist consists of the following attributes:
#     - a name
#     - a list of songs
#     - a current song
#     - a cycle flag

# representation:
#    - pretty self explanatory: self.name, self.songs, self.current_song_index (index into self.songs), self.cycle

# rep invariants:
#     - self.current_song_index must be a valid index in self.songs
#     - if self.songs is empty, self.current_song_index must be None


class Playlist:    
    def __init__(self, name, songs=None, cycle=False):        
        self.name = name
        self.songs = songs if songs is not None else []
        self.current_song_index = 0 if songs else None
        self.cycle = cycle

    @property
    def is_empty(self):
        return not self.songs

    @property
    def current_song(self):
        if self.current_song_index is None:
            return None
        return self.songs[self.current_song_index]

    def rewind(self):
        if not self.is_empty:
            self.current_song_index = 0
    
    def next_song(self):
        if self.is_empty:
            raise ValueError('attempted to take the next song of an empty playlist')

        if len(self.songs) == 1:
            return self.current_song if self.cycle else None
        
        if self.current_song_index == len(self.songs) - 1: # if the current song is the last one
            if self.cycle:
                self.current_song_index = 0
                return self.current_song
            else:
                return None
        else:
            self.current_song_index += 1
            return self.current_song
        
    def previous_song(self):
        if self.is_empty:
            raise ValueError('attempted to take the previous song of an empty playlist')

        if len(self.songs) == 1:
            return self.current_song if self.cycle else None
        
        if self.current_song_index == 0: # if the current song is the first one
            if self.cycle:
                self.current_song_index = len(self.songs) - 1
                return self.current_song
            else:
                return None
        else:
            self.current_song_index -= 1
            return self.current_song
    
    def add_song(self, song):
        # @song must be a Song instance
        if not self.songs:
            self.current_song_index = 0
        self.songs.append(song)

    def add_songs(self, songs):
        # @songs must be an iterable yielding Song instances
        self.songs.extend(songs)
        if self.songs and self.current_song_index is None:
            self.current_song_index = 0
            
    def shuffle(self):
        random.shuffle(self.songs)
        self.current_song_index = 0 if self.songs else None

    def contains_song_with_title(self, title):
        return title in (song.title for song in self.songs)
            
        
    @property
    def total_length(self):
        return Song.seconds_to_length(sum(song.seconds for song in self.songs))
        
    def to_dict(self):
        return {'name': self.name,
                'songs': [song.to_dict() for song in self.songs],
                'cycle': self.cycle}

    @classmethod
    def from_dict(cls, d):
        def error(msg):
            raise ValueError(f'unable to parse the dict to a Playlist object: {msg}')
        
        try:
            name = d['name']
            song_dicts = d['songs']
            cycle = d['cycle']
        except KeyError as ke:
            error('missing the key "{ke.args[0]}"')
        
        if type(name) is not str:
            error(f'd["name"] must be a string')
        
        try:
            songs = [Song.from_dict(sd) for sd in song_dicts]
        except ValueError:
            error('invalid song')

        if type(cycle) is not bool:
            error('d["cycle"] must be a boolean')
        
        return cls(name, songs, cycle)
    
    def save(self, path):
        path = os.path.join(path, f'{self.name}.playlist')
        with open(path, 'w') as f:
            f.write(json.dumps(self.to_dict(), indent=4))
        
    @classmethod
    def load(cls, path):
        with open(path) as f:
            json_str = f.read()
        try:
            json_dict = json.loads(json_str)
        except json.decoder.JSONDecodeError:
            raise ValueError(f'unable to parse the file at "{path}" to a json dict')
        return cls.from_dict(json_dict)

    def pprint(self):
        # artist column width
        acw = max(len('Artist'), *(len(song.artist) for song in self.songs))
        # title column width
        tcw = max(len('Song'), *(len(song.title) for song in self.songs))
        # length column width
        lcw = max(len('Length'), *(len(song.length) for song in self.songs))
        first_row = f'| {"Artist".ljust(acw)} | {"Song".ljust(tcw)} | {"Length".ljust(lcw)} |'
        second_row = f'| {"-" * acw} | {"-" * tcw} | {"-" * lcw} |'

        print(first_row)
        print(second_row)

        for song in self.songs:
            print(f'| {song.artist.ljust(acw)} | {song.title.ljust(tcw)} | {song.length.ljust(lcw)} |')

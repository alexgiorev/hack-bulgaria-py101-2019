from song import Song
import random
import json
import os
from positional_list import PositionalList

# a playlist consists of the following attributes:
#     - a name
#     - a list of songs
#     - a current song
#     - a cycle flag

# representation:
#    - self.name will be the name
#    - self.cycle will be the cycle flag
#    - self.songs will be a positional list containing the songs
#    - self.current_song_pos will be the position of the current song in self.songs

# rep invariants:
#     - self.current_song_pos must be a position from self.songs
#     - if self.songs is empty, self.current_song_pos must be None


class Playlist:    
    def __init__(self, name):
        self.name = name
        self.songs = PositionalList()
        self.current_song_pos = None
        self.cycle = False

    @property
    def is_empty(self):
        return self.songs.is_empty()

    @property
    def current_song(self):
        if self.is_empty:
            return None
        return self.current_song_pos.element()

    def rewind(self):
        if not self.is_empty:
            self.current_song_pos = self.songs.first()

    def next_song(self):
        if self.is_empty:
            raise ValueError('attempted to take the next song of an empty playlist')

        next_song_pos = self.songs.after(self.current_song_pos)        
        if next_song_pos is None:
            if self.cycle:
                self.current_song_pos = self.songs.first()
                return self.current_song
            else:
                return None
        else:
            self.current_song_pos = next_song_pos
            return self.current_song
            
    def previous_song(self):
        if self.is_empty:
            raise ValueError('attempted to take the next song of an empty playlist')

        prev_song_pos = self.songs.before(self.current_song_pos)        
        if prev_song_pos is None:
            if self.cycle:
                self.current_song_pos = self.songs.last()
                return self.current_song
            else:
                return None
        else:
            self.current_song_pos = prev_song_pos
            return self.current_song
    
    def add_song(self, song):
        # @song must be a Song instance
        new_pos = self.songs.add_last(song)
        if self.is_empty:
            self.current_song_pos = new_pos

    def add_songs(self, songs):
        # @songs must be an iterable yielding Song instances
        was_empty = self.is_empty
        
        for song in songs:
            self.songs.add_last(song)
            
        if not self.is_empty and was_empty:
            self.current_song_pos = self.songs.first()
            
    def shuffle(self):
        temp_list = list(self.songs)
        random.shuffle(temp_list)
        self.songs = PositionalList(temp_list)
        self.current_song_pos = self.songs.first()

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
            songs = PositionalList(Song.from_dict(sd) for sd in song_dicts)
        except ValueError:
            error('invalid song')

        if type(cycle) is not bool:
            error('d["cycle"] must be a boolean')
        
        result = cls.__new__(cls)
        result.name = name
        result.songs = songs
        result.current_song_pos = songs.first()
        result.cycle = cycle
        
        return result
    
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

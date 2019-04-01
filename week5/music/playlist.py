from song import Song
import random
import json
import os

class Playlist:    
    def __init__(self, name, songs=None, repeat=False):        
        self.name = name
        self.songs = songs if songs is not None else []
        self.csi = 0 if songs else None
        self.repeat = repeat

    def is_empty(self):
        return not self.songs

    @property
    def current_song(self):
        if self.csi is None:
            return None
        return self.songs[self.csi]
    
    def next_song(self):
        if self.is_empty():
            return None

        if self.csi == len(self.songs) - 1:
            self.csi = 0
            return self.current_song if self.repeat else None
        else:
            self.csi += 1
            return self.current_song

    def previous_song(self):
        if self.is_empty():
            return None

        if self.csi == 0:
            return None
        else:
            self.csi -= 1
            return self.current_song
    
    def add_song(self, song):
        # @song must be a Song instance
        if not self.songs:
            self.csi = 0
        self.songs.append(song)

    def add_songs(self, songs):
        # @songs must be an iterable yielding Song instances
        self.songs.extend(songs)
        if self.songs and self.csi is None:
            self.csi = 0
            
    def shuffle(self):
        random.shuffle(self.songs)
        self.csi = 0 if self.songs else None

    @property
    def total_length(self):
        return Song.seconds_to_length(sum(song.seconds for song in self.songs))
        
    def to_dict(self):
        return {'name': self.name,
                'songs': [song.to_dict() for song in self.songs],
                'repeat': self.repeat}

    @classmethod
    def from_dict(cls, d):
        errmsg = 'unable to parse the dict to a Playlist object'
        
        try:
            name = d['name']
            song_dicts = d['songs']
            repeat = d['repeat']
        except KeyError as ke:
            raise ValueError(f'{errmsg}: missing the key "{ke.args[0]}"')
        
        if type(name) is not str:
            raise ValueError(f'{errmsg}: d["name"] must be a string')
        
        try:
            songs = [Song.from_dict(sd) for sd in song_dicts]
        except ValueError:
            raise ValueError(f'{errmsg}: invalid song')

        if type(repeat) is not bool:
            raise ValueError(f'{errmsg}: d["repeat"] must be a boolean')
        
        return cls(name, songs, repeat)
    
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

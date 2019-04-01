class Song:
    def __init__(self, title, artist, album, length_str, filename):
        self.title = title
        self.artist = artist
        self.album = album
        self.seconds = Song.parse_length(length_str)
        self.filename = filename

    @staticmethod
    def parse_length(length_str):
        # returns a dict {'hours': int, 'minutes': int, 'seconds': int}
        # raises ValueError if @length_str is not parsable

        parts = length_str.split(':')
        if len(parts) == 1:
            return int(parts[0])
        elif len(parts) == 2:
            minutes, seconds = map(int, parts)
            return minutes * 60 + seconds
        elif len(parts) == 3:
            hours, minutes, seconds = map(int, parts)
            return hours * 3600 + minutes * 60 + seconds
        else:
            raise ValueError(f'unable to parse the length string "{length_str}"')

    @staticmethod
    def seconds_to_length(seconds):
        hours = seconds // 3600
        
        seconds %= 3600
        minutes = seconds // 60

        seconds %= 60

        if hours == 0:
            if minutes == 0:
                return str(seconds)
            return f'{minutes}:{seconds}'
        return f'{hours}:{minutes}:{seconds}'
        
    @property
    def minutes(self):
        # returns how many minutes there are in @self
        return self.seconds // 60
    
    @property
    def hours(self):
        # returns how many hours there are in @self
        return self.seconds // 3600
        
    @property
    def length(self):
        # returns the length of @self in human readable format
        return Song.seconds_to_length(self.seconds)
        
        
    def to_dict(self):
        return {attr_name: getattr(self, attr_name) for attr_name in
                ('title', 'artist', 'album', 'length', 'filename')}

    @classmethod
    def from_dict(cls, d):
        # if @d cannot be parsed to a Song, a ValueError will be raised
        attrs = ('title', 'artist', 'album', 'length', 'filename')
        try:
            args = [d[attr] for attr in attrs]
        except KeyError as ke:
            raise ValueError(f'unable to parse the dict to a Song: missing the key "{ke.args[0]}"')
        for attr, arg in zip(attrs, args):
            if type(arg) is not str:
                raise ValueError(f'unable to parse the dict to a Song: d["{attr}"] must be a str')
        return cls(*args)
        

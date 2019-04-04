import os
import sys
import mutagen.mp3
from player import init as player_init
from playlist import Playlist
from pprint import pprint
from song import Song

PROMPT = '> '

def parse_playlists(playlists_path):
    # @playlists_path should be a path to a directory
    # returns a dict which maps playlist names to playlists
    # the playlists are parsed from all files in @playlists_path which have the .playlist extension
    # for each .playlist file which cannot be parsed to a playlist, a message will be displayed
    
    result = {}
    playlist_filenames = [path for path in os.listdir(playlists_path) if path.endswith('.playlist')]
    for playlist_filename in playlist_filenames:
        try:
            playlist = Playlist.load(os.path.join(playlists_path, playlist_filename))
        except ValueError:
            print(f'unable to parse "{playlist_filename}"')
        result[playlist.name] = playlist
    return result

class Main:
    def __init__(self):
        if len(sys.argv) == 1:
            raise ValueError('missing playlist directory argument')
        
        path = sys.argv[1]
        
        if not os.path.isdir(path):
            raise ValueError(f'the path "{path}" must point to a directory')
        
        self.playlist_dir = path
        self.playlists = parse_playlists(path)
        self.modified_playlists = set()
        self.current_playlist = None
        
        self._init_command_handlers()
        
        def song_end_handler(): # for player_init
            next_song = self.current_playlist.next_song()
            if next_song is None:
                self.current_playlist.rewind()
                self.player.load(self.current_playlist.current_song.filename)
            else:
                self.player.load(next_song.filename)
                self.player.play()
        
        self.player = player_init(song_end_handler)
        
    def _init_command_handlers(self):
        # initializes self.handlers to a dict which maps command names to their corresponding handlers.
        # a handler is a procedure of no arguments which when called will perform the action of the command
    
        def checks_if_playlist_is_chosen(handler):
            def result():
                if self.current_playlist is None:
                    print('please select a playlist first')
                else:
                    handler()
            return result

        def checks_if_playlist_is_empty(handler):
            @checks_if_playlist_is_chosen
            def result():
                if self.current_playlist.is_empty:
                    print('current playlist is empty')
                else:
                    handler()
            return result

        def end_on_eof(handler):
            def result():
                try:
                    handler()
                except EOFError:
                    print()
            return result

        @checks_if_playlist_is_empty
        def play():
            self.player.play()

        @checks_if_playlist_is_empty
        def pause():
            self.player.pause()

        def load_and_play_if_was_playing(filename):
            was_playing = self.player.isplaying
            self.player.load(filename)
            if was_playing:
                self.player.play()

        @checks_if_playlist_is_empty
        def next_song():
            next_song = self.current_playlist.next_song()
            if next_song is None:
                print('you are at the end of the playlist')
            else:
                load_and_play_if_was_playing(next_song.filename)

        @checks_if_playlist_is_empty
        def previous_song():
            prev_song = self.current_playlist.previous_song()
            if prev_song is None:
                print('you are at the beginning of the playlist')
            else:
                load_and_play_if_was_playing(prev_song.filename)

        @checks_if_playlist_is_chosen
        def toggle_cycle():
            # if the current playlist has cycle enabled, disables it and vice versa
            self.current_playlist.cycle = not self.current_playlist.cycle

        @checks_if_playlist_is_empty
        def shuffle():
            self.current_playlist.shuffle()
            self.player.load(self.current_playlist.current_song.filename)

        @checks_if_playlist_is_empty
        def print_songs():
            for song in self.current_playlist.songs:
                if song is self.current_playlist.current_song:
                    print(f'*** {song.title}')
                else:
                    print(f'    {song.title}')

        @checks_if_playlist_is_empty
        def pprint_playlist():
            self.current_playlist.pprint()

        @end_on_eof
        def choose_playlist():
            name = input('enter playlist name: ')
            while name not in self.playlists:
                print(f'"{name}" is not a valid playlist name')
                name = input('try again: ')


            self.current_playlist = self.playlists[name]

            if self.current_playlist.is_empty:
                self.player.unload()
            else:
                self.player.load(self.current_playlist.current_song.filename)

        def print_playlists():
            # displays information about all of the playlists in the playlist collection
            for name, playlist in self.playlists.items():
                if playlist is self.current_playlist:
                    print(f'*** {name}')
                else:
                    print(f'    {name}')

        @end_on_eof
        def create_playlist():
            # creates a new playlist in the playlist collection based on
            # information entered by the user
            name = input('enter new playlist name: ')
            while name in self.playlists:
                print(f'there already exists a playlist with the name "{name}"')
                name = input('try again: ')
            new_playlist = Playlist(name)
            self.playlists[name] = new_playlist
            self.modified_playlists.add(name)

        @checks_if_playlist_is_empty
        def total_length():
            print(self.current_playlist.total_length)

        @end_on_eof
        @checks_if_playlist_is_chosen
        def add_song():
            # adds a new song in the current playlist based on information entered by the user
            
            def get_title():
                title = input('enter title: ')
                while not title or self.current_playlist.contains_song_with_title(title):
                    print('invalid title')
                    title = input('try again: ')
                return title
            
            def get_filename_and_seconds():
                filename = input('enter filename: ')
                while True:
                    try:
                        mp3 = mutagen.mp3.MP3(filename)
                    except mutagen.MutagenError:
                        print(f'"{filename}" is not a valid path name')
                        filename = input('try again: ')
                    else:
                        break
                return filename, int(mp3.info.length)
            
            # get song parts
            title = get_title()
            artist = input('enter artist: ')
            album = input('enter album: ')
            filename, seconds = get_filename_and_seconds()            
            song = Song(title, artist, album, seconds, filename)
            
            if self.current_playlist.is_empty:
                self.player.load(song.filename)
                
            self.current_playlist.add_song(song)
            self.modified_playlists.add(self.current_playlist.name)

        def remove_song():
            print('not implemented yet')

        def exit_application():
            self.keep_command_loop_going = False

        self.handlers = {'play': play,
                         'pause': pause,
                         'next': next_song,
                         'prev': previous_song,
                         'toggle-cycle': toggle_cycle,
                         'shuffle': shuffle,
                         'songs': print_songs,
                         'pprint': pprint_playlist,
                         'playlists': print_playlists,
                         'create-playlist': create_playlist,
                         'add-song': add_song,
                         'remove-song': remove_song,
                         'exit': exit_application,
                         'choose-playlist': choose_playlist,
                         'total-length': total_length,
                         'cp': choose_playlist}
        
    def start_command_loop(self):
        self.keep_command_loop_going = True
        
        try:
            while self.keep_command_loop_going:
                cmd = input(PROMPT)
                handler = self.handlers.get(cmd)
                if handler is None:
                    print(f'"{cmd}" is not a valid command name')
                else:
                    handler()
        finally:
            self.player.unload()
            
        for playlist_name in self.modified_playlists:
            answer = input(f'save "{playlist_name}"? (yes/no): ')
            while answer not in {'yes', 'no'}:
                answer = input('please enter "yes" or "no": ')
            if answer == 'yes':
                playlist = self.playlists[playlist_name]
                playlist.save(self.playlist_dir)


if __name__ == '__main__':
    m = Main()
    m.start_command_loop()

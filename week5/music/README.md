# Requirements

You need to have mpg321 installed and it must be in the directory /usr/bin/mpg321.

# How to run

`python3 main.py <playlist-dir>`
Where `<playlist-dir>` will be the directory where the new playlists will be stored. Also, if `<playlist-dir>` contains `.playlist` files,
they will be parsed to playlists inside the application.

# User interface:

From the perspective of the user, the application has 3 parts:

* the playlist table
* the current playlist
* the current song

You can see the current playlists with the `playlists` command. The current playlist will be marked with `***`. The songs of a playlist can be shown with the `songs` command. The current one is maked with `***`.

Here is a list of the rest of the commands, which are pretty self-explanatory:
* `play`
* `pause`
* `next`: move to next song (or the first one if `cycle` is on)
* `prev`: move to the previous song (or the last one if `cycle` is on)
* `toggle-cycle`: enable/disable `cycle`
* `shuffle`
* `pprint`: shows a table-like view of the current playlist
* `cp` or `choose-playlist`: switch to a new playlist
* `create-playlist`
* `add-song`
* `remove-song`
* `exit`

Some commands (like `cp`) expect you to type something. If you have changed your mind and don't want to finish typing, delete the text and press Crtl-D.

# Examples

I have made sample playlists and audio files in the `playlists` and `music` directory, if you wish to experiment with the app. To use the samples, just type on the command line `python3 main.py playlists`.

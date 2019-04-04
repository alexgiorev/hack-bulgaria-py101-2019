installation:

you need to have mpg321 installed and it must be in the directory /usr/bin/mpg321.

====================================================================================================
user interface:

from the perspective of the user, the application has 3 parts:
    - the playlist table
	- the current playlist
	- the current song

all commands somehow make use of these 3 parts

the current playlist is a playlist from the playlist table, or is None (i.e. not yet chosen).
most commands cannot work with the current playlist being None, and will display an error message if an attempt to execute them is made.

the current song is a song from the current playlist. the current song can also be None, but this happens only if the current playlist is
not chosen, or if the current playlist is empty. if there is a current song, it can be either playing or paused

whenever a song ends:
    if the current song was the last one in the playlist:
	    if the repeat option is on for the current playlist:
		    the current song becomes the first song in the playlist, and is played
		else:
		    the current song becomes the first song in the playlist, and is paused
	else:
	    the next song in the playlist is played

the program takes a single command line argument, which must be a path to a directory. all files which end in .playlist in that directory
will be parsed to playlists. if a .playlist file cannot be parsed, an error message will be displayed, but the program will still try
to parse the other files. the program does not look for .playlist files in subdirectories of the directory.

once the program starts, a prompt is shown ('> '). the user can then start entering commands, some of which accept arguments.

the commands that are supported so far are:
    - play
	    if there is a current song, plays it. it is innocuous to play an already playing song
		
	- pause
	    if there is a current song, pauses it. it is innocuous to pause an already paused song
		
	- next
	    if the playlist is not empty:
		    if the current song is the last one in the playlist and the playlist cycle option is on:
				the current song becomes the first one in the current playlist
				the current song is played only if it was playing before
			else:
			    the current song becomes the next one in the playlist
				the new current song is played only if the old current song was playing
				
	- prev
	    if the current song is the first one in the playlist, just stops it
		else, we take the song before the current song to be the new current song. if the old song was playing
		at the time of the execution of this command, the new song will be playing. the situation is similar if the
		old song was paused before executing the command

	- toggle-cycle
	    if the current playlist's cycle option is on, turns it off. if it is off, turns it on
		
	- shuffle
	    randomizes the order of the current playlist's songs.
		the current song becomes the first one in the new order, and is in a paused state

	- songs
	    prints the names of all of the songs in the current playlist, with a pointer '***' to the current song.

	- pprint
	    shows a table-like view of the current playlist

 	- cp or choose-playlist
	    set the current playlist to the name given as argument. the program will ask for a name until you enter a valid one.
		if you have changed your mind about changing the playlist, press crtl-d
	    
	- create-playlist
	    creates a new playlist in the playlist table. you must give the name as an argument. if the current name is already taken,
		you will be asked for a valid name again. to exit this loop, press crtl-d

	- add-song
        adds a song to the end of the current playlist. the user must enter the title, artist, album and filename of the song	    
		
	- remove-song
        asks the user for the name of a song and removes that song from the current playlist
		
	- exit
	    exits the application. if you have made changes to a playlist or have added new playlists, you will be asked which of them you
		want to save. they will be saved in the same directory you specified as an argument when starting the program and the names of the
		files will have the form <name>.playlist where <name> is the name of the playlist
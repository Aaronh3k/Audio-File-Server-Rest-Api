def audio_type_str_to_int(Type):
    if Type == 'SONG_FILE':
        Type = 1
    elif Type == 'PODCAST_FILE':
        Type = 2
    elif Type == 'AUDIOBOOK_FILE':
        Type = 3
    else:
        Type=None
    return Type

def audio_type_int_to_str(Type):
    if Type == 1:
        Type = 'SONG_FILE'
    elif Type == 2:
        Type = 'PODCAST_FILE'
    elif Type == 3:
        Type = 'AUDIOBOOK_FILE'
    else:
        Type=None
    return Type

def isotime(datestring):
    if datestring == None:
        return None
    else: 
        return datestring.strftime("%Y-%m-%d %H:%M:%S") 
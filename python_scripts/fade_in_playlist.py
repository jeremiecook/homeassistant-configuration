# Parameters
duration = data.get('duration', 120) # Total duration of the transition
delay = data.get('delay', 3) # Delay between each volume step
playlist = data.get('playlist', 'spotify:playlist:5PKh6LXvxvF2860ylwdPtJ') # Playlist


# Allumer l'ampli
hass.services.call('switch', 'turn_on', {'entity_id': 'switch.ampli'}, False)

# Se connecter sur Spotify
hass.services.call(
    'media_player', 'select_source', 
    {
        'entity_id': 'media_player.spotify', 
        'source': 'Michel (Pi)'  
    }, 
    False)

# Baisser le volume
hass.services.call(
    'media_player', 'volume_set', 
    {
        'entity_id': 'media_player.spotify', 
        'volume_level': '0.0'  
    }, 
    False)

# Jouer la playlist
hass.services.call(
    'spotify', 'play_playlist',
    {
       'media_content_id': playlist,
       'random_song': 'yes' # Aléatoire        
    }, 
    False)



# Tout jouer en aléatoire
time.sleep(1)
hass.services.call(
    'media_player', 'shuffle_set',
    {
       'entity_id': 'media_player.spotify',
       'shuffle': 'true' # Aléatoire        
    },
    False)
    

# Transition de volume    

steps = int (duration / delay)
step = 0

while (step <= steps):

    volume = float(step / steps)
    step = step + 1

    hass.services.call(
        'media_player', 'volume_set', 
        {
            'entity_id': 'media_player.spotify', 
            'volume_level': volume  
        }, 
        False)    

    logger.warning ("Changed volume to " + str(volume))

    time.sleep(delay)
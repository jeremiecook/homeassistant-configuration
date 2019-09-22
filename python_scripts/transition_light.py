
# Sources & Help
# https://community.home-assistant.io/t/light-fade-in/35509

# Default light steps
dawn_light = [
   [64, 0, 255, 0], # Indigo
   [64, 0, 255, 100], # Indigo + Brightness
   [255, 64, 0, 100], # Red Orange
   [255, 200, 38, 100], # Orangé vif
   [255, 255, 255, 20], # White
   [255, 255, 255, 80], # White + Brightness
]


# Parameters
entity_id = data.get('entity_id')
light_steps = data.get('light_steps', dawn_light) # Color steps of the transition
duration = int (data.get('duration', 120)) # Total duration of the transition
delay = float (data.get('delay', 2)) # Delay between each step, in seconds


total_steps = int (duration / delay)
step = 0

while step <= total_steps:
    light_step = step / total_steps * (len(light_steps) - 1)
    step = step + 1

    fromLightStep = math.floor(light_step)
    toLightStep = math.ceil(light_step)

    percentage = light_step - fromLightStep

    #logger.debug('Step: ' + str(step) + ' - From : ' + str(fromLightStep) + ' To : ' + str(toLightStep) + ' Percentage : ' + str(percentage)  )

    r = int(light_steps[fromLightStep][0] + (light_steps[toLightStep][0] - light_steps[fromLightStep][0]) * percentage)
    g = int(light_steps[fromLightStep][1] + (light_steps[toLightStep][1] - light_steps[fromLightStep][1]) * percentage)
    b = int(light_steps[fromLightStep][2] + (light_steps[toLightStep][2] - light_steps[fromLightStep][2]) * percentage)
    rgb = [r, g, b]

    brightness_pct = int(light_steps[fromLightStep][3] + (light_steps[toLightStep][3] - light_steps[fromLightStep][3]) * percentage)
    
    #logger.debug('Red: ' + str(light_steps[froms][0]) + ' to ' + str(light_steps[to][0]) + ' - Total ' + str(r) ) 
    #logger.debug('Green: ' + str(light_steps[froms][1]) + ' to ' + str(light_steps[to][1]) + ' - Total ' + str(g) ) 
    #logger.debug('Blue: ' + str(light_steps[froms][2]) + ' to ' + str(light_steps[to][2]) + ' - Total ' + str(b) ) 

    color_data = {
        'entity_id': entity_id,
        'rgb_color': rgb,
        'brightness_pct': brightness_pct
    }

    #brightness_data = {
    #    'entity_id': entity_id,
    #    'brightness_pct': brightness_pct
    #}

    logger.warning('Changed light ' + str(entity_id) + ' : Color ' + str(rgb) + ' - Brightness ' + str(brightness_pct))
    hass.services.call('light', 'turn_on', color_data, False)
    #hass.services.call('light', 'turn_on', brightness_data, False)
    time.sleep(delay)


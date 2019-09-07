
# Sources & Help
# https://community.home-assistant.io/t/light-fade-in/35509


# Parameters
entity_id = data.get('entity_id', 'light.salon')
duration = data.get('duration', 120)
delay = 2 # second

light_steps = [
   [64, 0, 255, 0], # Indigo / Luminosité 0
   [64, 0, 255, 100], # Indigo / Luminosité max
   [255, 64, 0, 100], # Rouge orangé
 #  [255, 246, 219, 100], # Orangé clair
   [255, 200, 38, 100], # Orangé vif
   [255, 255, 255, 20], # Blanc clair
  # [255, 255, 255, 50], # Blanc max
   [255, 255, 255, 80], # Blanc max
]

steps = duration / delay
step = 0

while step < steps:
    step = step + 1
    light_step = step / steps * (len(light_steps) - 1)
    froms = math.floor(light_step)
    to = math.ceil(light_step)
    percentage = light_step - froms

    logger.info('Step: ' + str(step) + ' - From : ' + str(froms) + ' To : ' + str(to) + ' Percentage : ' + str(percentage)  )
    r = int(light_steps[froms][0] + (light_steps[to][0] - light_steps[froms][0]) * percentage)
    g = int(light_steps[froms][1] + (light_steps[to][1] - light_steps[froms][1]) * percentage)
    b = int(light_steps[froms][2] + (light_steps[to][2] - light_steps[froms][2]) * percentage)
    
    rgb = [r, g, b]
    brightness_pct = int(light_steps[froms][3] + (light_steps[to][3] - light_steps[froms][3]) * percentage)
    #logger.info('Red: ' + str(light_steps[froms][0]) + ' to ' + str(light_steps[to][0]) + ' - Total ' + str(r) ) 
    #logger.info('Green: ' + str(light_steps[froms][1]) + ' to ' + str(light_steps[to][1]) + ' - Total ' + str(g) ) 
    #logger.info('Blue: ' + str(light_steps[froms][2]) + ' to ' + str(light_steps[to][2]) + ' - Total ' + str(b) ) 

    color_data = {
        'entity_id': entity_id,
        'rgb_color': rgb,
    }

    brightness_data = {
        'entity_id': entity_id,
        'brightness_pct': brightness_pct
    }

    logger.info('Luminosité de ' + str(entity_id) + ' : Couleur ' + str(rgb) + ' - Luminosité ' + str(brightness_pct))
    hass.services.call('light', 'turn_on', color_data, False)
    hass.services.call('light', 'turn_on', brightness_data, False)
    time.sleep(delay)


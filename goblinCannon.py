import obspython as obs
import random as rand
import os

#File path fo the goblins
goblinFolder = "xxxxxx"

#Set boundaries in which the goblins can spawn
minX, maxX = 0, 1920
minY, maxY = 0, 1080

#Set max and min scale sizes
minScale, maxScale = .75, 1.75

hotkey_id = obs.OBS_INVALID_HOTKEY_ID

class GoblinLauncher:
    def __init__(self, source_name=None):
        self.source_name = source_name
    
    def add_goblin(self):
        settings = obs.obs_data_create()
        scene = obs.obs_scene_from_source(obs.obs_frontend_get_current_scene())

        #Selects a random goblin from the folder
        goblinFilePath = goblinFolder + "/" +rand.choice(os.listdir(goblinFolder))
        
        #Creates a new source 
        source = obs.obs_source_create("image_source", "goblin", settings, None)
        newGoblin = obs.obs_scene_add(scene, source)
        
        #Adds the image file path to the source
        obs.obs_data_set_string(settings, "file", goblinFilePath)
        
        #Changes the position (from the top left) of the new source
        pos = obs.vec2()
        pos.x = rand.randint(minX, maxX)
        pos.y = rand.randint(minY, maxY)
        obs.obs_sceneitem_set_pos(newGoblin, pos)
        
        #Changes the scale of the goblin
        scaler = rand.uniform(minScale, maxScale)
        scale = obs.vec2()
        scale.x = scaler
        scale.y = scaler
        obs.obs_sceneitem_set_scale(newGoblin, scale)

        #Stores the goblins in the "goblin farm" group, and respositions the group if it gets moved offscreen
        group = obs.obs_scene_sceneitem_from_source(scene, obs.obs_get_source_by_name("goblin farm"))
        obs.obs_sceneitem_group_add_item(group, newGoblin)

        farmPos = obs.vec2()
        farmPos.x, farmPos.y = 0, 0
        obs.obs_sceneitem_set_pos(group, farmPos)

        #Update/pushes the changes to OBS
        obs.obs_source_update(source, settings)
        obs.obs_source_release(source)
        obs.obs_scene_release(scene)

goblin = GoblinLauncher()

def script_description():
    return "[Needs to be hotkey'd in Settings > Hotkeys > Goblin Launcher] Simply creates a goblin somewhere within the specified boundaries within the specified size range. Very cool."

def script_save(settings):
    global hotkey_id
    hotkey_save_array = obs.obs_hotkey_save(hotkey_id)
    obs.obs_data_set_array(settings, "goblinHotkey", hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)

def script_load(settings):
    global hotkey_id
    def callback(pressed):
        if pressed:
            return goblin.add_goblin()
        
    hotkey_id = obs.obs_hotkey_register_frontend("htk_hotkey", "Goblin Launch", callback)

    hotkey_save_array = obs.obs_data_get_array(settings, "goblinHotkey")
    obs.obs_hotkey_load(hotkey_id, hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)

def script_update(settings):
    goblin.source_name = obs.obs_data_get_string(settings, "source")

def script_properties():
    #Lowkey, this shit doesnt do anything useful, im just too scared to remove it and break stuff.
    props = obs.obs_properties_create()
    p = obs.obs_properties_add_list(
        props,
        "source",
        "Goblin Housing",
        obs.OBS_COMBO_TYPE_EDITABLE,
        obs.OBS_COMBO_FORMAT_STRING,
    )
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            if source_id == "image" or source_id == "text_ft2_source":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)

        obs.source_list_release(sources)
    return props


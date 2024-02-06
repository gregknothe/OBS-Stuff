import obspython as obs

hotkey_id = obs.OBS_INVALID_HOTKEY_ID

class GoblinMurderSticker:
    def __init__(self, source_name=None):
        self.source_name = source_name
    
    def goblin_murder(self):
        scene = obs.obs_scene_from_source(obs.obs_frontend_get_current_scene())    

        #Finds the goblin farm location
        group = obs.obs_scene_sceneitem_from_source(scene, obs.obs_get_source_by_name("goblin farm"))
        
        #Creates a hit list of the goblins
        goblinList = obs.obs_sceneitem_group_enum_items(group)

        #Takes the goblins out back
        for x in goblinList:
            obs.obs_sceneitem_remove(x)

        #Update/pushes the changes to OBS
        obs.obs_scene_release(scene)

goblin = GoblinMurderSticker()

def script_description():
    return "[Needs to be hotkey'd in Settings > Hotkeys > Goblin Killswitch] Kills the goblins in the goblin farm. Very not cool."

def script_save(settings):
    global hotkey_id
    hotkey_save_array = obs.obs_hotkey_save(hotkey_id)
    obs.obs_data_set_array(settings, "goblinKillHotKey", hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)

def script_load(settings):
    global hotkey_id
    def callback(pressed):
        if pressed:
            return goblin.goblin_murder()
        
    hotkey_id = obs.obs_hotkey_register_frontend("htk_hotkey2", "Goblin Kill Switch", callback)

    hotkey_save_array = obs.obs_data_get_array(settings, "goblinKillHotKey")
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


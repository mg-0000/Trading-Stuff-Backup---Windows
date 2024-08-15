from breeze_connect import BreezeConnect

api_keys = ["2K88h93=O07T2P175O1u(493734D060p", "0w$S7143J@857669k4`H7O2372K668nq"]
api_secrets = ["98328102h1332l3g4Lg5~203%4392145", "5439143UN65!xzt0#6q_70818~r6892+"]
session_tokens = ["40815484", "31418122"]
keys_used = []
breeze_objects = []

class Breeze:
    # breeze.breeze is the BreezeConnect object
    def __init__(self, key_number = 0):
        global keys_used, breeze_objects
        if key_number not in keys_used:
            keys_used.append(key_number)
            self.breeze = BreezeConnect(api_key=api_keys[key_number])
            self.breeze.generate_session(api_secret=api_secrets[key_number], session_token=str(session_tokens[key_number]))
            breeze_objects.append(self.breeze)
        else:
            print("Key already in use")
            self.breeze = breeze_objects[keys_used.index(key_number)].breeze
    

from breeze_connect import BreezeConnect
### Mridul's credentials
api_key="650G7Z51z645540%&15~b93v5*4M!574"
api_secret="409755400@8P#xT7009=x6~O58977333"
session_token="31815250"
breeze = BreezeConnect(api_key=api_key)
breeze.generate_session(api_secret=api_secret, session_token=str(session_token))

api_key_2="0w$S7143J@857669k4`H7O2372K668nq"
api_secret_2="5439143UN65!xzt0#6q_70818~r6892+"
session_token_2="31418122"
breeze_2 = BreezeConnect(api_key=api_key)
breeze_2.generate_session(api_secret=api_secret, session_token=str(session_token))



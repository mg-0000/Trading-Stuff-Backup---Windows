from breeze_connect import BreezeConnect
### Mridul's credentials
api_key="650G7Z51z645540%&15~b93v5*4M!574"
api_secret="409755400@8P#xT7009=x6~O58977333"
session_token="33128207"
breeze = BreezeConnect(api_key=api_key)
breeze.generate_session(api_secret=api_secret, session_token=str(session_token))
# print(breeze.get_customer_details(api_session=session_token))


# api_key="#1W894^w=4u2445s58QBY$4627c17435"
# api_secret="1387740386~31Q+5134%9112SymN9Z5_"
# session_token="31890409"
# breeze = BreezeConnect(api_key=api_key)
# breeze.generate_session(api_secret=api_secret, session_token=str(session_token))



api_key_2="0w$S7143J@857669k4`H7O2372K668nq"
api_secret_2="5439143UN65!xzt0#6q_70818~r6892+"
session_token_2="32113726"
breeze_2 = BreezeConnect(api_key=api_key)
breeze_2.generate_session(api_secret=api_secret, session_token=str(session_token))



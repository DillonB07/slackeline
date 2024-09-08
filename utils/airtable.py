from pyairtable import Table, Api


class AirtableManager:
    def __init__(self, api_key, base_id):
        api = Api(api_key)
        self.user_table = api.table(base_id, "Users")
        self.channel_table = api.table(base_id, "Channels")
        self.log_table = api.table(base_id, "Logs")
        print('Connected to Airtable')

    def get_user(self, user_id):
        user = self.user_table.first(formula=f"{{User ID}} = '{user_id}'")
        return user

    def update_or_add_user(self, user_id, name, whitelisted=None, admin=None):
        try:
            user = self.user_table.first(formula=f"{{User ID}} = '{user_id}'")
            if user:
                user_data = user["fields"]
                user_data["Name"] = name
                if whitelisted is not None:
                    user_data["Allowed to Phone"] = whitelisted
                if admin is not None:
                    user_data["Admin"] = admin

                self.user_table.update(user["fields"]["ID"], user_data)
            else:
                self.user_table.create({"User ID": user_id, "Name": name})
            return True
        except Exception as e:
            print(f"Error updating user in Airtable: {e}")
            return False

    def add_channel(self, channel_info):
        try:
            self.channel_table.create(channel_info)
            return True
        except Exception as e:
            print(f"Error adding channel to Airtable: {e}")
            return False

    def add_log(self, log_info):
        try:
            self.log_table.create(log_info)
            return True
        except Exception as e:
            print(f"Error adding log to Airtable: {e}")
            return False

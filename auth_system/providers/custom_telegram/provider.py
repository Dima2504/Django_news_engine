from allauth.socialaccount.providers.telegram.provider import TelegramProvider


class CustomTelegramProvider(TelegramProvider):
    id = 'custom_telegram'
    name = 'Custom Telegram'

    def extract_common_fields(self, data):
        return {
            "first_name": data.get('first_name'),
            "last_name": data.get("last_name"),
            "username": data.get("username"),
        }


provider_classes = [CustomTelegramProvider, ]
BOT_UA_MARKERS = (
    
    # Поисковые боты
    "Googlebot",
    "YandexBot",
    "Bingbot",
    "Baiduspider",
    "DuckDuckBot",
    
    # Социальные сети и мессенджеры
    "Slackbot",
    "Discordbot",
    "TelegramBot",
    "WhatsApp",
    "SkypeUriPreview",
    "Twitterbot",
    "FacebookExternalHit",
    "LinkedInBot",
    
    # Превью-генераторы
    "GoogleImageProxy",
    "Google-AMPHTML",
    "Applebot",
    
    # Аналитика и мониторинг
    "Pingdom",
    "NewRelicPinger",
    "Datadog",
    "UptimeRobot",
    
    # Библиотеки и инструменты
    "python-requests",
    "Go-http-client",
    "curl",
    "wget",
    "PostmanRuntime",
)

# Легкие боты
LIGHT_BOT_MARKERS = (
    "GoogleImageProxy",
    "Slackbot",
    "Discordbot",
)

class BotDetector:
    def __init__(self, custom_markers: list | None = None):
        self.markers = list(BOT_UA_MARKERS)
        if custom_markers:
            self.markers.extend(custom_markers)
    
    def is_bot(self, user_agent: str | None) -> bool:
        if not user_agent:
            return False
        
        ua_lower = user_agent.lower()
        for marker in self.markers:
            if marker.lower() in ua_lower:
                return True
        return False
    
    def get_bot_type(self, user_agent: str | None) -> str | None:
        if not user_agent:
            return None
        
        ua_lower = user_agent.lower()
        for marker in self.markers:
            if marker.lower() in ua_lower:
                return marker
        return None

_default_detector = BotDetector()

def is_bot(user_agent: str | None) -> bool:
    return _default_detector.is_bot(user_agent)

def get_bot_type(user_agent: str | None) -> str | None:
    return _default_detector.get_bot_type(user_agent)
from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv

@dataclass
class Config:
    token: str
    
    attention_message: str = "🔔 Attention everyone!"
    no_members_message: str = "No members found to tag. Make sure I have the necessary permissions."
    private_chat_message: str = "This command only works in groups!"
    start_message: str = "Hi! I am a bot that can tag all members in this chat. Use /tag_all to tag everyone."
    error_message: str = "Sorry, I couldn't tag everyone. Error: {}"
    permission_error_message: str = "I need to be an administrator with the right to mention all members!"
    
    rate_limit: int = 30
    
    @classmethod
    def load(cls) -> Optional['Config']:
        """Load configuration from environment variables."""
        load_dotenv()
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            return None
        return cls(token=token) 
"""
Chat repository for chat history operations.
"""
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import desc
from backend.models.chat import ChatHistory
from backend.repositories.base import BaseRepository
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class ChatRepository(BaseRepository[ChatHistory]):
    """Repository for ChatHistory model operations"""
    
    def __init__(self, session: Session):
        super().__init__(ChatHistory, session)
    
    def add_message(self, user_id: int, message: str, response: str) -> ChatHistory:
        """
        Add a chat message to history.
        
        Args:
            user_id: User ID
            message: User's message
            response: AI's response
        
        Returns:
            Created ChatHistory instance
        """
        try:
            chat = ChatHistory(
                user_id=user_id,
                message=message,
                response=response
            )
            self.session.add(chat)
            self.session.commit()
            self.session.refresh(chat)
            
            logger.info(f"Added chat message for user_id={user_id}")
            return chat
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error adding chat message: {str(e)}")
            raise
    
    def get_user_history(self, user_id: int, limit: int = 50) -> List[ChatHistory]:
        """
        Get chat history for a user.
        
        Args:
            user_id: User ID
            limit: Maximum number of messages to retrieve
        
        Returns:
            List of ChatHistory instances, ordered by timestamp descending
        """
        return (
            self.session.query(ChatHistory)
            .filter(ChatHistory.user_id == user_id)
            .order_by(desc(ChatHistory.timestamp))
            .limit(limit)
            .all()
        )
    
    def delete_user_history(self, user_id: int) -> int:
        """
        Delete all chat history for a user.
        
        Args:
            user_id: User ID
        
        Returns:
            Number of deleted records
        """
        try:
            count = (
                self.session.query(ChatHistory)
                .filter(ChatHistory.user_id == user_id)
                .delete()
            )
            self.session.commit()
            
            logger.info(f"Deleted {count} chat messages for user_id={user_id}")
            return count
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error deleting chat history: {str(e)}")
            raise
    
    def get_recent_messages(self, user_id: int, count: int = 10) -> List[ChatHistory]:
        """
        Get most recent messages for a user.
        
        Args:
            user_id: User ID
            count: Number of recent messages
        
        Returns:
            List of recent ChatHistory instances
        """
        return (
            self.session.query(ChatHistory)
            .filter(ChatHistory.user_id == user_id)
            .order_by(desc(ChatHistory.timestamp))
            .limit(count)
            .all()
        )

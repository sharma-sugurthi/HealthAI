import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import bcrypt

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    chat_history = relationship('ChatHistory', back_populates='user', cascade='all, delete-orphan')
    treatment_plans = relationship('TreatmentPlan', back_populates='user', cascade='all, delete-orphan')
    health_metrics = relationship('HealthMetric', back_populates='user', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        """Verify password"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))


class ChatHistory(Base):
    __tablename__ = 'chat_history'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='chat_history')


class TreatmentPlan(Base):
    __tablename__ = 'treatment_plans'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(200), nullable=False)
    condition = Column(String(200), nullable=False)
    plan_details = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='treatment_plans')


class HealthMetric(Base):
    __tablename__ = 'health_metrics'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    metric_type = Column(String(50), nullable=False)  # 'heart_rate', 'blood_pressure', 'glucose', etc.
    value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)
    notes = Column(Text)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='health_metrics')


class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, db_path='healthai.db'):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        """Get a new database session"""
        return self.Session()
    
    def create_user(self, username, password, full_name, age, gender):
        """Create a new user"""
        session = self.get_session()
        try:
            user = User(
                username=username,
                full_name=full_name,
                age=age,
                gender=gender
            )
            user.set_password(password)
            session.add(user)
            session.commit()
            return user
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def authenticate_user(self, username, password):
        """Authenticate a user"""
        session = self.get_session()
        try:
            user = session.query(User).filter_by(username=username).first()
            if user and user.check_password(password):
                return user
            return None
        finally:
            session.close()
    
    def get_user_by_username(self, username):
        """Get user by username"""
        session = self.get_session()
        try:
            return session.query(User).filter_by(username=username).first()
        finally:
            session.close()
    
    def add_chat_message(self, user_id, message, response):
        """Add a chat message to history"""
        session = self.get_session()
        try:
            chat = ChatHistory(
                user_id=user_id,
                message=message,
                response=response
            )
            session.add(chat)
            session.commit()
            return chat
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_chat_history(self, user_id, limit=50):
        """Get chat history for a user"""
        session = self.get_session()
        try:
            return session.query(ChatHistory).filter_by(user_id=user_id).order_by(ChatHistory.timestamp.desc()).limit(limit).all()
        finally:
            session.close()
    
    def create_treatment_plan(self, user_id, title, condition, plan_details):
        """Create a new treatment plan"""
        session = self.get_session()
        try:
            plan = TreatmentPlan(
                user_id=user_id,
                title=title,
                condition=condition,
                plan_details=plan_details
            )
            session.add(plan)
            session.commit()
            return plan
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_treatment_plans(self, user_id):
        """Get all treatment plans for a user"""
        session = self.get_session()
        try:
            return session.query(TreatmentPlan).filter_by(user_id=user_id).order_by(TreatmentPlan.created_at.desc()).all()
        finally:
            session.close()
    
    def add_health_metric(self, user_id, metric_type, value, unit, notes=None):
        """Add a health metric"""
        session = self.get_session()
        try:
            metric = HealthMetric(
                user_id=user_id,
                metric_type=metric_type,
                value=value,
                unit=unit,
                notes=notes
            )
            session.add(metric)
            session.commit()
            return metric
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_health_metrics(self, user_id, metric_type=None):
        """Get health metrics for a user"""
        session = self.get_session()
        try:
            query = session.query(HealthMetric).filter_by(user_id=user_id)
            if metric_type:
                query = query.filter_by(metric_type=metric_type)
            return query.order_by(HealthMetric.recorded_at.desc()).all()
        finally:
            session.close()

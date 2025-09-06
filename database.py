import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import json

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                rating REAL DEFAULT 5.0,
                total_sales INTEGER DEFAULT 0,
                total_purchases INTEGER DEFAULT 0,
                is_banned BOOLEAN DEFAULT FALSE,
                banned_at TIMESTAMP
            )
        ''')
        
        # Таблица объявлений
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS advertisements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                category TEXT,
                subcategory TEXT,
                price REAL,
                currency TEXT,
                condition TEXT,
                server TEXT,
                photos TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Таблица избранного
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                ad_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (ad_id) REFERENCES advertisements (id)
            )
        ''')
        
        # Таблица жалоб
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                ad_id INTEGER,
                reason TEXT,
                description TEXT,
                evidence TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending',
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (ad_id) REFERENCES advertisements (id)
            )
        ''')
        
        # Таблица интеграций
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS integrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                integration_type TEXT NOT NULL,
                url TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица чатов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                seller_id INTEGER,
                ad_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (seller_id) REFERENCES users (user_id),
                FOREIGN KEY (ad_id) REFERENCES advertisements (id)
            )
        ''')
        
        # Таблица сообщений
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                user_id INTEGER,
                message_text TEXT,
                file_path TEXT,
                message_type TEXT DEFAULT 'text',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES chats (id),
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None):
        """Добавление пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name))
        
        conn.commit()
        conn.close()
    
    def add_advertisement(self, user_id: int, title: str, description: str, category: str, 
                         subcategory: str, price: float, currency: str, condition: str, 
                         server: str, photos: str = None):
        """Добавление объявления"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO advertisements (user_id, title, description, category, subcategory, 
                                     price, currency, condition, server, photos)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, title, description, category, subcategory, price, currency, condition, server, photos))
        
        conn.commit()
        conn.close()
    
    def get_advertisements(self, limit: int = 10, offset: int = 0, category: str = None, 
                          server: str = None, min_price: float = None, max_price: float = None):
        """Получение объявлений с фильтрами"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT a.*, u.username, u.first_name, u.last_name
            FROM advertisements a
            JOIN users u ON a.user_id = u.user_id
            WHERE a.is_active = TRUE
        '''
        params = []
        
        if category:
            query += " AND a.category = ?"
            params.append(category)
        
        if server:
            query += " AND a.server = ?"
            params.append(server)
        
        if min_price is not None:
            query += " AND a.price >= ?"
            params.append(min_price)
        
        if max_price is not None:
            query += " AND a.price <= ?"
            params.append(max_price)
        
        query += " ORDER BY a.created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_advertisement_by_id(self, ad_id: int):
        """Получение объявления по ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.*, u.username, u.first_name, u.last_name
            FROM advertisements a
            JOIN users u ON a.user_id = u.user_id
            WHERE a.id = ?
        ''', (ad_id,))
        
        result = cursor.fetchone()
        conn.close()
        return result
    
    def add_favorite(self, user_id: int, ad_id: int):
        """Добавление в избранное"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR IGNORE INTO favorites (user_id, ad_id)
            VALUES (?, ?)
        ''', (user_id, ad_id))
        
        conn.commit()
        conn.close()
    
    def remove_favorite(self, user_id: int, ad_id: int):
        """Удаление из избранного"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM favorites WHERE user_id = ? AND ad_id = ?
        ''', (user_id, ad_id))
        
        conn.commit()
        conn.close()
    
    def get_user_favorites(self, user_id: int):
        """Получение избранного пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.*, u.username, u.first_name, u.last_name
            FROM favorites f
            JOIN advertisements a ON f.ad_id = a.id
            JOIN users u ON a.user_id = u.user_id
            WHERE f.user_id = ? AND a.is_active = TRUE
            ORDER BY f.created_at DESC
        ''', (user_id,))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def is_favorite(self, user_id: int, ad_id: int):
        """Проверка, есть ли объявление в избранном"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 1 FROM favorites WHERE user_id = ? AND ad_id = ?
        ''', (user_id, ad_id))
        
        result = cursor.fetchone()
        conn.close()
        return result is not None
    
    def add_complaint(self, user_id: int, ad_id: int, reason: str, description: str, evidence: str = None):
        """Добавление жалобы"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO complaints (user_id, ad_id, reason, description, evidence)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, ad_id, reason, description, evidence))
        
        conn.commit()
        conn.close()
    
    def get_complaints(self, status: str = None):
        """Получение жалоб"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if status:
            cursor.execute('''
                SELECT c.*, a.title, u.username
                FROM complaints c
                JOIN advertisements a ON c.ad_id = a.id
                JOIN users u ON c.user_id = u.user_id
                WHERE c.status = ?
                ORDER BY c.created_at DESC
            ''', (status,))
        else:
            cursor.execute('''
                SELECT c.*, a.title, u.username
                FROM complaints c
                JOIN advertisements a ON c.ad_id = a.id
                JOIN users u ON c.user_id = u.user_id
                ORDER BY c.created_at DESC
            ''')
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def add_integration(self, name: str, integration_type: str, url: str, description: str = ""):
        """Добавление интеграции"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO integrations (name, integration_type, url, description)
            VALUES (?, ?, ?, ?)
        ''', (name, integration_type, url, description))
        
        conn.commit()
        conn.close()
    
    def get_integrations(self):
        """Получение интеграций"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM integrations ORDER BY created_at DESC')
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_or_create_chat(self, user_id: int, seller_id: int, ad_id: int):
        """Получение или создание чата"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id FROM chats 
            WHERE user_id = ? AND seller_id = ? AND ad_id = ?
        ''', (user_id, seller_id, ad_id))
        
        result = cursor.fetchone()
        
        if not result:
            cursor.execute('''
                INSERT INTO chats (user_id, seller_id, ad_id)
                VALUES (?, ?, ?)
            ''', (user_id, seller_id, ad_id))
            chat_id = cursor.lastrowid
        else:
            chat_id = result[0]
        
        conn.commit()
        conn.close()
        return chat_id
    
    def get_chat_between(self, user1_id: int, user2_id: int):
        """Получение чата между двумя пользователями"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM chats 
            WHERE (user_id = ? AND seller_id = ?) OR (user_id = ? AND seller_id = ?)
        ''', (user1_id, user2_id, user2_id, user1_id))
        
        result = cursor.fetchone()
        conn.close()
        return result
    
    def get_chat_messages(self, chat_id: int, limit: int = 50):
        """Получение сообщений чата"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.*, u.username, u.first_name
            FROM messages m
            JOIN users u ON m.user_id = u.user_id
            WHERE m.chat_id = ?
            ORDER BY m.created_at DESC
            LIMIT ?
        ''', (chat_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def add_message(self, chat_id: int, user_id: int, message_text: str = None, 
                   file_path: str = None, message_type: str = "text"):
        """Добавление сообщения в чат"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO messages (chat_id, user_id, message_text, file_path, message_type)
            VALUES (?, ?, ?, ?, ?)
        ''', (chat_id, user_id, message_text, file_path, message_type))
        
        conn.commit()
        conn.close()
    
    def delete_advertisement(self, ad_id: int, user_id: int = None):
        """Удаление объявления"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute('''
                UPDATE advertisements SET is_active = FALSE 
                WHERE id = ? AND user_id = ?
            ''', (ad_id, user_id))
        else:
            cursor.execute('''
                UPDATE advertisements SET is_active = FALSE WHERE id = ?
            ''', (ad_id,))
        
        conn.commit()
        conn.close()
    
    def get_user_statistics(self, user_id: int):
        """Получение статистики пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Количество объявлений
        cursor.execute('''
            SELECT COUNT(*) FROM advertisements WHERE user_id = ? AND is_active = TRUE
        ''', (user_id,))
        ads_count = cursor.fetchone()[0]
        
        # Количество избранного
        cursor.execute('''
            SELECT COUNT(*) FROM favorites WHERE user_id = ?
        ''', (user_id,))
        favorites_count = cursor.fetchone()[0]
        
        # Рейтинг
        cursor.execute('''
            SELECT rating FROM users WHERE user_id = ?
        ''', (user_id,))
        rating = cursor.fetchone()[0] if cursor.fetchone() else 5.0
        
        conn.close()
        return {
            'ads_count': ads_count,
            'favorites_count': favorites_count,
            'rating': rating
        }
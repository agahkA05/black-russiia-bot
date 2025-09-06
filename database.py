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
                category TEXT NOT NULL,
                subcategory TEXT,
                price REAL NOT NULL,
                currency TEXT DEFAULT 'USD',
                condition TEXT DEFAULT 'new',
                location TEXT,
                server TEXT,
                photos TEXT, -- JSON массив путей к фото
                is_active BOOLEAN DEFAULT TRUE,
                views INTEGER DEFAULT 0,
                likes INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Таблица избранного
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                target_type TEXT NOT NULL, -- 'item', 'seller', 'category'
                target_id INTEGER, -- ID товара, продавца или категории
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Таблица жалоб
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                target_type TEXT NOT NULL, -- 'advertisement', 'user', 'message'
                target_id INTEGER,
                reason TEXT NOT NULL,
                description TEXT,
                evidence TEXT, -- file_id или путь к файлу
                status TEXT DEFAULT 'pending', -- 'pending', 'in_progress', 'resolved', 'rejected'
                moderator_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (moderator_id) REFERENCES users (user_id)
            )
        ''')
        
        # Таблица интеграций
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS integrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL, -- 'chat', 'channel', 'website', 'bot'
                url TEXT NOT NULL,
                description TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица чатов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                seller_id INTEGER,
                advertisement_id INTEGER,
                last_message_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (seller_id) REFERENCES users (user_id),
                FOREIGN KEY (advertisement_id) REFERENCES advertisements (id)
            )
        ''')
        
        # Таблица сообщений
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                user_id INTEGER,
                message_text TEXT,
                message_type TEXT DEFAULT 'text', -- 'text', 'photo', 'document'
                file_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES chats (id),
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, user_id: int, username: str, first_name: str, last_name: str) -> bool:
        """Добавление нового пользователя"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO users (user_id, username, first_name, last_name)
                VALUES (?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка добавления пользователя: {e}")
            return False
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Получение пользователя по ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            user = cursor.fetchone()
            
            conn.close()
            
            if user:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, user))
            return None
        except Exception as e:
            print(f"Ошибка получения пользователя: {e}")
            return None
    
    def get_user_stats(self, user_id: int) -> Dict:
        """Получение статистики пользователя"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Количество объявлений
            cursor.execute('SELECT COUNT(*) FROM advertisements WHERE user_id = ?', (user_id,))
            ads_count = cursor.fetchone()[0]
            
            # Количество избранного
            cursor.execute('SELECT COUNT(*) FROM favorites WHERE user_id = ?', (user_id,))
            favorites_count = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'ads_count': ads_count,
                'favorites_count': favorites_count
            }
        except Exception as e:
            print(f"Ошибка получения статистики: {e}")
            return {'ads_count': 0, 'favorites_count': 0}
    
    def add_advertisement(self, user_id: int, title: str, description: str, category: str, 
                         subcategory: str, price: float, currency: str, condition: str, 
                         location: str, server: str, photos: List[str]) -> bool:
        """Добавление нового объявления"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            photos_json = json.dumps(photos)
            
            cursor.execute('''
                INSERT INTO advertisements (user_id, title, description, category, subcategory,
                                         price, currency, condition, location, server, photos)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, title, description, category, subcategory, price, currency, 
                  condition, location, server, photos_json))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка добавления объявления: {e}")
            return False

    def get_advertisements(self, category: str = None) -> List[Dict]:
        """Получение объявлений"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if category:
                cursor.execute('''
                    SELECT a.*, u.username, u.first_name, u.last_name, u.rating
                    FROM advertisements a
                    LEFT JOIN users u ON a.user_id = u.user_id
                    WHERE a.category = ? AND a.is_active = 1
                    ORDER BY a.created_at DESC
                ''', (category,))
            else:
                cursor.execute('''
                    SELECT a.*, u.username, u.first_name, u.last_name, u.rating
                    FROM advertisements a
                    LEFT JOIN users u ON a.user_id = u.user_id
                    WHERE a.is_active = 1
                    ORDER BY a.created_at DESC
                ''')
            
            ads = cursor.fetchall()
            conn.close()
            
            if ads:
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, ad)) for ad in ads]
            return []
        except Exception as e:
            print(f"Ошибка получения объявлений: {e}")
            return []

    def get_advertisement(self, ad_id: int) -> dict:
        """Получить конкретное объявление по ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.*, u.username, u.first_name, u.last_name
                FROM advertisements a
                LEFT JOIN users u ON a.user_id = u.user_id
                WHERE a.id = ?
            """, (ad_id,))
            
            row = cursor.fetchone()
            conn.close()
            if row:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
            return {}
        except Exception as e:
            print(f"Ошибка получения объявления: {e}")
            return {}

    def get_user_favorites(self, user_id: int, target_type: str) -> list:
        """Получить избранное пользователя по типу"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM favorites 
                WHERE user_id = ? AND target_type = ?
                ORDER BY created_at DESC
            """, (user_id, target_type))
            
            favorites = cursor.fetchall()
            conn.close()
            return [dict(zip([col[0] for col in cursor.description], row)) for row in favorites]
        except Exception as e:
            print(f"Ошибка получения избранного: {e}")
            return []

    def add_favorite(self, user_id: int, target_type: str, target_id: int) -> bool:
        """Добавить в избранное"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Проверяем, не добавлено ли уже
            cursor.execute("""
                SELECT id FROM favorites 
                WHERE user_id = ? AND target_type = ? AND target_id = ?
            """, (user_id, target_type, target_id))
            
            if cursor.fetchone():
                conn.close()
                return False  # Уже добавлено
            
            cursor.execute("""
                INSERT INTO favorites (user_id, target_type, target_id, created_at)
                VALUES (?, ?, ?, datetime('now'))
            """, (user_id, target_type, target_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка добавления в избранное: {e}")
            return False

    def remove_favorite(self, user_id: int, target_type: str, target_id: int) -> bool:
        """Убрать из избранного"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM favorites 
                WHERE user_id = ? AND target_type = ? AND target_id = ?
            """, (user_id, target_type, target_id))
            
            conn.commit()
            conn.close()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Ошибка удаления из избранного: {e}")
            return False

    def is_favorite(self, user_id: int, target_type: str, target_id: int) -> bool:
        """Проверить, находится ли объект в избранном пользователя"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 1 FROM favorites
                WHERE user_id = ? AND target_type = ? AND target_id = ?
                LIMIT 1
            """, (user_id, target_type, target_id))
            exists = cursor.fetchone() is not None
            conn.close()
            return exists
        except Exception as e:
            print(f"Ошибка проверки избранного: {e}")
            return False

    def add_complaint(self, user_id: int, target_type: str, target_id: int, 
                      reason: str, description: str, evidence: str = None) -> bool:
        """Добавление жалобы"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO complaints (user_id, target_type, target_id, reason, description, evidence)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, target_type, target_id, reason, description, evidence))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка добавления жалобы: {e}")
            return False

    def get_pending_complaints(self) -> List[Dict]:
        """Получение новых жалоб"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT c.*, u.username as user_username, u.first_name, u.last_name
                FROM complaints c
                LEFT JOIN users u ON c.user_id = u.user_id
                WHERE c.status = 'pending'
                ORDER BY c.created_at DESC
            ''')
            
            complaints = cursor.fetchall()
            conn.close()
            
            if complaints:
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, complaint)) for complaint in complaints]
            return []
        except Exception as e:
            print(f"Ошибка получения жалоб: {e}")
            return []

    def add_integration(self, name: str, integration_type: str, url: str, description: str = None) -> bool:
        """Добавление новой интеграции"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO integrations (name, type, url, description)
                VALUES (?, ?, ?, ?)
            ''', (name, integration_type, url, description))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка добавления интеграции: {e}")
            return False

    def get_integrations(self) -> List[Dict]:
        """Получение всех интеграций"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM integrations WHERE is_active = 1 ORDER BY created_at DESC')
            integrations = cursor.fetchall()
            
            conn.close()
            
            if integrations:
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, integration)) for integration in integrations]
            return []
        except Exception as e:
            print(f"Ошибка получения интеграций: {e}")
            return []

    def create_chat(self, user_id: int, seller_id: int, advertisement_id: int = None) -> int:
        """Создание чата между пользователями"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO chats (user_id, seller_id, advertisement_id)
                VALUES (?, ?, ?)
            ''', (user_id, seller_id, advertisement_id))
            
            chat_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return chat_id
        except Exception as e:
            print(f"Ошибка создания чата: {e}")
            return 0

    def get_or_create_chat(self, user_id: int, seller_id: int, advertisement_id: int) -> int:
        """Получить существующий чат по объявлению или создать новый"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id FROM chats WHERE user_id = ? AND seller_id = ? AND advertisement_id = ?
            ''', (user_id, seller_id, advertisement_id))
            row = cursor.fetchone()
            if row:
                conn.close()
                return row[0]
            cursor.execute('''
                INSERT INTO chats (user_id, seller_id, advertisement_id)
                VALUES (?, ?, ?)
            ''', (user_id, seller_id, advertisement_id))
            chat_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return chat_id
        except Exception as e:
            print(f"Ошибка получения/создания чата: {e}")
            return 0

    def get_chat_between(self, user_id: int, seller_id: int, advertisement_id: int) -> Optional[Dict]:
        """Получить чат между пользователем и продавцом по объявлению"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM chats WHERE user_id = ? AND seller_id = ? AND advertisement_id = ?
            ''', (user_id, seller_id, advertisement_id))
            row = cursor.fetchone()
            conn.close()
            if row:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
            return None
        except Exception as e:
            print(f"Ошибка получения чата: {e}")
            return None

    def get_chat_messages(self, chat_id: int) -> List[Dict]:
        """Получить сообщения чата"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM messages WHERE chat_id = ? ORDER BY created_at ASC
            ''', (chat_id,))
            rows = cursor.fetchall()
            conn.close()
            return [dict(zip([col[0] for col in cursor.description], row)) for row in rows]
        except Exception as e:
            print(f"Ошибка получения сообщений чата: {e}")
            return []

    def add_message(self, chat_id: int, user_id: int, message_text: str, 
                   message_type: str = 'text', file_path: str = None) -> bool:
        """Добавление сообщения в чат"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO messages (chat_id, user_id, message_text, message_type, file_path)
                VALUES (?, ?, ?, ?, ?)
            ''', (chat_id, user_id, message_text, message_type, file_path))
            
            # Обновляем время последнего сообщения в чате
            cursor.execute('''
                UPDATE chats SET last_message_at = CURRENT_TIMESTAMP WHERE id = ?
            ''', (chat_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка добавления сообщения: {e}")
            return False

    def delete_advertisement(self, ad_id: int, requester_id: int, is_admin: bool = False) -> bool:
        """Удалить объявление. Разрешено владельцу или администратору."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            # Проверяем владельца
            cursor.execute('SELECT user_id FROM advertisements WHERE id = ?', (ad_id,))
            row = cursor.fetchone()
            if not row:
                conn.close()
                return False
            owner_id = row[0]
            if not is_admin and owner_id != requester_id:
                conn.close()
                return False
            cursor.execute('DELETE FROM advertisements WHERE id = ?', (ad_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка удаления объявления: {e}")
            return False
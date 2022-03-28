from flask import session


class LoginAdmin:
    """Функции входа и работы с сессией админа и выход из сессии """
    @staticmethod
    def login_admin():
        """if admin login"""
        session['admin_logged'] = 1

    @staticmethod
    def is_logged():
        """if admin in session"""
        return True if session.get("admin_logged") else False

    @staticmethod
    def logout():
        """if admin is logout"""
        session.pop('admin_logged', None)

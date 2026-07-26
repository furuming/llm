class DomainError(Exception):
    """domain層のベースのエラー"""


# User系
class UserAlreadyExistsError(DomainError):
    """既に存在するユーザー"""

    pass


class UserNotFoundError(DomainError):
    """ユーザーが見つからない"""

    pass


class UserPasswordNotSEtError(DomainError):
    """パスワード未設定エラー"""

    pass


class InvalidPasswordError(DomainError):
    """パスワードポリシー違反"""

    pass


# Contract系


class ContractNotFoundError(DomainError):
    pass

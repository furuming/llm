# API Reference

## Auth

### POST /users/register
- request: `CreateUserRequest`
- response: `CreateUserResponse`
- 認証: 不要

### POST /login
- request: `LoginRequest`
- response: `LoginResponse`
- 認証: 不要

## User

### GET /auth/get-user
- response: `AuthenticatedUserResponse`
- 認証: 必須

## Chat

> `chat_router` は `app/cmd/api/router.py` で `prefix="/chat"` として登録されています。

### POST /chat/sessions
- request: `CreateChatSessionRequest`
- response: `ChatSessionResponse`
- 認証: 必須

### GET /chat/sessions
- response: `list[ChatSessionResponse]`
- 認証: 必須

### GET /chat/sessions/{session_id}/chats
- response: `list[ChatMessageResponse]`
- 認証: 必須

### POST /chat/sessions/{session_id}/chats
- request: `content: str`
- response: `ChatMessageEntity`
- 認証: 必須

export type Role = 'user' | 'assistant';

export interface ChatMessage {
    id: string;
    role: Role;
    content: string;
    created_at: Date;
}

export interface ChatSession {
    id: string;
    title: string;
    messages: ChatMessage[];
    created_at: Date;
}
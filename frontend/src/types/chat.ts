
export interface Chat {
    id: number;
    title: string;
    created_at: string;
    updated_at: string;
}

export interface Message {
  id: number | string;
  role: "user" | "assistant";
  text: string;
  isThinking?: boolean;
}
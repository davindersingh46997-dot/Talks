
export interface Chat {
  id: string;
  title: string;
  updated_at: string;
}

export interface Message {
  id: number | string;
  role: "user" | "assistant";
  text: string;
}
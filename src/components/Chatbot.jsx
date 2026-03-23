import React, { useState } from "react";

const Chatbot = () => {
  const [chats, setChats] = useState([
    { id: 1, messages: [] }
  ]);
  const [currentChatId, setCurrentChatId] = useState(1);
  const [input, setInput] = useState("");

  const currentChat = chats.find(c => c.id === currentChatId);

  const sendMessage = () => {
    if (!input.trim()) return;

    const userMsg = { text: input, sender: "user" };
    const botMsg = { text: "Hello! I am your assistant", sender: "bot" };

    const updatedChats = chats.map(chat => {
      if (chat.id === currentChatId) {
        return {
          ...chat,
          messages: [...chat.messages, userMsg, botMsg]
        };
      }
      return chat;
    });

    setChats(updatedChats);
    setInput("");
  };

  const createNewChat = () => {
    const newChat = {
      id: Date.now(),
      messages: []
    };
    setChats([...chats, newChat]);
    setCurrentChatId(newChat.id);
  };

  return (
    <div className="main-container">

      {/* Sidebar */}
      <div className="sidebar">
        <h3>Chats</h3>
        {chats.map(chat => (
          <div
            key={chat.id}
            className={`chat-item ${chat.id === currentChatId ? "active" : ""}`}
            onClick={() => setCurrentChatId(chat.id)}
          >
            Chat {chat.id}
          </div>
        ))}

        <button onClick={createNewChat}>+ New Chat</button>
      </div>

      {/* Chat Area */}
      <div className="chat-container">
        <div className="header">Chat bot</div>

        <div className="chat-box">
          {currentChat.messages.map((msg, i) => (
            <div key={i} className={msg.sender}>
              {msg.text}
            </div>
          ))}
        </div>

        <div className="input-box">
          <input
            type="text"
            placeholder="Type Message"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button onClick={sendMessage}>➤</button>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
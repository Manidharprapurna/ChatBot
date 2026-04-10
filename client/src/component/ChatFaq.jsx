import React from "react";

const ChatFaq = ({
  questions,
  messages,
  onQuestionClick,
  selectedDept,
  chatBoxRef,
  input,
  setInput,
  sendMessage,
  isTyping,
}) => {
  return (
    <div className="chat-container">

      {/* HEADER */}
      <div className="header">
        {selectedDept ? selectedDept.name : "Select Department"}
      </div>

      {/* CHAT BOX */}
      <div className="chat-box" ref={chatBoxRef}>

        {/* QUESTIONS PANEL */}
        {questions.length > 0 && (
          <div className="questions-panel">
            {questions.map((q) => (
              <div
                key={q.id}
                className="question"
                onClick={() => onQuestionClick(q)}
              >
                {q.question}
              </div>
            ))}
          </div>
        )}

        {/*CHAT MESSAGES COLUMN */}
        <div className="chat-messages">

          {messages.map((msg, i) => (
            <div key={i} className={`message ${msg.sender}`}>
              {msg.text}
            </div>
          ))}

          {/* Typing indicator */}
          {isTyping && (
            <div className="message bot typing">
              typing...
            </div>
          )}

        </div>

      </div>

      {/* INPUT BOX */}
      <div className="input-box">
        <input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button onClick={sendMessage}>➤</button>
      </div>

    </div>
  );
};

export default ChatFaq;
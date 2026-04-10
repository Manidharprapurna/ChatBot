import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import Sidebar from "./Sidebar";
import ChatFaq from "./ChatFaq";

const API = "http://127.0.0.1:8000";

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [questions, setQuestions] = useState([]);
  const [allQuestions, setAllQuestions] = useState([]);
  const [selectedDept, setSelectedDept] = useState(null);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [showAll, setShowAll] = useState(false); 

  const chatBoxRef = useRef(null);

  // Auto scroll
  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop =
        chatBoxRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  // Typing effect
  const typeMessage = (text, callback) => {
    let index = 0;
    let current = "";

    const interval = setInterval(() => {
      if (index < text.length) {
        current += text[index];
        index++;
        callback(current);
      } else {
        clearInterval(interval);
      }
    }, 20);
  };

  // Fetch departments
  useEffect(() => {
    const fetchDepartments = async () => {
      try {
        const res = await axios.get(`${API}/api/departments/`);
        setDepartments(res.data.departments || []);
      } catch (err) {
        console.error(err);
      }
    };

    fetchDepartments();
  }, []);

  // Load questions
  const handleDepartmentClick = async (dept) => {
    setSelectedDept(dept);
    setQuestions([]);
    setMessages([]);
    setShowAll(false);

    try {
      const res = await axios.get(
        `${API}/api/departments/${dept.id}/questions/`
      );

      const all = res.data.questions || [];

      setAllQuestions(all);          
      setQuestions(all.slice(0, 3));

    } catch (err) {
      console.error(err);
    }
  };

  // FAQ answer
  const handleQuestionClick = async (q) => {
    const userMessage = {
      text: q.question,
      sender: "user",
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsTyping(true);

    try {
      const res = await axios.get(
        `${API}/api/faq/${q.id}/answer/`
      );

      const fullText = res.data.answer || "No answer";

      setIsTyping(false);

      setMessages((prev) => [
        ...prev,
        { text: "", sender: "bot" },
      ]);

      typeMessage(fullText, (text) => {
        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = {
            text,
            sender: "bot",
          };
          return updated;
        });
      });

    } catch (err) {
      console.error(err);
      setIsTyping(false);
    }
  };

  // AI CHAT
  const sendMessage = async () => {
    if (!input.trim()) return;

    const userText = input;

    setMessages((prev) => [
      ...prev,
      { text: userText, sender: "user" },
    ]);

    setInput("");
    setIsTyping(true);

    try {
      const res = await axios.post(`${API}/get/`, {
        msg: userText,
      });

      const fullText = res.data.response || "No response";

      setIsTyping(false);

      setMessages((prev) => [
        ...prev,
        { text: "", sender: "bot" },
      ]);

      typeMessage(fullText, (text) => {
        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = {
            text,
            sender: "bot",
          };
          return updated;
        });
      });

    } catch (err) {
      console.error("Chat error:", err);

      setMessages((prev) => [
        ...prev,
        { text: "Server error", sender: "bot" },
      ]);

      setIsTyping(false);
    }
  };

  // VIEW MORE HANDLER
  const handleViewMore = () => {
    setQuestions(allQuestions);
    setShowAll(true);
  };

  return (
    <div className="main-container">

      <Sidebar
        departments={departments}
        selectedDept={selectedDept}
        onSelectDept={handleDepartmentClick}
      />

      <ChatFaq
        questions={questions}
        messages={messages}
        onQuestionClick={handleQuestionClick}
        selectedDept={selectedDept}
        chatBoxRef={chatBoxRef}
        input={input}
        setInput={setInput}
        sendMessage={sendMessage}
        isTyping={isTyping}
      />

      {/* VIEW MORE BUTTON */}
      {!showAll && allQuestions.length > 3 && (
        <div style={{ textAlign: "center", margin: "10px" }}>
          <button onClick={handleViewMore}>
            View More
          </button>
        </div>
      )}

    </div>
  );
};
export default Chatbot;
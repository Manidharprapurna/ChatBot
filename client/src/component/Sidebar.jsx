import React from "react";

const Sidebar = ({ departments = [], selectedDept, onSelectDept }) => {
  return (
    <div className="sidebar">
      <h3>Departments</h3>

      {departments.length === 0 && (
        <p style={{ color: "white" }}>No departments found</p>
      )}

      {departments.map((dept) => (
        <div
          key={dept.id}
          className={`chat-item ${
            selectedDept?.id === dept.id ? "active" : ""
          }`}
          onClick={() => onSelectDept(dept)}
        >
          {dept.name}
        </div>
      ))}
    </div>
  );
};

export default Sidebar;
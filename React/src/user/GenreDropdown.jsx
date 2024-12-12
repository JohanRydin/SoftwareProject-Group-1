import React, { useState } from "react";
import "./GenreDropdown.css"; // Import CSS for styling

export const GenreDropdown = () => {
  const [isOpen, setIsOpen] = useState(false);

  // Array of data for the dropdown
  const columns = [
    Array.from({ length: 10 }, (_, i) => `Item ${i + 1}`),
    Array.from({ length: 10 }, (_, i) => `Item ${i + 11}`),
    Array.from({ length: 10 }, (_, i) => `Item ${i + 21}`),
    Array.from({ length: 10 }, (_, i) => `Item ${i + 31}`),
  ];
  if (!isOpen)
  {
    return null
  }

  return (
    <div className="dropdown-container">
      <button onClick={() => setIsOpen(!isOpen)} className="dropdown-button">
        Toggle Dropdown
      </button>
      {isOpen && (
        <div className="dropdown-menu">
          {columns.map((column, colIndex) => (
            <div key={colIndex} className="dropdown-column">
              {column.map((item, itemIndex) => (
                <div key={itemIndex} className="dropdown-item">
                  {item}
                </div>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default GenreDropdown;

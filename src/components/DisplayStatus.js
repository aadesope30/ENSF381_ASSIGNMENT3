import React from "react";

function DisplayStatus({ type, message }) {

  return (
  <div className={`status-message ${type}`}>
    {message}
    </div>
    );
}

export default DisplayStatus;
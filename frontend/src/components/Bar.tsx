import React from "react";
import "./styles/Bar.scss";
import { Link } from "react-router-dom";

function Bar() {
  return (
    <>
      <nav>
        <Link to={"/menu/"}>
          <img alt="main menu"></img>
        </Link>
        <Link to={"/projects/"}>
          <img alt="my projects"></img>
        </Link>
        <Link to={"/tasks/"}>
          <img alt="my tasks"></img>
        </Link>
      </nav>
    </>
  );
}

export default Bar;

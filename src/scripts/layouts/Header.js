import React from "react";

class Header extends React.Component {
  constructor(props) {
    super(props);
    this.state = {count: props.initialCount};
  }
  render() {
    return (
      <header className="layout_header">
        Header
      </header>
    );
  }
}

export default Header;
import React  from "react";
import Header from "./layouts/Header";

class App extends React.Component {
  constructor(props) {
    super(props);
    
    this.state = {};
  }

  render() {
    return <main className="App-wrapper">
      <Header />
    </main>;
  }
}

React.render(
  <App />, 
  document.getElementById('app')
);
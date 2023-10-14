import React from 'react';
import { Navbar, Container } from 'react-bootstrap';

const navBarStyle = {
  backgroundColor: 'lightblue',
};

const Header = ({ title }) => {
  return (
    <Navbar style={navBarStyle} bg="dark" data-bs-theme="dark">
      <Container>
        <Navbar.Brand href="/">{title}</Navbar.Brand>
      </Container>
    </Navbar>
  );
};

export default Header;

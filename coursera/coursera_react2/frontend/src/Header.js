import React from 'react';
import Jumbotron from 'react-bootstrap/Jumbotron';
import Container from 'react-bootstrap/Container';

import './static/vendors/bootstrap/css/bootstrap.min.css';
import NoAuthHeader from './NoAuthHeader.js';
import AuthedHeader from './AuthedHeader.js';


function Header(props) {
    return (
        <Jumbotron>
            <Container>
                <a className="glyphicon glyphicon-home" href="/"></a>&nbsp;
                {
                    props.authorized ? <AuthedHeader user={props.user}></AuthedHeader> : <NoAuthHeader></NoAuthHeader>
                }
            </Container>
        </Jumbotron>
    );
}

export default Header;

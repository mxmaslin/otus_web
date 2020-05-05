import React from 'react';
import axios from 'axios';
import Jumbotron from 'react-bootstrap/Jumbotron';
import Container from 'react-bootstrap/Container';

import './static/vendors/bootstrap/css/bootstrap.min.css';
import NoAuthHeader from './NoAuthHeader.js';
import AuthedHeader from './NoAuthHeader.js';

import {
    userUrl,
    coursesUrl
} from './config.js';

axios.defaults.withCredentials = true;
const headers = {
    "Content-Type": "application/json",
	"Authorization": "Token 2d559776f31c979095476aecca145783d24fb6950079dd8b433b7405b9f43870"
}

class Courses extends React.Component {
    constructor(props) {
        super(props);
        this.state = { courses: ''};
    }
    componentDidMount() {
    }
    render() {
        console.log(coursesUrl);
        return ''
    }
}

function Header(props) {
    return (
        <Jumbotron>
            <Container>
                {
                    props.authorized ?
                    <AuthedHeader user={props.user}></AuthedHeader> :
                    <NoAuthHeader></NoAuthHeader>
                }
            </Container>
        </Jumbotron>
    );
}


function Footer() {
    return (
        <Jumbotron>
            <Container>Все права защищены.</Container>
        </Jumbotron>
    );
}

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = { authorized: false, user: null};
    }
    async componentDidMount() {
        await axios.get(
            userUrl, {params: {}, headers: headers}
        ).then(response => {
            this.setState({ authorized: true });
            this.setState({ user: response.data })
        }).catch((error) => this.setState({ authorized: false }))

        await axios.get(
            coursesUrl, {params: {}, headers: headers}
        ).then(
            response => {
                console.log(this.response)
        })
    }
    render() {
        return (
            <>
                <Header authorized={this.state.authorized} user={this.state.user}/>
                <Courses />
                <Footer />
            </>
        );
    }
}

export default App;

import React, { useState, useEffect } from 'react';
import axios from 'axios';
//import cookie from 'react-cookies';
import Jumbotron from 'react-bootstrap/Jumbotron';
import Container from 'react-bootstrap/Container';

import {
    bootstrapCss,
    userUrl,
    loginUrl,
    studentSignupUrl,
    teacherSignupUrl,
    logoutUrl,
    adminUrl,
    feedbackUrl,
    myCoursesUrl,
    lecturingUrl,
    createUrl
} from './config.js';

axios.defaults.withCredentials = true;
const headers = {
    "Content-Type": "application/json",
	"Authorization": "Token 2d559776f31c979095476aecca145783d24fb6950079dd8b433b7405b9f43870"
}

function NoAuthHeader() {
    return (
        <>
            Вы не авторизованы
            <a href={loginUrl}>Войти</a>
            <a href={studentSignupUrl}>Зарегистрироваться как учащийся</a>
            <a href={teacherSignupUrl}>Зарегистрироваться как преподаватель</a>
        </>
    );
}

class AuthedHeader extends React.Component {
    render() {
        let message = '';
        if (this.props.user) {
            if (this.props.user.student) {
                message = <span>
                    Привет, { this.props.user.username }!
                    <a href={myCoursesUrl}>Твои курсы</a>
                    <a href={feedbackUrl}>Оставить отзыв</a>
                </span>
            }
            else if (this.props.user.teacher) {
                message = <span>
                    Здравствуйте, { this.props.user.first_name }.
                    <a href={lecturingUrl}>Ваши курсы</a>
                    <a href={createUrl}>Создать курс</a>
                </span>
            }
            else {
                message = <span>
                    Здравствуйте, { this.props.user.username }.
                    <a href={adminUrl}>Админка</a>
                </span>
            }
        }
        return (
            <>
                {message}
                <a href={logoutUrl}>Выйти</a>
            </>
        );
    }
}


class Courses extends React.Component {
    constructor(props) {
        super(props);
        this.state = { authorized: false, user: null};
    }
    componentDidMount() {
        axios.get(
            userUrl, {params: {}, headers: headers}
        ).then(response => {
            this.setState({ authorized: true });
            this.setState({ user: response.data })
        }).catch((error) => this.setState({ authorized: false }))
    }
    render() {
        return (
            <>
                {
                    this.state.authorized ?
                    <AuthedHeader user={this.state.user}></AuthedHeader> :
                    <NoAuthHeader></NoAuthHeader>
                }
            </>
        );
    }
}

class Header extends React.Component {
    constructor(props) {
        super(props);
        this.state = { authorized: false, user: null};
    }
    componentDidMount() {
        axios.get(
            userUrl, {params: {}, headers: headers}
        ).then(response => {
            this.setState({ authorized: true });
            this.setState({ user: response.data })
        }).catch((error) => this.setState({ authorized: false }))
    }
    render() {
        return (
            <Jumbotron>
                <Container>
                    {
                        this.state.authorized ?
                        <AuthedHeader user={this.state.user}></AuthedHeader> :
                        <NoAuthHeader></NoAuthHeader>
                    }
                </Container>
            </Jumbotron>
        );
    }
}


function Footer() {
    return (
        <Jumbotron>
            <Container>Все права защищены.</Container>
        </Jumbotron>
    );
}

function App() {
    return (
        <div>
            <Header />
            <Courses />
            <Footer />
        </div>
    );
}

export default App;

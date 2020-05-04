import React from 'react';
import axios from 'axios';
//import cookie from 'react-cookies';
import Jumbotron from 'react-bootstrap/Jumbotron';
import Container from 'react-bootstrap/Container';

import { userUrl, loginUrl, studentSignupUrl, teacherSignupUrl } from './config.js';

axios.defaults.withCredentials = true;
const headers = {
    "Content-Type": "application/json",
	"Authorization": "Token 4b10a22363a4cfb53ac096e0244eeeac29ebdd25c00731ea4067a98004027a1d"
}

//<a class="glyphicon glyphicon-home" href="{% url 'courses:course-list' %}"></a>
//{% if user.is_authenticated %}
//    {% if user.student %}
//        Привет, {{ user.username }}!
//        <a href="{% url 'courses:my-courses' %}">Твои курсы</a>
//        <a href="{% url 'feedback:feedback' %}">Оставить отзыв</a>
//        <a href="{% url 'logout' %}">Выйти</a>
//    {% elif user.teacher %}
//        Здравствуйте, {{ user.username }}
//        <a href="{% url 'courses:lecturing' %}">Ваши курсы</a>
//        <a href="{% url 'courses:create' %}">Создать курс</a>
//        <a href="{% url 'logout' %}">Выйти</a>
//    {% else %}
//        Здравствуйте, {{ user.username }}
//        <a href="{% url 'admin:index' %}">Админка</a>
//        <a href="{% url 'logout' %}">Выйти</a>
//    {% endif %}
//{% else %}
//    Вы не авторизованы
//    <a href="{% url 'login' %}?next={{ request.path }}">Войти</a>
//    <a href="{% url 'profiles:student-signup' %}">Зарегистрироваться как учащийся</a>
//    <a href="{% url 'profiles:teacher-signup' %}">Зарегистрироваться как преподаватель</a>
//{% endif %}


function NoAuthHeader() {
    return (
        <div>
            Вы не авторизованы
            <a href={loginUrl}>Войти</a>
            <a href={studentSignupUrl}>Зарегистрироваться как учащийся</a>
            <a href={teacherSignupUrl}>Зарегистрироваться как преподаватель</a>
        </div>
    );
}

function AuthedHeader() {
    return (
        <div>
            Вы авторизованы

        </div>
    );
}

class Header extends React.Component {
    constructor(props) {
        super(props);
        this.state = { authorized: false };
    }
    componentDidMount() {
        axios.get(
            userUrl, {params: {}, headers: headers}
        ).then(response => {
            this.setState({ authorized: true })
        }).catch((error) => this.setState({ authorized: false }))
    }
    render() {
        return (
            <Jumbotron>
                <Container>
                    {
                        this.state.authorized ?
                        <AuthedHeader></AuthedHeader> :
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
            <Footer />
        </div>
    );
}

export default App;

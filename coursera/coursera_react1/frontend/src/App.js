import React from 'react';
import cookie from 'react-cookies';

import './static/css/styles.css';
import './static/vendors/bootstrap/css/bootstrap.min.css';

import Jumbotron from 'react-bootstrap/Jumbotron';
import Container from 'react-bootstrap/Container';

//import $ from 'jquery';
import axios from 'axios';


//axios.defaults.baseURL = 'http://127.0.0.1:8000/api/v1/';
axios.defaults.withCredentials = true;
const header = {
    headers: {
        "Accept": "application/json",
	    'Content-Type': 'application/json',
	}
}

//axios.get(
//    'http://127.0.0.1:8000/api/v1/courses/', {}, header
//).then(function(response){
//    const courses = response.data;
//    const authToken = cookie.load('authToken');
//}).catch((err) => {console.log(err)})


//const authToken = cookie.load('authToken');



//                    <a class="glyphicon glyphicon-home" href="{% url 'courses:course-list' %}"></a>
//                    {% if user.is_authenticated %}
//                        {% if user.student %}
//                            Привет, {{ user.username }}!
//                            <a href="{% url 'courses:my-courses' %}">Твои курсы</a>
//                            <a href="{% url 'feedback:feedback' %}">Оставить отзыв</a>
//                            <a href="{% url 'logout' %}">Выйти</a>
//                        {% elif user.teacher %}
//                            Здравствуйте, {{ user.username }}
//                            <a href="{% url 'courses:lecturing' %}">Ваши курсы</a>
//                            <a href="{% url 'courses:create' %}">Создать курс</a>
//                            <a href="{% url 'logout' %}">Выйти</a>
//                        {% else %}
//                            Здравствуйте, {{ user.username }}
//                            <a href="{% url 'admin:index' %}">Админка</a>
//                            <a href="{% url 'logout' %}">Выйти</a>
//                        {% endif %}
//                    {% else %}
//                        Вы не авторизованы
//                        <a href="{% url 'login' %}?next={{ request.path }}">Войти</a>
//                        <a href="{% url 'profiles:student-signup' %}">Зарегистрироваться как учащийся</a>
//                        <a href="{% url 'profiles:teacher-signup' %}">Зарегистрироваться как преподаватель</a>
//                    {% endif %}


class Header extends React.Component {
    state = { token: '' }
    componentDidMount() {
        axios.get(
            'http://192.168.1.2:8000/api/v1/courses/', null, {header: header}
        ).then(response => {
            const token = response.headers['kuka'];
            console.log(cookie.load('kuka'));
            console.log(response.data);
            this.setState({ token });
        })
    }
    render() {
        return (
            <Jumbotron>
                <Container>
                    yay
                    { this.state.token }
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

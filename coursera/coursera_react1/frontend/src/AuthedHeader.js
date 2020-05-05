import React from 'react';
import axios from 'axios';
import Jumbotron from 'react-bootstrap/Jumbotron';
import Container from 'react-bootstrap/Container';

import './static/vendors/bootstrap/css/bootstrap.min.css';
import NoAuthHeader from './NoAuthHeader.js';

import {
    userUrl,
    logoutUrl,
    adminUrl,
    feedbackUrl,
    myCoursesUrl,
    lecturingUrl,
    createUrl,
    coursesUrl
} from './config.js';

axios.defaults.withCredentials = true;
const headers = {
    "Content-Type": "application/json",
	"Authorization": "Token 2d559776f31c979095476aecca145783d24fb6950079dd8b433b7405b9f43870"
}

class AuthedHeader extends React.Component {
    render() {
        let message = '';
        if (this.props.user) {
            if (this.props.user.student) {
                message = <span>
                    &nbsp;Привет, { this.props.user.username }!&nbsp;
                    <a href={myCoursesUrl}>Твои курсы</a>&nbsp;
                    <a href={feedbackUrl}>Оставить отзыв</a>
                </span>
            }
            else if (this.props.user.teacher) {
                message = <span>
                    Здравствуйте, { this.props.user.first_name }.&nbsp;
                    <a href={lecturingUrl}>Ваши курсы</a>&nbsp;
                    <a href={createUrl}>Создать курс</a>
                </span>
            }
            else {
                message = <span>
                    Здравствуйте, { this.props.user.username }.&nbsp;
                    <a href={adminUrl}>Админка</a>
                </span>
            }
        }
        return (
            <>
                {message}&nbsp;
                <a href={logoutUrl}>Выйти</a>
            </>
        );
    }
}

export default AuthedHeader;
import React from 'react';

import './static/vendors/bootstrap/css/bootstrap.min.css';

import {
    logoutUrl,
    adminUrl,
    feedbackUrl,
    myCoursesUrl,
    lecturingUrl,
    createUrl,
} from './config.js';


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
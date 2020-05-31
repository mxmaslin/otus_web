import React from 'react';

import './static/vendors/bootstrap/css/bootstrap.min.css';

import {
    studentSignupUrl,
    teacherSignupUrl,
    loginUrl
} from './config.js';

function NoAuthHeader() {
    return (
        <>
            Вы не авторизованы&nbsp;
            <a href={loginUrl}>Войти</a>&nbsp;
            <a href={studentSignupUrl}>Зарегистрироваться как учащийся</a>&nbsp;
            <a href={teacherSignupUrl}>Зарегистрироваться как преподаватель</a>
        </>
    );
}

export default NoAuthHeader;
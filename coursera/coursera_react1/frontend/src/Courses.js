import React from 'react';

import './static/vendors/bootstrap/css/bootstrap.min.css';

import { baseUrl } from './config.js';

const url = require('url');

function Courses(props) {
    return (
        <ul>
            {props.courses.map(
                course => <li key={course.id}><a href={url.resolve(baseUrl, course.url)}>{course.name} {course.started}</a></li>
            )}
        </ul>
    );
}

export default Courses;

import React from 'react';

import axios from 'axios';

import './static/vendors/bootstrap/css/bootstrap.min.css';

import { courseUrl } from './config.js';

axios.defaults.withCredentials = true;
const headers = {
    "Content-Type": "application/json",
	"Authorization": "Token a28c1210ef0fdec32c6ebddd5607eceefcd62ebbcae39d13d512265cf213ac10"
}

export default class Course extends React.Component {
    constructor(props) {
        super(props);
        this.state = { course: {}, courseFetching: true };
    }
    async componentDidMount() {
        const url = `${courseUrl}${this.props.id}/`;
        await axios.get(url)
        .then(response => response.data)
        .then(data => {this.setState({course: data, courseFetching: false})});
    }
    render() {
        if (this.state.courseFetching) {
            return <div>Fetching course...</div>
        }
        if (this.state.authorized) {

            return (
                <div>
                    {this.state.course}
                </div>
            )
        }
        return (
            <div>
                <p>Имя курса: {this.state.course.name}</p>
                <p>Начало курса: {this.state.course.started}</p>
                <p><a href='#'>Войдите</a>, чтобы просматривать данные курса</p>
            </div>
        )
    }
}

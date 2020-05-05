import React from 'react';
import axios from 'axios';

import './static/vendors/bootstrap/css/bootstrap.min.css';
import Header from './Header.js';
import Footer from './Footer.js';

import {
    baseUrl,
    userUrl,
    coursesUrl
} from './config.js';

const url = require('url');
axios.defaults.withCredentials = true;
const headers = {
    "Content-Type": "application/json",
	"Authorization": "Token 0a7234bc3850e79db90633c4dcbd77e092e6fe67dc8efdd7186e436738a4e766"
}


function Courses(props) {
    return (
        <ul>
            {props.courses.map(
                course => <li><a href={url.resolve(baseUrl, course.url)}>{course.name} {course.started}</a></li>
            )}
        </ul>
    );
}


class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            authorized: false,
            user: {},
            authFetching: true,
            coursesFetching: true,
            courses: []
        };
    }
    async componentDidMount() {
        await axios.get(userUrl, {params: {}, headers: headers})
        .then(response => this.setState({authorized: true, user: response.data, authFetching: false}))
        .catch((error) => this.setState({ authorized: false, authFetching: false}))

        await axios.get(coursesUrl)
        .then(response => {this.setState({courses: response.data, coursesFetching: false})})
        .catch((error) => this.setState({coursesFetching: false}))

    }
    render() {
        const { authorized, user, authFetching, coursesFetching, courses } = this.state;
        if (authFetching && coursesFetching) return <div>...Loading</div>;
        console.log(this.state.courses);
        return (
            <>
                <Header authorized={this.state.authorized} user={this.state.user} />
                <Courses courses={this.state.courses} />
                <Footer />
            </>
        );
    }
}

export default App;

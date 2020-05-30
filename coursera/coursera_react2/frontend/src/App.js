import React from 'react';
import axios from 'axios';

import './static/vendors/bootstrap/css/bootstrap.min.css';
import Header from './Header.js';
import Courses from './Courses.js';
import Footer from './Footer.js';

import {
    userUrl,
    coursesUrl
} from './config.js';

axios.defaults.withCredentials = true;
const headers = {
    "Content-Type": "application/json",
	"Authorization": "Token 5e2fb99e4a7b8be11e8101afeef3f89664a438f1bb9fff154d8d275b20ca0a61"
}


export default class App extends React.Component {
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
        .then(response => response.data)
        .then(data => this.setState({authorized: true, user: data, authFetching: false}))
        .catch((error) => this.setState({ authorized: false, authFetching: false}))

        await axios.get(coursesUrl)
        .then(response => response.data)
        .then(data => {this.setState({courses: data, coursesFetching: false})})
        .catch((error) => this.setState({coursesFetching: false}))

    }
    render() {
        const { authorized, user, authFetching, coursesFetching, courses } = this.state;
        if (authFetching && coursesFetching) return <div>...Loading</div>;
        return (
            <>
                <Header authorized={authorized} user={user} />
                <Courses courses={courses} />
                <Footer />
            </>
        );
    }
}

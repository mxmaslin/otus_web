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
	"Authorization": "Token a28c1210ef0fdec32c6ebddd5607eceefcd62ebbcae39d13d512265cf213ac10"
}


export default class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            user: {},
            authFetching: true,
            coursesFetching: true,
            courses: []
        };
    }
    async componentDidMount() {
        await axios.get(userUrl, {params: {}, headers: headers})
        .then(response => response.data)
        .then(data => this.setState({authenticated: true, user: data, authFetching: false}))
        .catch((error) => this.setState({authenticated: false, authFetching: false}))

        await axios.get(coursesUrl)
        .then(response => response.data)
        .then(data => {this.setState({courses: data, coursesFetching: false})})
        .catch((error) => this.setState({coursesFetching: false}))
    }
    render() {
        const { user, authFetching, coursesFetching, courses } = this.state;
        if (authFetching && coursesFetching) return <div>...Loading</div>;
        return (
            <div>
                <Header user={user} />
                <Courses user={user} courses={courses} />
                <Footer />
            </div>
        );
    }
}

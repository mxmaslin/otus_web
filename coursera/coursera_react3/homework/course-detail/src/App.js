import React from 'react';
import axios from 'axios';

import Container from 'react-bootstrap/Container';

import './static/vendors/bootstrap/css/bootstrap.min.css';
import Header from './Header.js';
import Footer from './Footer.js';

import {
    userUrl,
    courseUrl,
    myCoursesUrl,
    lecturingUrl
} from './config.js';

axios.defaults.withCredentials = true;
const headers = {
    "Content-Type": "application/json",
	"Authorization": "Token 258bd0696139d879baee60cb2b2f004fcb86d22a204a5b0d2f7590da1cc06357"
}

export default class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            course: {},
            user: {},
            myCourses: [],
            myLecturing: [],
            courseFetching: true,
            authFetching: true,
            myCoursesFetching: true,
            myLecturingFetching: true,
            courseId: 7,
        };
    }

    async componentDidMount() {
        await axios.get(userUrl, {params: {}, headers: headers})
        .then(response => response.data)
        .then(data => this.setState({ user: data, authFetching: false }))
        .catch((error) => this.setState({ authFetching: false }))

//        const url = `${courseUrl}${this.props.id}/`;
        const url = `${courseUrl}${this.state.courseId}/`;
        await axios.get(url, {params: {}, headers: headers})
        .then(response => response.data)
        .then(data => {this.setState({course: data, courseFetching: false})})
        .catch((error) => this.setState({ courseFetching: false }))

        await axios.get(myCoursesUrl, {params: {}, headers: headers})
        .then(response => response.data)
        .then(data => {this.setState({myCourses: data, myCoursesFetching: false})})
        .catch((error) => this.setState({ myCoursesFetching: false }))

        await axios.get(lecturingUrl, {params: {}, headers: headers})
        .then(response => response.data)
        .then(data => {this.setState({myLecturing: data, myLecturingFetching: false})})
        .catch((error) => this.setState({ myLecturing: false }))
    }

    render() {
        const authenticated = Boolean(Object.keys(this.state.user).length);

        const {course, user, courseFetching, authFetching, myCoursesFetching, myLecturingFetching, myCourses, myLecturing, courseId} = this.state;

        if (authFetching & courseFetching & myCoursesFetching & myLecturingFetching) {
            return <div>Fetching...</div>
        }

        if (authenticated) {
            if (user.is_student) {
                const myCoursesIds = myCourses.map(c => c.id);
                const isEnrolled = myCoursesIds.includes(courseId) ? true: false;
                if (isEnrolled) {
                    return (
                        <div>
                            <Header user={user} />
                            <Container>
                                <p>Имя курса: {course.name}</p>
                                <p>Начало курса: {course.started}</p>
                                <ol>
                                    {
                                       course.lessons.map(
                                           lesson => <li><p>{lesson.name}</p><p>{lesson.content}</p></li>
                                       )
                                    }
                                </ol>
                                <p><a href='#'>Покинуть курс</a></p>
                            </Container>
                            <Footer />
                        </div>
                    )
                }
                return (
                    <div>
                        <Header user={user} />
                        <Container>
                            <p>Имя курса: {course.name}</p>
                            <p>Начало курса: {course.started}</p>
                            <p><a href='#'>Запишитесь на курс</a>, чтобы просматривать уроки</p>
                        </Container>
                        <Footer />
                    </div>
                )
            }
            const myLecturingIds = myLecturing.map(c => c.id);
            const isLecturing = myLecturingIds.includes(courseId) ? true: false;
            if (isLecturing) {
                return (
                    <div>
                        <Header user={user} />
                        <Container>
                            <p>Имя курса: {course.name}</p>
                            <p>Начало курса: {course.started}</p>
                            <ol>
                                {
                                   course.lessons.map(
                                       lesson => <li><p>{lesson.name}</p><p>{lesson.content}</p></li>
                                   )
                                }
                            </ol>
                            <p><a href='#'>Отредактировать курс</a></p>
                            <p><a href='#'>Удалить курс</a></p>
                        </Container>
                        <Footer />
                    </div>
                )
            }

            return (
                <div>
                    <Header user={user} />
                    <Container>
                        <p>Имя курса: {course.name}</p>
                        <p>Начало курса: {course.started}</p>
                    </Container>
                    <Footer />
                </div>
            )
        }
        return (
            <div>
                <Header user={user} />
                <Container>
                    <p>Имя курса: {course.name}</p>
                    <p>Начало курса: {course.started}</p>
                    <p><a href='#'>Войдите</a>, чтобы просматривать данные курса</p>
                </Container>
                <Footer />
            </div>
        )
    }
}

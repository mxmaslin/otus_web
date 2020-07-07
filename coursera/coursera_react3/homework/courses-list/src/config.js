const path = require('path');
const url = require('url');
const staticPath = './static';

const myStyles = path.join(staticPath, 'css/styles.css');
const jquery = path.join(staticPath, 'vendors/jquery/jquery-3.4.1.min.js');


const baseUrl = 'http://127.0.0.1:8000';
const userUrl = url.resolve(baseUrl, 'profiles-api/v2/user/');
const loginUrl = url.resolve(baseUrl, 'auth/login/?next=/profiles/student-signup/');
const studentSignupUrl = url.resolve(baseUrl, 'profiles/student-signup/');
const teacherSignupUrl = url.resolve(baseUrl, 'profiles/teacher-signup/');
const logoutUrl = url.resolve(baseUrl, 'auth/logout/');
const adminUrl = url.resolve(baseUrl, 'admin/');
const feedbackUrl = url.resolve(baseUrl, 'feedback/');
const myCoursesUrl = url.resolve(baseUrl, 'my-courses/');
const lecturingUrl = url.resolve(baseUrl, 'lecturing/');
const createUrl = url.resolve(baseUrl, 'create/');
const coursesUrl = url.resolve(baseUrl, 'api/v1/courses/');
const courseUrl = url.resolve(baseUrl, 'api/v1/course/')

module.exports = {
    baseUrl,
    myStyles,
    jquery,
    userUrl,
    loginUrl,
    studentSignupUrl,
    teacherSignupUrl,
    logoutUrl,
    adminUrl,
    feedbackUrl,
    myCoursesUrl,
    lecturingUrl,
    createUrl,
    coursesUrl,
    courseUrl
};

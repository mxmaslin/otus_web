const path = require('path');
const url = require('url');
const staticPath = './static';

const bootstrapCss = path.join(staticPath, 'vendors/bootstrap/css/bootstrap.min.css');
const bootstrapJs = path.join(staticPath, 'vendors/bootstrap/js/bootstrap.min.js');
const myStyles = path.join(staticPath, 'css/styles.css');
const jquery = path.join(staticPath, 'vendors/jquery/jquery-3.4.1.min.js');


const baseUrl = 'http://127.0.0.1:8000';
const userUrl = url.resolve(baseUrl, 'profiles-api/v2/user');
const loginUrl = url.resolve(baseUrl, 'auth/login/?next=/profiles/student-signup');
const studentSignupUrl = url.resolve(baseUrl, 'profiles/student-signup');
const teacherSignupUrl = url.resolve(baseUrl, 'profiles/teacher-signup');

module.exports = {
    bootstrapCss,
    bootstrapJs,
    myStyles,
    jquery,
    userUrl,
    loginUrl,
    studentSignupUrl,
    teacherSignupUrl
};

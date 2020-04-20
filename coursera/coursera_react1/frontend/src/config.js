const path = require('path');
const staticPath = './static';

//const bootstrapCss = path.join(staticPath, 'vendors/bootstrap/css/bootstrap.min.css');


const bootstrapJs = path.join(staticPath, 'vendors/bootstrap/js/bootstrap.min.js');
const myStyles = path.join(staticPath, 'css/styles.css');
const jquery = path.join(staticPath, 'vendors/jquery/jquery-3.4.1.min.js');

module.exports = {bootstrapCss, bootstrapJs, myStyles, jquery};

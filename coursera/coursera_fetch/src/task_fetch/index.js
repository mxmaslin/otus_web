const axios = require('axios');
import {api_url} from './config.js'

axios.get(api_url)
    .then(function(response){
        let courses = response.data;
        let ul = $('ul.courses-fetched');
        let result = courses.map(
            course => {
             return `<li><a href='/${course.id}/'>${course.name} ${course.started}</a></li>`
        })
        result = result.join('');
        ul.append(result);
    })
var myDate = new Date();
var myDay = myDate.getDay();
// Array of days.
  var weekday = ['sunday  ', 'monday  ', 'tuesday ','wednesday  ', 'thursday  ', 'friday  ', 'saturday  '];
document.write(weekday[myDay]);
// get hour value.
var hours = myDate.getHours();
var ampm = hours >= 12 ? 'pm' : 'am';
hours = hours % 12;
hours = hours ? hours : 12;
var minutes = myDate.getMinutes();
minutes = minutes < 10 ? '0' + minutes : minutes;
var myTime = hours + " " + " : " + minutes+ ampm
document.write(myTime);

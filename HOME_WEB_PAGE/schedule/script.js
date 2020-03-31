((window) => {
  let now = moment()

  // JSON DATA
  let schedule = [
    {
      date: now,
      agenda: [
        {range: ['10:30', '12:00'], display: {h:10, m:' 30', a: 'am'}, location: 'Tired Classrom, Academic Block', desc: 'Talk by Aman Sanduja, CoFounder - Zubi.io'},
        {range: ['12:00', '01:00'], display: {h:12, m:' 00', a: 'pm'}, location: 'College Mess', desc: 'Lunch at College Mess'},
        {range: ['01:00', '01:30'], display: {h:1, m:' 00', a: 'pm'}, location: 'ALC1, Academic Block', desc: 'Introduction to Pitchathon'},
        {range: ['01:30', '02:30'], display: {h:1, m:' 30', a: 'pm'}, location: 'ALC1, Academic Block', desc: 'speed dating '},
        {range: ['02:30',  '03:30'], display: {h:'2', m:' 30', a: 'pm'}, location: 'ALC1, Academic Block', desc: 'problem statement  ( how might we )'},
        {range: ['03:30', '04:30'], display: {h:'3', m:' 30', a: 'pm'}, location: 'ALC1, Academic Block', desc: 'your idea'},
        {range: ['04:30', '05:30'], display: {h:'4', m:' 30', a: 'pm'}, location: 'ALC1, Academic Block', desc: 'snacks'},
      ]
    // },
    // {
    //   date: moment(now).add(1, 'day'),
    //   agenda: [
    //     {start: 0, end: 859, display: {h:8, m:30, a: 'am'}, location: 'ALC1, Academic Block', desc: 'Introduction to Pitchathon'},
    //     {start: 900, end: 959, display: {h:9, m:'', a: 'am'}, location: 'ALC1, Academic Block', desc: 'speed dating '},
    //     {start: 1000, end: 1159, display: {h:10, m:'', a: 'am'}, location: 'ALC1, Academic Block', desc: 'problem statement  ( how might we )'},
    //     {start: 1200, end: 1229, display: {h:'Noon', m:'', a: '-ish'}, location: 'ALC1, Academic Block', desc: 'your idea'},
    //     {start: 1230, end: 1529, display: {h:12, m:30, a: 'pm'}, location: 'ALC1, Academic Block', desc: 'snacks'},
    //     {start: 1530, end: 1900, display: {h:3, m:30, a: 'pm'}, location: 'ALC1, Academic Block', desc: 'business model '},
    //     {start: 1901, end: 1959, display: {h:7, m:'', a: 'pm'}, location: 'ALC1, Academic Block', desc: 'Dinner!'}
    //   ]
    // },
    // {
    //   date: moment(now).add(2, 'day'),
    //   agenda: [
    //     {start: 0, end: 829, display: {h:8, m:30, a: 'am'}, location: 'Underscore Coffee Bar', desc: 'market research '},
    //     {start: 1000, end: 1159, display: {h:10, m:'', a: 'am'}, location: '', desc: 'kahoot'},
    //     {start: 1200, end: 1229, display: {h:'Noon', m:'', a: '-ish'}, location: 'midnight snacks'},
    //     {start: 1230, end: 1529, display: {h:12, m:30, a: 'pm'}, location: '', desc: 'product ( MVP ) / value proposition'},
    //     {start: 1530, end: 1900, display: {h:3, m:30, a: 'pm'}, location: 'competitors'},
    //   ]
    }
  ]

  let timeFromNum = (num, sep, ampm) => {
    let hh = parseInt(num)
    let mm = Math.round((num-hh) * 60)
    sep = sep || ''
    return (hh>12&&ampm?hh-12:hh)+sep+('00'+mm).substr(-2)+(ampm?(hh>11?' pm':' am'):'')
  }

  let numFromTime = (time) => {
    let set = time.split(/[.:]/)
    let hh = parseInt(set[0])
    let mm = set[1] ? parseInt(set[1]) : 0
    return parseFloat((hh + mm / 60).toFixed(1))
  }

  let app = new Vue({
    el: 'aside',
    data: {
      now: numFromTime(moment(now).format('HH:mm')),
      time: moment().format('h:mm a'),
      showTimeTraveller: false
    }
  })

  let sked = new Vue({
    el: 'main',
    filters: {
      date: function(date) {
        return date.format('ddd, MMM D');
      }
    },
    data: {
      now: numFromTime(moment(now).format('HH:mm')),
      schedule: schedule
    },
    methods: {
      checkTime: function(ts, te) {
        return (this.now >= numFromTime(ts) && this.now < numFromTime(te))
      }
    }
  })

  let setClockPos = () => {
    setTimeout(() => {
      let anchor = document.querySelector('.current')
      let t = '1em'
      if(anchor) {
        t = Math.round(anchor.getBoundingClientRect().top) + 'px'
      }
      document.documentElement.style.setProperty('--y', t)
    }, 350)
  }
  
  let timeTraveler

  let setTime = function() {
    let now = moment()
    app.now = sked.now = numFromTime(moment(now).format('HH:mm'))
    app.time = moment(now).format('h:mm a')
  }

  let runTimer = () => {
    setClockPos()
    timeTraveler = setInterval(function() {
      setTime()
    }, 30000)
  }

  runTimer()

  document.querySelector('#traveler').addEventListener('input', (e) => {
    app.time = timeFromNum(e.target.value, ':', true)
    sked.now = e.target.value
    setClockPos()
    clearInterval(timeTraveler)
  }, false)

  document.querySelector('.control header').addEventListener('click', (e) => {
    setTime()
    runTimer()
  }, false)

  let randum = function(min, max) {
    return Math.round((Math.random() * min) + (Math.random() * max));
  }

  let randex = function() {
    return '#' + ( '00' + Math.floor( Math.random() * 16777216 ).toString(16) ).substr(-6)
  }
  
  let colorizer = () => {
    let hex = randex()
    let reverseHex = '#' + hex.replace('#', '').split("").reverse().join("")
    document.documentElement.style.setProperty('--bg', hex)
    document.documentElement.style.setProperty('--accent', reverseHex)
  }

  let transformer = () => {
    document.documentElement.style.setProperty('--transform', 'translate(-50%, -50%) rotate(' + randum(-360, 360) + 'deg)');
  }

  setTimeout(() => {
    colorizer()
  }, 1000)  
  
  setTimeout(() => {
    transformer()
  }, 100)
  
  let adventureTime = window.setInterval(function() {
    colorizer()
  }, 7500);

  let partyTime = window.setInterval(function() {
    transformer()
  }, 12000);

  // resize capture
  let resizeTimer
  window.addEventListener('resize', (e) => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      setClockPos()
    }, 60);
  }, false)
  
})(window)
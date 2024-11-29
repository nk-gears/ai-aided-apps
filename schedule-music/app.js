// Register the service worker
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('service-worker.js').then(() => {
      console.log('Service Worker Registered');
    });
  }
  
  // Application logic
  const scheduleForm = document.getElementById('scheduleForm');
  const messageDiv = document.getElementById('message');
  
  let scheduledTasks = [];
  
  scheduleForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const time = document.getElementById('time').value;
    const track = document.getElementById('track').value;
  
    const playbackTime = new Date();
    const [hours, minutes] = time.split(':');
    playbackTime.setHours(hours, minutes, 0, 0);
  
    scheduledTasks.push({ time: playbackTime, track });
    messageDiv.innerText = `Scheduled ${track} at ${time}`;
  
    checkSchedule();
  });
  
  function checkSchedule() {
    setInterval(() => {
      const now = new Date();
      scheduledTasks.forEach((task, index) => {
        if (Math.abs(task.time - now) < 1000) {
          playMusic(task.track);
          scheduledTasks.splice(index, 1);
        }
      });
    }, 1000);
  }
  
  function playMusic(track) {
    const audio = new Audio(`assets/music/${track}`);
    audio.play();
  }
  
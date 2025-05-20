// audioUtils.js - 음악 재생 관련 유틸리티 함수들

// 오디오 상태 객체
let audioState = {
  currentAudio: null,      // 현재 재생 중인 Audio 객체
  currentMusicId: 0,       // 현재 재생 중인 음악 ID
  isPlaying: false,        // 재생 중 여부
  progress: 0,             // 재생 진행률 (0-100)
  progressInterval: null   // 진행률 업데이트를 위한 interval
};

// 음악 재생 함수
function playMusic(music) {
  // 이미 재생 중인 음악이 있으면 중지
  if (audioState.currentAudio) {
    audioState.currentAudio.pause();
    clearInterval(audioState.progressInterval);
  }

  // 새 음악 재생
  const newAudio = new Audio(music.musicUrl);
  newAudio.play();

  // 상태 업데이트
  audioState.currentAudio = newAudio;
  audioState.currentMusicId = music.musicId;
  audioState.isPlaying = true;

  // 서버에 재생 상태 저장
  fetch('/api/audio/play', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      musicId: music.musicId,
      musicUrl: music.musicUrl
    })
  }).catch(error => {
    console.error('음악 재생 상태 저장 오류:', error);
  });

  // 진행률 업데이트 설정
  audioState.progressInterval = setInterval(() => {
    getCurrentMusicProgress();
  }, 100);

  return true;
}

// 음악 중지 함수
function stopMusic() {
  if (audioState.currentAudio) {
    audioState.currentAudio.pause();
    audioState.isPlaying = false;

    // 진행률 업데이트 중지
    clearInterval(audioState.progressInterval);

    // 서버에 중지 상태 저장
    fetch('/api/audio/stop', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    }).catch(error => {
      console.error('음악 중지 상태 저장 오류:', error);
    });

    return true;
  }

  return false;
}

// 오디오 객체 제거 함수
function removeAudio() {
  if (audioState.currentAudio) {
    audioState.currentAudio.pause();
    audioState.currentAudio = null;
    audioState.currentMusicId = 0;
    audioState.isPlaying = false;

    // 진행률 업데이트 중지
    clearInterval(audioState.progressInterval);

    // 서버에 제거 상태 저장
    fetch('/api/audio/remove', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    }).catch(error => {
      console.error('음악 제거 상태 저장 오류:', error);
    });

    return true;
  }

  return false;
}

// 현재 음악 진행률 업데이트 함수
function getCurrentMusicProgress() {
  if (audioState.currentAudio && audioState.isPlaying) {
    const currentProgress = (audioState.currentAudio.currentTime / audioState.currentAudio.duration) * 100;
    audioState.progress = currentProgress;

    // 진행률 표시 업데이트 (DOM 요소가 있는 경우)
    const progressElement = document.querySelector(`.musicContainer[data-music-id="${audioState.currentMusicId}"] .progress`);
    if (progressElement) {
      progressElement.style.width = `${currentProgress}%`;
    }

    // 10% 단위로 서버에 진행 상태 업데이트 (너무 자주 요청하지 않도록)
    if (Math.floor(currentProgress) % 10 === 0) {
      fetch('/api/audio/progress', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          progress: currentProgress
        })
      }).catch(error => {
        console.error('진행 상태 업데이트 오류:', error);
      });
    }

    return currentProgress;
  }

  return 0;
}

// 페이지 로드 시 서버에서 오디오 상태 가져오기
function loadAudioState() {
  fetch('/api/audio/state')
    .then(response => response.json())
    .then(data => {
      if (data.success && data.response) {
        const state = data.response;

        // 상태 업데이트
        audioState.currentMusicId = state.currentMusicId;
        audioState.isPlaying = state.isPlaying;
        audioState.progress = state.progress;

        // 재생 중이었던 경우 다시 재생
        if (state.isPlaying && state.musicUrl) {
          const music = {
            musicId: state.currentMusicId,
            musicUrl: state.musicUrl
          };

          // 음악 재생
          playMusic(music);

          // 이미 재생되던 위치로 이동 (선택사항)
          if (audioState.currentAudio && state.progress > 0) {
            const duration = audioState.currentAudio.duration;
            if (!isNaN(duration)) {
              const currentTime = (state.progress / 100) * duration;
              audioState.currentAudio.currentTime = currentTime;
            }
          }
        }
      }
    })
    .catch(error => {
      console.error('오디오 상태 로드 오류:', error);
    });
}

// DOM이 로드된 후 오디오 상태 로드
document.addEventListener('DOMContentLoaded', loadAudioState);
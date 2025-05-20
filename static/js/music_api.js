/**
 * 음악 관련 API 함수
 */

// 플레이리스트 가져오기
async function getPlayList() {
  try {
    const response = await window.api.httpRequest('/playlist', {
      method: 'GET'
    });
    return response.response.music;
  } catch (error) {
    console.error('플레이리스트 로드 오류:', error);
    throw error;
  }
}

// 내 플레이리스트 가져오기 (인증 필요)
async function getMyPlayList() {
  try {
    const response = await window.api.authorizationRequest('/myplaylist', {
      method: 'GET'
    });
    return response.response.music;
  } catch (error) {
    console.error('내 플레이리스트 로드 오류:', error);
    throw error;
  }
}

// 인기 플레이리스트 가져오기
async function getPopularPlayList() {
  try {
    const token = localStorage.getItem('accessToken');
    const requestFunc = token ? window.api.authorizationRequest : window.api.httpRequest;

    const response = await requestFunc('/popular-playlist', {
      method: 'GET'
    });
    return response.response.music;
  } catch (error) {
    console.error('인기 플레이리스트 로드 오류:', error);
    throw error;
  }
}

// 음악 좋아요
async function postMusicLike(musicId) {
  try {
    const response = await window.api.authorizationRequest(`/music/${musicId}/like`, {
      method: 'POST',
      body: { musicId }
    });
    return response;
  } catch (error) {
    console.error('음악 좋아요 오류:', error);
    throw error;
  }
}

// 음악 생성
async function postGenerateMusic(prompt1, prompt2) {
  try {
    const response = await window.api.httpRequest('/generate-music', {
      method: 'POST',
      body: { prompt1, prompt2 }
    });
    return response;
  } catch (error) {
    console.error('음악 생성 오류:', error);
    throw error;
  }
}

// 회원 음악 생성 (인증 필요)
async function postMemberGenerateMusic(prompt1, prompt2) {
  try {
    const response = await window.api.authorizationRequest('/generate-music', {
      method: 'POST',
      body: { prompt1, prompt2 }
    });
    return response;
  } catch (error) {
    console.error('음악 생성 오류:', error);
    throw error;
  }
}

// 이미지로 음악 생성
async function postFormData(formData) {
  try {
    const token = localStorage.getItem('accessToken');
    const requestFunc = token ? window.api.imageMemberRequest : window.api.imageRequest;

    const response = await requestFunc('/generate-music/image', formData);
    return response;
  } catch (error) {
    console.error('이미지 업로드 오류:', error);
    throw error;
  }
}

// API 함수들을 전역으로 노출
window.musicApi = {
  getPlayList,
  getMyPlayList,
  getPopularPlayList,
  postMusicLike,
  postGenerateMusic,
  postMemberGenerateMusic,
  postFormData
};
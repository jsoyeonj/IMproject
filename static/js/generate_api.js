/**
 * 이미지 및 음악 생성 관련 API 함수
 */

// 이미지로 음악 생성 함수
async function handleImageUpload(formData) {
  try {
    // 로딩 상태 활성화
    showLoading();

    // API 요청
    const response = await fetch('/api/generate-music/image', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    // 로딩 상태 비활성화
    hideLoading();

    if (data.success) {
      // 성공 시 처리
      alert('음악이 성공적으로 생성되었습니다.');

      // 생성된 음악 URL을 localStorage에 저장
      if (data.response && data.response.musicUrl) {
        localStorage.setItem('currentMusicUrl', data.response.musicUrl);
      }

      // 완료 페이지로 이동
      window.location.href = '/createEnd';
    } else {
      // 실패 시 처리
      alert('이미지 업로드에 실패했습니다: ' + (data.error || '알 수 없는 오류'));
    }
  } catch (error) {
    // 로딩 상태 비활성화
    hideLoading();
    alert('요청 중 오류가 발생했습니다: ' + error);
  }
}

// 텍스트로 음악 생성 함수 (일반)
async function generateMusic(prompts) {
  try {
    // 로딩 상태 활성화
    showLoading();

    // API 요청
    const response = await fetch('/api/generate-music', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(prompts)
    });

    const data = await response.json();

    // 로딩 상태 비활성화
    hideLoading();

    if (data.success) {
      // 성공 시 처리
      alert('음악이 성공적으로 생성되었습니다.');

      // 생성된 음악 URL을 localStorage에 저장
      if (data.response && data.response.musicUrl) {
        localStorage.setItem('currentMusicUrl', data.response.musicUrl);
      }

      // 완료 페이지로 이동
      window.location.href = '/createEnd';
    } else {
      // 실패 시 처리
      alert('음악 생성에 실패했습니다: ' + (data.error || '알 수 없는 오류'));
    }
  } catch (error) {
    // 로딩 상태 비활성화
    hideLoading();
    alert('요청 중 오류가 발생했습니다: ' + error);
  }
}

// 텍스트로 음악 생성 함수 (회원)
async function generateMemberMusic(prompts) {
  try {
    // 로딩 상태 활성화
    showLoading();

    // API 요청 (인증 토큰 포함)
    const response = await fetch('/api/member/generate-music', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': localStorage.getItem('accessToken')
      },
      body: JSON.stringify(prompts)
    });

    const data = await response.json();

    // 로딩 상태 비활성화
    hideLoading();

    if (data.success) {
      // 성공 시 처리
      alert('음악이 성공적으로 생성되었습니다.');

      // 생성된 음악 URL을 localStorage에 저장
      if (data.response && data.response.musicUrl) {
        localStorage.setItem('currentMusicUrl', data.response.musicUrl);
      }

      // 완료 페이지로 이동
      window.location.href = '/createEnd';
    } else {
      // 실패 시 처리
      alert('음악 생성에 실패했습니다: ' + (data.error || '알 수 없는 오류'));
    }
  } catch (error) {
    // 로딩 상태 비활성화
    hideLoading();
    alert('요청 중 오류가 발생했습니다: ' + error);
  }
}

// 로딩 표시 함수
function showLoading() {
  const loadingElement = document.getElementById('loading-component');
  if (loadingElement) {
    loadingElement.style.display = 'flex';
  }
}

// 로딩 숨김 함수
function hideLoading() {
  const loadingElement = document.getElementById('loading-component');
  if (loadingElement) {
    loadingElement.style.display = 'none';
  }
}

// 전역 객체에 함수 추가
window.generateApi = {
  handleImageUpload,
  generateMusic,
  generateMemberMusic
};
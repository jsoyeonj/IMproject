/**
 * 회원 상태 관리를 위한 JavaScript 함수
 */

// 전역 상태 객체
window.memberState = {
  isMember: false
};

// 회원 상태 확인 함수
function checkIsMember() {
  // localStorage에서 accessToken 확인
  const accessToken = localStorage.getItem('accessToken');

  // 세션 스토리지에서도 확인 (Flask 세션과 연동)
  const sessionMember = sessionStorage.getItem('is_member');

  // 서버에서 회원 상태 확인
  fetch('/check_member')
    .then(response => response.json())
    .then(data => {
      const isMember = accessToken !== null || data.is_member === true || sessionMember === 'true';
      window.memberState.isMember = isMember;

      // 회원 상태 변경 이벤트 발생
      const event = new CustomEvent('memberStateChanged', { detail: { isMember } });
      document.dispatchEvent(event);

      return isMember;
    })
    .catch(error => {
      console.error('회원 상태 확인 중 오류:', error);
      return false;
    });
}

// 로그아웃 함수
function logOut() {
  // localStorage에서 토큰 제거
  localStorage.removeItem('accessToken');

  // 세션 스토리지에서도 제거
  sessionStorage.removeItem('is_member');

  // 서버에 로그아웃 요청
  fetch('/auth/logout', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // 회원 상태 업데이트
      window.memberState.isMember = false;

      // 회원 상태 변경 이벤트 발생
      const event = new CustomEvent('memberStateChanged', { detail: { isMember: false } });
      document.dispatchEvent(event);

      // 페이지 새로고침 또는 홈페이지로 이동
      window.location.href = '/';
    }
  })
  .catch(error => {
    console.error('로그아웃 중 오류:', error);
  });
}

// 페이지 로드 시 회원 상태 확인
document.addEventListener('DOMContentLoaded', function() {
  checkIsMember();
});

// 회원 API 함수를 전역에 노출
window.memberApi = {
  checkIsMember: checkIsMember,
  logOut: logOut,
  isMember: function() {
    return window.memberState.isMember;
  }
};

// 회원 상태에 따른 UI 업데이트 예시
function updateUI() {
  const isMember = window.memberState.isMember;

  // 회원 상태에 따라 UI 요소 표시/숨김
  const memberElements = document.querySelectorAll('.member-only');
  const guestElements = document.querySelectorAll('.guest-only');

  memberElements.forEach(element => {
    element.style.display = isMember ? 'block' : 'none';
  });

  guestElements.forEach(element => {
    element.style.display = isMember ? 'none' : 'block';
  });
}

// 회원 상태 변경 이벤트 리스너
document.addEventListener('memberStateChanged', updateUI);
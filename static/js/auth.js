function handleGoogleLogin() {
  // Google 로그인 구현
  console.log("Google login initiated");

  // Google OAuth 엔드포인트로 리디렉션
  window.location.href = "/auth/google";
}
// 로그아웃 처리 함수
function handleLogOut() {
  // 서버에 로그아웃 요청
  fetch('/auth/logout', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  })
  .then(response => {
    if (response.ok) {
      // 로그아웃 성공시 홈페이지로 이동
      window.location.href = '/';
    } else {
      console.error('로그아웃 실패');
    }
  })
  .catch(error => {
    console.error('로그아웃 요청 오류:', error);
  });
}
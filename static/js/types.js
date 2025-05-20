/**
 * 구글 로그인 응답 형식
 * @typedef {Object} GoogleLoginRes
 * @property {boolean} success - 성공 여부
 * @property {Object} response - 응답 객체
 * @property {string} response.accessToken - 액세스 토큰
 * @property {null} error - 에러 (성공시 null)
 */

/**
 * 토큰 형식
 * @typedef {Object} Token
 * @property {string} accessToken - 액세스 토큰
 */

// 타입 정의를 전역으로 노출 (필요한 경우)
window.types = {
  // 여기에 타입 관련 유틸리티 함수를 추가할 수 있습니다
};
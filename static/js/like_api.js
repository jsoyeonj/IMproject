/**
 * 좋아요 기능을 위한 API 함수
 */

// 음악 좋아요 함수
function postMusicLike(musicId) {
  return fetch(`/api/music/${musicId}/like`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ musicId: musicId })
  })
  .then(response => {
    if (!response.ok) {
      if (response.status === 409) {
        throw new Error('이미 좋아요를 누른 음악입니다.');
      }
      throw new Error('좋아요 처리 중 오류가 발생했습니다.');
    }
    return response.json();
  })
  .then(data => {
    // 좋아요 성공 후 처리
    alert('해당 음악에 좋아요 표시를 했습니다.');
    // 페이지 새로고침으로 목록 업데이트 (React Query의 invalidateQueries 대체)
    window.location.reload();
    return data;
  })
  .catch(error => {
    alert(error.message || '좋아요 처리 중 오류가 발생했습니다.');
    throw error;
  });
}

// 좋아요 함수를 전역에 노출
window.likeApi = {
  postMusicLike: function(musicId) {
    return postMusicLike(musicId);
  }
};

/**
 * 음악 좋아요 처리 간소화 함수
 * HTML에서 직접 호출하기 위한 래퍼 함수
 */
function handleMusicLike(musicId) {
  postMusicLike(musicId)
    .then(() => {
      // 성공 처리는 함수 내에서 이미 처리됨
    })
    .catch(error => {
      console.error('좋아요 처리 실패:', error);
    });
}
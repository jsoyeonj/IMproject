// API 설정
const BASE_URL = window.location.origin; // 현재 서버의 기본 URL을 사용

// 기본 요청 함수 (JSON 요청)
async function fetchApi(url, options = {}) {
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include', // 쿠키 포함
  };

  const mergedOptions = { ...defaultOptions, ...options };

  if (mergedOptions.body && typeof mergedOptions.body === 'object' && !(mergedOptions.body instanceof FormData)) {
    mergedOptions.body = JSON.stringify(mergedOptions.body);
  }

  try {
    const response = await fetch(url, mergedOptions);

    if (!response.ok) {
      throw new Error(`API 요청 실패: ${response.status}`);
    }

    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      return await response.json();
    }

    return await response.text();
  } catch (error) {
    console.error('API 요청 오류:', error);
    throw error;
  }
}

// 일반 API 요청 (인증 없음)
async function httpRequest(endpoint, options = {}) {
  return fetchApi(`${BASE_URL}/api${endpoint}`, options);
}

// 멤버 관련 요청
async function memberRequest(endpoint, options = {}) {
  return fetchApi(`${BASE_URL}${endpoint}`, options);
}

// 인증이 필요한 API 요청
async function authorizationRequest(endpoint, options = {}) {
  const accessToken = localStorage.getItem('accessToken');
  const authOptions = {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': accessToken
    }
  };

  return fetchApi(`${BASE_URL}/api${endpoint}`, authOptions);
}

// 이미지 업로드 요청
async function imageRequest(endpoint, formData, options = {}) {
  const imageOptions = {
    ...options,
    method: options.method || 'POST',
    body: formData,
    headers: {
      // FormData를 사용할 때는 Content-Type을 설정하지 않음
      // 브라우저가 자동으로 multipart/form-data와 boundary를 설정
    }
  };

  return fetchApi(`${BASE_URL}/api${endpoint}`, imageOptions);
}

// 인증이 필요한 이미지 업로드 요청
async function imageMemberRequest(endpoint, formData, options = {}) {
  const accessToken = localStorage.getItem('accessToken');
  const imageOptions = {
    ...options,
    method: options.method || 'POST',
    body: formData,
    headers: {
      'Authorization': accessToken
    }
  };

  return fetchApi(`${BASE_URL}/api${endpoint}`, imageOptions);
}

// API 함수들을 전역으로 노출
window.api = {
  httpRequest,
  memberRequest,
  authorizationRequest,
  imageRequest,
  imageMemberRequest
};
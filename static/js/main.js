// static/js/main.js

// ProcessButton 클릭 시 해당 경로로 이동하는 함수..
function handleProcessButton(route) {
  window.location.href = '/' + route;
}

// ProcessButton 클릭 이벤트 처리(확인용)
function onClickProcess(route) {
  console.log("Process button clicked: " + route);
  window.location.href = "/" + route;
}

  // 페이지가 로드된 후 실행할 코드를 여기에 추가할 수 있습니다
});

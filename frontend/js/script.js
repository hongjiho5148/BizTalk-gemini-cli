// js/script.js

document.addEventListener('DOMContentLoaded', () => {
    const originalText = document.getElementById('originalText');
    const currentCharCount = document.getElementById('currentCharCount');
    const convertBtn = document.getElementById('convertBtn');
    const convertedText = document.getElementById('convertedText');
    const copyBtn = document.getElementById('copyBtn');
    const copyFeedback = document.getElementById('copyFeedback');
    const errorMsg = document.getElementById('errorMsg');
    const btnText = convertBtn.querySelector('.btn-text');
    const spinner = convertBtn.querySelector('.spinner');

    // 1. 실시간 글자 수 세기
    originalText.addEventListener('input', () => {
        const length = originalText.value.length;
        currentCharCount.textContent = length;
    });

    // 2. 변환 버튼 클릭 이벤트
    convertBtn.addEventListener('click', async () => {
        const text = originalText.value.trim();
        const target = document.querySelector('input[name="target"]:checked').value;

        if (!text) {
            alert('변환할 내용을 입력해주세요.');
            return;
        }

        // UI 상태: 로딩 시작
        setLoading(true);
        errorMsg.classList.add('hidden');

        try {
            const response = await fetch('/api/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text, target })
            });

            if (!response.ok) {
                throw new Error('네트워크 응답에 문제가 있습니다.');
            }

            const data = await response.json();
            convertedText.value = data.converted_text;
        } catch (error) {
            console.error('Error:', error);
            errorMsg.classList.remove('hidden');
        } finally {
            // UI 상태: 로딩 종료
            setLoading(false);
        }
    });

    // 3. 복사하기 버튼 클릭 이벤트
    copyBtn.addEventListener('click', () => {
        const textToCopy = convertedText.value;

        if (!textToCopy) return;

        navigator.clipboard.writeText(textToCopy).then(() => {
            // 시각적 피드백 제공
            copyFeedback.classList.remove('hidden');
            setTimeout(() => {
                copyFeedback.classList.add('hidden');
            }, 2000);
        }).catch(err => {
            console.error('복사 실패:', err);
        });
    });

    // 로딩 상태 제어 함수
    function setLoading(isLoading) {
        if (isLoading) {
            convertBtn.disabled = true;
            btnText.classList.add('hidden');
            spinner.classList.remove('hidden');
        } else {
            convertBtn.disabled = false;
            btnText.classList.remove('hidden');
            spinner.classList.add('hidden');
        }
    }
});
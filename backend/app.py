import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

app = Flask(__name__)

# CORS 설정: 개발 환경에서는 모든 오리진 허용 (배포 시 수정 필요)
CORS(app)

# Groq API Key 확인 (사용을 위해 .env 파일 설정 필요)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.route('/api/health', methods=['GET'])
def health_check():
    """서버 상태 확인용 엔드포인트"""
    return jsonify({
        "status": "healthy",
        "service": "BizTone Converter API",
        "version": "v1.0"
    }), 200

@app.route('/api/convert', methods=['POST'])
def convert_text():
    """
    텍스트 변환 엔드포인트
    Request Body: { "text": "...", "target": "boss" | "colleague" | "customer" }
    """
    try:
        data = request.get_json()
        
        # 입력 유효성 검사
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        text = data.get('text', '').strip()
        target = data.get('target', 'boss') # 기본값: 상사

        if not text:
            return jsonify({"error": "Text is required"}), 400
            
        if len(text) > 500:
            return jsonify({"error": "Text exceeds 500 characters"}), 400

        # TODO: 실제 Groq AI API 연동 구현 (Sprint 3)
        # 현재는 Phase 1 단계이므로 더미 응답 반환
        
        # 더미 변환 로직 (테스트용)
        mock_prefix = {
            "boss": "[상사용 변환] ",
            "colleague": "[동료용 변환] ",
            "customer": "[고객용 변환] "
        }
        converted_text = f"{mock_prefix.get(target, '[변환] ')} {text} (실제 AI 변환은 추후 구현됩니다.)"

        response_data = {
            "original": text,
            "converted": converted_text,
            "target": target,
            "status": "success_mock"
        }
        
        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # 로컬 개발 서버 실행
    app.run(debug=True, port=5000)

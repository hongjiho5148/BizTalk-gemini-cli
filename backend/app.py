import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../frontend', static_url_path='')
# 모든 출처에서의 요청을 허용 (CORS)
CORS(app) 

# Groq 클라이언트 초기화
# API 키는 환경 변수 'GROQ_API_KEY'에서 자동으로 로드됩니다.
try:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        logger.warning("GROQ_API_KEY is not set in environment variables.")
    groq_client = Groq(api_key=api_key)
    logger.info("Groq client initialized successfully.")
except Exception as e:
    groq_client = None
    logger.error(f"Error initializing Groq client: {e}")

# 대상별 프롬프트 정의
PROMPTS = {
    "Upward": (
        "상사에게 보고하는 상황입니다. 다음 원문을 정중한 격식체(하십시오체)로 변환하세요. "
        "결론부터 명확하게 제시하고, 신뢰감을 주는 전문적인 보고 형식을 갖춰주세요."
    ),
    "Lateral": (
        "타 부서 동료에게 협조를 요청하는 상황입니다. 다음 원문을 친절하고 상호 존중하는 어투로 변환하세요. "
        "요청 사항과 마감 기한을 명확히 전달하며 원활한 협업을 이끌어낼 수 있는 형식으로 작성하세요."
    ),
    "External": (
        "고객이나 외부 업체에 보내는 상황입니다. 다음 원문을 극존칭을 사용하여 매우 정중하게 변환하세요. "
        "전문성과 서비스 마인드가 느껴지도록 하며, 안내, 공지, 사과 등 목적에 부합하는 격식을 갖춰주세요."
    )
}

@app.route('/api/convert', methods=['POST'])
def convert_text():
    """
    Groq AI API를 사용하여 텍스트를 대상에 맞는 말투로 변환합니다.
    """
    if not groq_client:
        return jsonify({"error": "AI 서비스가 구성되지 않았습니다. API 키를 확인해주세요."}), 500

    data = request.json
    original_text = data.get('text')
    target = data.get('target')

    if not original_text or not target:
        return jsonify({"error": "텍스트와 변환 대상은 필수입니다."}), 400

    if target not in PROMPTS:
        return jsonify({"error": "잘못된 변환 대상입니다."}), 400

    logger.info(f"Conversion request: target={target}, text_len={len(original_text)}")

    try:
        system_instruction = PROMPTS[target]
        
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"당신은 비즈니스 커뮤니케이션 전문가입니다. {system_instruction} 원문의 의미를 훼손하지 않으면서 자연스러운 한국어 비즈니스 문장으로 변환하세요. 결과물만 출력하세요."
                },
                {
                    "role": "user",
                    "content": original_text,
                }
            ],
            model="moonshotai/kimi-k2-instruct-0905",
            temperature=0.7,
            max_tokens=1000,
        )

        converted_text = chat_completion.choices[0].message.content.strip()
        logger.info("Conversion successful.")

        response_data = {
            "original_text": original_text,
            "converted_text": converted_text,
            "target": target
        }
        
        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Error during API call: {e}")
        return jsonify({"error": "변환 도중 오류가 발생했습니다. 다시 시도해 주세요."}), 500

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
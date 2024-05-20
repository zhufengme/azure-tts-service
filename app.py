import os
import requests
from flask import Flask, request, send_file, jsonify
import logging
from io import BytesIO

# 初始化Flask应用
app = Flask(__name__)

# 配置日志记录
logging.basicConfig(level=logging.INFO)

# 获取Azure订阅密钥和区域
subscription_key = os.getenv('AZURE_SUBSCRIPTION_KEY')
region = os.getenv('AZURE_REGION')

if not subscription_key or not region:
    logging.error("Environment variables AZURE_SUBSCRIPTION_KEY and AZURE_REGION must be set.")
    raise ValueError("Environment variables AZURE_SUBSCRIPTION_KEY and AZURE_REGION must be set.")

def get_token(subscription_key, region):
    fetch_token_url = f"https://{region}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    response = requests.post(fetch_token_url, headers=headers)
    response.raise_for_status()
    return response.text

def text_to_speech(subscription_key, region, text, voice_name="en-US-AriaNeural", style="general", rate="0%"):
    token = get_token(subscription_key, region)
    tts_url = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm'
    }
    ssml = f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
        <voice name="{voice_name}">
            <mstts:express-as style="{style}">
                <prosody rate="{rate}">{text}</prosody>
            </mstts:express-as>
        </voice>
    </speak>
    """
    logging.info(f"SSML Request: {ssml}")
    response = requests.post(tts_url, headers=headers, data=ssml.encode('utf-8'))
    response.raise_for_status()

    if response.headers['Content-Type'] == 'audio/wav':
        logging.info("Audio content received")
    else:
        logging.warning(f"Unexpected content type: {response.headers['Content-Type']}")
    return BytesIO(response.content)

@app.route('/tts', methods=['POST'])
def synthesize():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            logging.error("Invalid request data: 'text' field is required.")
            return jsonify({'error': "Invalid request data: 'text' field is required."}), 400

        text = data['text']
        voice_name = data.get('voice_name', 'en-US-AriaNeural')
        style = data.get('style', 'general')
        rate = data.get('rate', '0%')

        audio_stream = text_to_speech(subscription_key, region, text, voice_name, style, rate)
        return send_file(audio_stream, mimetype='audio/wav', as_attachment=True, download_name='output.wav')

    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
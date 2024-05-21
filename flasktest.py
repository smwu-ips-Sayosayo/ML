import numpy as np
from flask import Flask, Response, request, json, jsonify

import cv2
import camera2
import io

app = Flask(__name__)
@app.route('/stream', methods=['POST'])
def stream():
    # 프레임 받아 처리
    frame_data = request.data
    np_arr = np.frombuffer(frame_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    # 객체 감지 , 손 인식
    processed_frame = camera2.process_stream(frame)

    _, buffer = cv2.imencode('.jpg', processed_frame)
    buffer = io.BytesIO(buffer)

    # 결과 반환
    response = {
        "result": "카메라 실행 완료"
    }
    return jsonify(response)


@app.route("/test", methods=['GET'])
def versionCheck():
    print("받은 Json 데이터 ")
    response = {
        "result": "ok"
    }
    return jsonify(response)
from flask import Flask, request

app = Flask(__name__)

@app.route('/video', methods=['POST'])
def receive_image():
    try:
        image_data = request.get_data()
        # 여기서 image_data를 사용하여 이미지 처리를 수행할 수 있습니다.

        # 연결 확인 응답을 보냅니다.
        return '연결됨', 200
    except Exception as e:
        return f'에러: {e}', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
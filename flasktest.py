import numpy as np
from flask import Flask, Response, request, json, jsonify

import cv2
import camera2

app = Flask(__name__)
@app.route('/stream', methods=['POST'])
def stream():
    # 프레임 받아 처리
    frame_data = request.data
    np_arr = np.frombuffer(frame_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    # 객체 감지 , 손 인식
    processed_frame = camera2.process_stream(frame)
    # 결과 반환
    response = {
        "result": "카메라 실행 완료"
    }
    return jsonify(response)


@app.route("/test", methods=['POST'])
def versionCheck():
    # params = request.get_json()
    # print("받은 Json 데이터 ", params)
    response = {
        "result": "ok"
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

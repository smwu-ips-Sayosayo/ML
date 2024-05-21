import numpy as np
from flask import Flask, Response, request, json, jsonify
from PIL import Image
import cv2
import camera2
import io

app = Flask(__name__)
@app.route('/stream', methods=['POST'])
def stream():
    # 프레임 받아 처리
    frame_data = request.data
    if not frame_data:
        return jsonify({'error': 'No data provided'}), 400

        # 바이너리 데이터를 이미지로 변환
    image = Image.open(io.BytesIO(frame_data))
    image = np.array(image)
    # np_arr = np.frombuffer(frame_data, np.uint8)
    # frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # 객체 감지 , 손 인식
    processed_frame = camera2.process_stream(image)



    # 결과 반환
    response = {
        "result": "카메라 실행이 완료됐습니다",
        "data": processed_frame
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
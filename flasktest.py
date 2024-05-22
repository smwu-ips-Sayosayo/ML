import base64
import logging
import io

import numpy as np
from flask import Flask, Response, request, json, jsonify
from PIL import Image
import cv2
import camera2
import os

app = Flask(__name__)
@app.route('/stream', methods=['POST'])
def stream():
    try:
        image_data = request.data
        if image_data:
            try:
                # Bytes 데이터를 이미지로 변환
                image = Image.open(io.BytesIO(image_data))
                image.show()  # 이미지를 열어 확인
                image = np.array(image)
                # image= cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                # 이미지 저장
                save_path = 'received_image.jpg'
                cv2.imwrite(save_path, image)
                print(f"Image saved to {save_path}")

                processed_frame = camera2.process_stream(image)
                print("Processed frame objects:", processed_frame)  # 추가된 디버깅 메시지
                return jsonify({"message": processed_frame}), 200
            except Exception as e:
                print(f"Error processing image: {e}")
                return jsonify({"error": str(e)}), 400
        # 결과 반환
            response = {
                "result": "카메라 실행이 완료됐습니다",
                "data": processed_frame
            }
        return jsonify(response)
    except Exception as e:
        # 오류가 발생할 경우 오류 메시지와 함께 500 응답 반환
        logging.error(f"Error processing image: {e}")
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
sudo apt-get update
sudo apt-get install cmake libjpeg8-dev #아마 turbo 어쩌구로 깔라고 메시지가 나왔던것 같다, 그걸로 깔면된다
sudo apt-get install gcc g++
git clone https://github.com/jacksonliam/mjpg-streamer.git
cd mjpg-streamer/mjpg-streamer-experimental
make
sudo make install #환경설치

mjpg_streamjer -i "input_uvc.so" -o "output_http.so" #서버 열기

http://라즈베리파이ip주소:8080/?action=stream 
#기본 포트는 8080, 같은 와이파이가 연결된 기기에서 실행가능, 참고로 실습실 컴퓨터엔 와이파이가 안된다..

#만약 카메라 모듈이 여러개라면 포트와 비디오 모듈을 지정해주고 여러 화면을 띄울 수 있다
v4l2-ctl --list-devices #사용가능한 비디오 인풋 확인하기

mjpg_streamer -i "input_uvc.so -d /dev/video숫자" -o "output_http.so -p 포트숫자" 
#위의 코드에서 video숫자를 video0,video1등 비디오 인풋에서 필요한 인풋의 숫자를 적는다
#포트숫자는 주로 8080,8081,8082를 사용했다
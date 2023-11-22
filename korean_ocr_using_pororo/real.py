import subprocess

# 응용 프로그램의 경로를 지정합니다.
exe_path = r"C:\Users\k3553\Documents\py\korean_ocr_using_pororo\upup\realesrgan-ncnn-vulkan.exe"

# 입력 파일명, 출력 파일명, 및 스케일 값을 지정합니다.
input_file = "asqw.jpg"
output_file = "aswqwe.jpg"
scale = "3"

# subprocess.run 함수를 이용하여 응용 프로그램을 실행하고, 파라미터를 전달합니다.
subprocess.run([exe_path, "-i", input_file, "-s", scale, "-o", output_file])
